CREATE EXTERNAL TABLE `${database_name}.${table_name}`(
  `datetime` date,
  `avg_temperature` string,
  `high_temperature` string,
  `low_temperature` string,
  `precipitation` string,
  `hours_sunlight` string,
  `solar_radiation` string,
  `deepest_snowfall` string,
  `total_snowfall` string,
  `avg_wind_speed` string,
  `avg_vapor_pressure` string,
  `avg_local_pressure` string,
  `avg_humidity` string,
  `avg_sea_pressure` string,
  `cloud_cover` string)
ROW FORMAT DELIMITED
  FIELDS TERMINATED BY ','
STORED AS INPUTFORMAT
  'org.apache.hadoop.mapred.TextInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://${weather_data_bucket}'
TBLPROPERTIES (
  'skip.header.line.count'='1')