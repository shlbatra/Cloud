from google.cloud import storage


def list_cs_files(bucket_name): 
    # Create a client object

    client = storage.Client()

    # List all the buckets in your project

    buckets = list(client.list_buckets())

    # Check if the bucket you created is in the list of buckets

    for bucket in buckets:
        if bucket.name == "my-first-bucket14755286":
          print("Bucket found!")

    print(file_list = [bucket.name for bucket in buckets])