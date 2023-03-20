# Imports the 'storage' module from the google.cloud package
# to allow interactions with the Google Cloud Storage.
from google.cloud import storage

def create_bucket(bucket_name, storage_class='STANDARD', location='us-central1'): 
    # Creates a Client object that allows the script to communicate
    # with Google Cloud Storage and perform operations on it (like creating a bucket).
    client = storage.Client()

    # Creates a new bucket with a specified name
    bucket = client.bucket(bucket_name)
    bucket.storage_class = storage_class
    bucket = client.create_bucket(bucket, location=location)

    # Prints a message indicating the bucket was successfully created.
    print("Bucket {} created.".format(bucket.name))