import sys
import boto3

athena = boto3.client("athena")
s3 = boto3.resource("s3")

RESULT_BUCKET = sys.argv[1]


def main():
    query_exeqution_id = select_avgtemp_by_prefecture(athena)
    print("Athena select_avgtemp_by_prefecture Run success")
    download_csv_to_local(s3, RESULT_BUCKET, query_exeqution_id, "result_all.csv")
    query_exeqution_id = select_avgtemp_at_kanto(athena)
    print("Athena select_avgtemp_at_kanto Run success")
    download_csv_to_local(s3, RESULT_BUCKET, query_exeqution_id, "result_kanto.csv")


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
            low_temperature != '') as weather
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


def select_avgtemp_by_prefecture(athena):
    sql = """
        SELECT 
       MAX(station.prefecture) AS prefecture,
       AVG(CAST(weather.avg_temperature AS double)) AS avg_temperature,
       MAX(station.latitude) AS latitude,
       MAX(station.longitude) AS longitude,
       MAX(station.altitude) AS altitude
    FROM (
      SELECT datetime, 
        avg_temperature, 
        precipitation, 
        hours_sunlight, 
        avg_wind_speed,
        station_id
      FROM "weather_v2"."weather_with_station_id"
      WHERE avg_temperature != '') as weather
    LEFT JOIN ( 
      SELECT id, 
             prefecture,
             latitude,
             longitude,
             altitude
      FROM "weather_v2"."station") as station
    ON weather.station_id = station.id
    GROUP BY station.prefecture;
    """
    results = execute_athena_query(athena, sql)
    return results


def select_avgtemp_at_kanto(athena):
    sql = """
    SELECT 
       weather.station_id,
       weather.datetime,
       weather.avg_temperature,
       station.prefecture,
       station.latitude,
       station.longitude,
       station.altitude
    FROM (
      SELECT datetime, 
        avg_temperature, 
        station_id
      FROM "weather_v2"."weather_with_station_id"
      WHERE avg_temperature != '') as weather
    LEFT JOIN ( 
      SELECT id, 
             prefecture,
             latitude,
             longitude,
             altitude
      FROM "weather_v2"."station") as station
    ON weather.station_id = station.id
    WHERE station.prefecture = 'tokyo' OR
              station.prefecture = 'kanagawa' OR
              station.prefecture = 'saitama' OR
              station.prefecture = 'chiba' OR
              station.prefecture = 'gunma' OR
              station.prefecture = 'tochigi' OR
              station.prefecture = 'ibaraki';
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


def download_csv_to_local(s3, result_bucket, query_exeqution_id, local_name):
    s3.meta.client.download_file(result_bucket, query_exeqution_id + ".csv", local_name)


if __name__ == "__main__":
    main()
