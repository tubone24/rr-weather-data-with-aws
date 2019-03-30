import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql.functions import input_file_name, regexp_replace
from awsglue.context import GlueContext
from awsglue.job import Job


args = getResolvedOptions(sys.argv, ["JOB_NAME"])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Create Glue DynamicFrame
datasource0 = glueContext.create_dynamic_frame.from_catalog(database="weather", table_name="glueweather_data", transformation_ctx="datasource0")

# Extract necessary column
applymapping1 = ApplyMapping.apply(frame=datasource0, mappings=[("calendar_date", "string", "date", "string"), ("avg_temperature", "double", "avg_temperature", "double"), ("high_temperature", "double", "high_temperature", "double"), ("low_temperature", "double", "low_temperature", "double"), ("precipitation", "double", "precipitation", "double"), ("hours_sunlight", "double", "hours_sunlight", "double"), ("solar_radiation", "double", "solar_radiation", "double"), ("avg_wind_speed", "double", "avg_wind_speed", "double")], transformation_ctx="applymapping1")
resolvechoice2 = ResolveChoice.apply(frame=applymapping1, choice="make_struct", transformation_ctx="resolvechoice2")
dropnullfields3 = DropNullFields.apply(frame=resolvechoice2, transformation_ctx="dropnullfields3")

# Convert Glue DynamicFrame to Pyspark DataFrame
dataFrame = dropnullfields3.toDF()

# Add file_name
add_filename = dataFrame.withColumn("file_name", input_file_name())

# Convert into station_id
add_station_id = add_filename.withColumn("station_id", regexp_replace("file_name", "s3://athena-origin-data20190317/weather-data/", ""))
fix_station_id = add_station_id.withColumn("station_id", regexp_replace("station_id", ".csv", ""))

# Write CSV with compression
fix_station_id.write.mode("append").csv("s3://athena-origin-data20190317/weather-data-with-station-id", compression="gzip")

# Write parquet
# fix_station_id.write.mode("overwrite").parquet("s3://athena-origin-data20190317/weather-data-with-station-id")

job.commit()