CREATE EXTERNAL TABLE `${database_name}.${table_name}`(
  `datetime` date,
  `avg_temperature` string,
  `high_temperature` string,
  `low_temperature` string,
  `precipitation` string,
  `hours_sunlight` string,
  `solar_radiation` string,
  `avg_wind_speed` string,
  `s3_csv_path` string,
  `station_id` string)
ROW FORMAT DELIMITED
  FIELDS TERMINATED BY ','
STORED AS INPUTFORMAT
  'org.apache.hadoop.mapred.TextInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://${weather_with_station_id_bucket}'
TBLPROPERTIES (
  'skip.header.line.count'='1')