# pip install --upgrade google-cloud-storage

from urllib.request import Request
from google.cloud import storage

import pickle

App_Model = {}
App_Model['DateOfLastAPIRequest'] = None

GCP_Model = {}
GCP_Model['GCP_Client'] = storage.Client()
GCP_Model['GCP_BucketName'] = '20220615-datastore'
GCP_Model['GCP_Bucket'] = GCP_Model['GCP_Client'].bucket(GCP_Model['GCP_BucketName'])
GCP_Model['GCP_FileName'] = 'App_Model_20220613'

def StoreAppModel(GCP_Model, App_Model):
    Bucket = GCP_Model['GCP_Bucket']
    FileName = GCP_Model['GCP_FileName']
    with open(FileName+'.pickle', 'wb') as handle:
            pickle.dump(App_Model, handle, protocol=pickle.HIGHEST_PROTOCOL)
    Blob = Bucket.blob(FileName)
    Blob.upload_from_filename(FileName+'.pickle')
    
def InitateAppModel(GCP_Model, App_Model):
    Bucket = GCP_Model['GCP_Bucket']
    StorageClient = GCP_Model['GCP_Client']
    FileName = GCP_Model['GCP_FileName']
    #Note name should not include file extension
    if storage.Blob(bucket=Bucket, name=FileName).exists(StorageClient):
        #If the file exists, pull
        Blob = Bucket.get_blob(FileName)
        App_Model = pickle.loads(Blob.download_as_string())
    else:
        #If the file does not exist, push
        StoreAppModel(GCP_Model, App_Model)
    return App_Model

InitateAppModel(GCP_Model, App_Model)



