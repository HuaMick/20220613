# pip install --upgrade google-cloud-storage

from urllib.request import Request
from google.cloud import storage

App_Model = {}
App_Model['GCP_Bucket_Name'] = '20220615-datastore'
App_Model['GCP_Client'] = storage.Client()
App_Model['GCP_Bucket'] = App_Model['GCP_Client'].bucket(App_Model['GCP_Bucket_Name'])
App_Model['Metadata'] = {'DateOfLastAPIRequest':None}

import pickle
#pickle doesn't support client objects, so best we dont do the whole app_model
def InitateAppMetadata(StorageClient, Bucket, Metadata = App_Model['Metadata']):
    FileName = 'App_Metadata'
    #Note name should not include file extension
    if storage.Blob(bucket=Bucket, name=FileName).exists(StorageClient):
        pass
    else:
        with open(FileName+'.pickle', 'wb') as handle:
            pickle.dump(Metadata, handle, protocol=pickle.HIGHEST_PROTOCOL)
        Blob = Bucket.blob(FileName)
        Blob.upload_from_filename('App_Metadata.pickle')

InitateAppMetadata(StorageClient = App_Model['GCP_Client'], Bucket = App_Model['GCP_Bucket'] , Metadata = App_Model['Metadata'])

bucket = App_Model['GCP_Client'].get_bucket('20220615-datastore')
# Then do other things...
blob = bucket.get_blob('20220615')
print(blob.download_as_bytes())
print(blob.download_as_text())



name = 'file_i_want_to_check.txt'   
storage_client = storage.Client()
bucket_name = 'my_bucket_name'

stats = storage.Blob(bucket=bucket, name=name).exists(storage_client)


bucket_name = '20220615-datastore'
storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)












def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )
