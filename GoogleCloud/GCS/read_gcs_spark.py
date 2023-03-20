
# Apache Spark doesn’t have out of the box support for Google Cloud Storage, we need 
# to download and add the connector separately. 
# It is a jar file

from pyspark.sql import SparkSession
spark = SparkSession.builder.appName(‘GCSFilesRead’).getOrCreate()

spark._jsc.hadoopConfiguration().set("google.cloud.auth.service.account.json.keyfile","<path_to_your_credentials_json>")

bucket_name="my_bucket"
path=f"gs://{bucket_name}/data/sample.csv"
df=spark.read.csv(path, header=True)
df.show()