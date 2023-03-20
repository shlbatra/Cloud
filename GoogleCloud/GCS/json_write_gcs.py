from google.cloud import storage
import json

# credentials to get access google cloud storage
# write your key path in place of gcloud_private_key.json
# set key credentials file path
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'/path/to/credentials/project-name-123456.json'

# storage_client = storage.Client.from_service_account_json('gcloud_private_key.json')
storage_client = storage.Client()

# write your bucket name in place of bucket1go
bucket_name = 'bucket1go'
BUCKET = storage_client.get_bucket(bucket_name) # storage_client.bucket(bucket_name)

def create_json(json_object, filename):
    '''
    this function will create json object in
    google cloud storage
    '''
    # create a blob
    blob = BUCKET.blob(filename)
    # upload the blob 
    blob.upload_from_string(                 # blob.upload_from_filename("./my-file.txt")
        data=json.dumps(json_object), 
        content_type='application/json'
        )
    result = filename + ' upload complete'
    return {'response' : result}

# your object
json_object = {
    'Name': 'Anurag',
    'Age': '23'
}
# set the filename of your json object
filename = 'test.json'

# run the function and pass the json_object
print(create_json(json_object, filename))