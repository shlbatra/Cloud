from google.cloud import storage
import os
from datetime import datetime, timedelta

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'/path/to/credentials/project-name-123456.json'

# define function that generates the public URL, default expiration is set to 24 hours
def get_cs_file_url(bucket_name, file_name, expire_in=datetime.today() + timedelta(1)): 
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    url = bucket.blob(file_name).generate_signed_url(expire_in)

    return url