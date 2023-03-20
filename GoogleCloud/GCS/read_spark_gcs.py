# https://kontext.tech/article/689/pyspark-read-file-in-google-cloud-storage
# https://junjiejiang94.medium.com/3-easy-step-to-use-google-storage-with-pyspark-fd053d1bde9

# Cloud storage connector

# Pass in the package as depedency when submitting application -> 
# spark-submit --packages com.google.cloud.bigdataoss:gcs-connector:hadoop3-2.2.0

#Run script using ->
#spark-submit --packages com.google.cloud.bigdataoss:gcs-connector:hadoop3-2.2.0 pyspark-gcs.py

from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StructType, StringType, IntegerType

appName = "PySpark Example - Read JSON file from GCS"
master = "local"

# Create Spark session
spark = SparkSession.builder \
    .appName(appName) \
    .master(master) \
    .getOrCreate()

# Setup hadoop fs configuration for schema gs://
conf = spark.sparkContext._jsc.hadoopConfiguration()
conf.set("fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")
conf.set("fs.AbstractFileSystem.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS")

# Create a schema for the dataframe
schema = StructType([
    StructField('ID', IntegerType(), True),
    StructField('ATTR1', StringType(), True)
])

# Create data frame
json_file_path = 'gs://YOUR_BUCKET/test.json'
df = spark.read.json(json_file_path, schema, multiLine=True)
print(df.schema)
df.show()