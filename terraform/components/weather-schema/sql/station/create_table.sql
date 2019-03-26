CREATE EXTERNAL TABLE `${database_name}.${table_name}`(
  `id` string,
  `prefecture` string,
  `first_name` string,
  `second_name` string,
  `latitude` double,
  `longitude` double,
  `altitude` double,
  `date_terminated` string)
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