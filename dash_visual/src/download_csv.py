import boto3

athena = boto3.client("athena")
s3 = boto3.resource("s3")

RESULT_BUCKET = "weather-athena-result-lambda"


def main():
    query_exeqution_id = select_weather(athena)
    print("Athena Run success")
    download_csv_to_local(s3, RESULT_BUCKET, query_exeqution_id)


def select_weather(athena):
    sql = """
    SELECT weather.datetime,
       weather.avg_temperature,
       weather.high_temperature,
       weather.low_temperature,
       weather.precipitation,
       weather.hours_sunlight,
       weather.avg_wind_speed,
       weather.path,
       weather.station_id,
       station.prefecture,
       station.first_name,
       station.second_name,
       station.latitude,
       station.longitude,
       station.altitude
    FROM (
      SELECT datetime, 
        avg_temperature, 
        high_temperature, 
        low_temperature, 
        precipitation, 
        hours_sunlight, 
        avg_wind_speed,
        "$path" as path,
        replace(replace("$path", 's3://athena-origin-data20190317/weather-data/'), '.csv') as station_id
      FROM "weather"."wearher_v2"
      WHERE avg_temperature != '' AND
            high_temperature != '' AND
            low_temperature != '' AND
            precipitation != '' AND
            hours_sunlight != '' AND
            avg_wind_speed != '') as weather
    LEFT JOIN ( 
      SELECT id, 
             prefecture,
             first_name,
             second_name,
             latitude,
             longitude,
             altitude
      FROM "weather"."station_v2") as station
    ON weather.station_id = station.id;
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
