import sys
import boto3

athena = boto3.client("athena")
s3 = boto3.resource("s3")

RESULT_BUCKET = sys.argv[1]


def main():
    query_exeqution_id = select_weather(athena)
    print("Athena Run success")
    download_csv_to_local(s3, RESULT_BUCKET, query_exeqution_id)


def select_weather(athena):
    sql = """
    SELECT 
       weather.station_id,
       AVG(CAST(weather.avg_temperature AS double)) AS avg_temperature,
       MAX(CAST(weather.high_temperature AS double)) AS high_temperature,
       MIN(CAST(weather.low_temperature AS double)) AS low_temperature,
       MAX(station.prefecture) AS prefecture,
       MAX(station.first_name) AS first_name,
       MAX(station.second_name) AS second_name,
       MAX(station.latitude) AS latitude,
       MAX(station.longitude) AS longitude,
       MAX(station.altitude) AS altitude
    FROM (
      SELECT datetime, 
        avg_temperature, 
        high_temperature, 
        low_temperature, 
        precipitation, 
        hours_sunlight, 
        avg_wind_speed,
        station_id
      FROM "weather_v2"."weather_with_station_id"
      WHERE avg_temperature != '' AND
            high_temperature != '' AND
            low_temperature != '' AND) as weather
    LEFT JOIN ( 
      SELECT id, 
             prefecture,
             first_name,
             second_name,
             latitude,
             longitude,
             altitude
      FROM "weather_v2"."station") as station
    ON weather.station_id = station.id
    GROUP BY station_id;
    """
    results = execute_athena_query(athena, sql)
    return results


def execute_athena_query(athena, sql):
    print("Athena start_query_execution")
    response = athena.start_query_execution(
        QueryString=sql,
        ResultConfiguration={
            "OutputLocation": "s3://" + RESULT_BUCKET})

    query_exeqution_id = response["QueryExecutionId"]

    while True:
        get_status = athena.get_query_execution(QueryExecutionId=query_exeqution_id)
        status= get_status["QueryExecution"]["Status"]["State"]
        if status == "SUCCEEDED":
            break
        elif status == "FAILED":
            raise Exception(status)

    return query_exeqution_id


def download_csv_to_local(s3, result_bucket, query_exeqution_id):
    s3.meta.client.download_file(result_bucket, query_exeqution_id + ".csv", "./result.csv")


if __name__ == "__main__":
    main()
