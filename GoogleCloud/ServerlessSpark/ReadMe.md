- choose between Serverless, Kubernetes clusters, and compute clusters for their Spark applications
- By default, Dataproc Serverless runs workloads within Docker containers. This container provides the runtime environment for the workload’s driver and executor processes.
- Ex custom container image -> 
# Debian 11 is recommended.
FROM debian:11-slim

# Suppress interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# (Required) Install utilities required by Spark scripts.
RUN apt update && apt install -y procps tini

# (Optional) Add extra jars.
ENV SPARK_EXTRA_JARS_DIR=/opt/spark/jars/
ENV SPARK_EXTRA_CLASSPATH='/opt/spark/jars/*'
RUN mkdir -p "${SPARK_EXTRA_JARS_DIR}"
COPY spark-bigquery-with-dependencies_2.12-0.22.2.jar "${SPARK_EXTRA_JARS_DIR}"

# (Optional) Install and configure Miniconda3.
ENV CONDA_HOME=/opt/miniconda3
ENV PYSPARK_PYTHON=${CONDA_HOME}/bin/python
ENV PATH=${CONDA_HOME}/bin:${PATH}
COPY Miniconda3-py39_4.10.3-Linux-x86_64.sh .
RUN bash Miniconda3-py39_4.10.3-Linux-x86_64.sh -b -p /opt/miniconda3 \
  && ${CONDA_HOME}/bin/conda config --system --set always_yes True \
  && ${CONDA_HOME}/bin/conda config --system --set auto_update_conda False \
  && ${CONDA_HOME}/bin/conda config --system --prepend channels conda-forge \
  && ${CONDA_HOME}/bin/conda config --system --set channel_priority strict

# (Optional) Install Conda packages.
#
# The following packages are installed in the default image, it is strongly
# recommended to include all of them.
#
# Use mamba to install packages quickly.
RUN ${CONDA_HOME}/bin/conda install mamba -n base -c conda-forge \
    && ${CONDA_HOME}/bin/mamba install \
      conda \
      cython \
      fastavro \
      fastparquet \
      gcsfs \
      google-cloud-bigquery-storage \
      google-cloud-bigquery[pandas] \
      google-cloud-dataproc \
      koalas \
      matplotlib \
      nltk \
      numba \
      numpy \
      openblas \
      orc \
      pandas \
      pyarrow \
      pysal \
      pytables \
      python \
      regex \
      requests \
      rtree \
      scikit-image \
      scikit-learn \
      scipy \
      seaborn \
      sqlalchemy \
      sympy \
      virtualenv

# (Optional) Add extra Python modules.
ENV PYTHONPATH=/opt/python/packages


# (Required) Create the 'spark' group/user.
# The GID and UID must be 1099. Home directory is required.
RUN groupadd -g 1099 spark
RUN useradd -u 1099 -g 1099 -d /home/spark -m spark
USER spark


- Run commands below to set up docker image ->

IMAGE=gcr.io/my-project/my-image:1.0.1

# Download the BigQuery connector.
gsutil cp \
  gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.22.2.jar .

# Download the Miniconda3 installer.
wget https://repo.anaconda.com/miniconda/Miniconda3-py39_4.10.3-Linux-x86_64.sh

# Build and push the image.
docker build -t "${IMAGE}" .
docker push "${IMAGE}"

- Set up PySpark script 


#!/usr/bin/python
"""BigQuery I/O PySpark example."""
from pyspark.sql import SparkSession
spark = SparkSession \
.builder \
.appName('spark-bigquery') \
.getOrCreate()
# Use the Cloud Storage bucket for temporary BigQuery export data used by the connector.
#Specify a bucket with with json files
bucket = "my-bucket-name"
spark.conf.set('temporaryGcsBucket', bucket)
filePath=f"gs://{bucket}/"
df=spark.read.json(filePath)
# Saving the data to BigQuery
df.write.format('bigquery') \
.option('table', 'my-dataset.my-table') \
.save()

- Run on dataproc serverless as :

gcloud dataproc batches submit pyspark myscript.py
--batch my-batch-name
--container-image "gcr.io/my-gcp-project/spark-serverless:1.0.1"
--project my-project
--region my-region
--deps-bucket gcs-bucket
--service-account service-account
--subnet default
