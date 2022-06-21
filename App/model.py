# pip install --upgrade google-cloud-storage
import datetime
from datetime import date
from urllib.request import Request
from google.cloud import storage

import pickle

Info = {}
Info['AppName'] = '20220613'

Resources = {}
Resources['API'] = {}
Resources['GCP'] = {}
Resources['API']['AppName'] = []
Resources['API']['RequestDate'] = []
Resources['API']['Status'] = []
Resources['API']['Response'] = []
Resources['GCP']['AppName'] = []
Resources['GCP']['RequestDate'] = []
Resources['GCP']['RequestType'] = []
Resources['GCP']['Response'] = []

GCP = {}
GCP['GCP_Client'] = storage.Client()
GCP['GCP_BucketName'] = '20220618-bucket'
GCP['GCP_Bucket'] = GCP['GCP_Client'].bucket(GCP['GCP_BucketName'])

VIEW_Model={}
VIEW_Model['ContactInfo'] = ("""
Author: Mick Hua
Linkedin: https://www.linkedin.com/in/mick-hua-3    53353a/
github: https://github.com/HuaMick/20220609
""")
VIEW_Model['STEP1Text0'] = ("""
Step 1: Store Application metadata on GCP
""")
VIEW_Model['STEP1Text1'] = ("""
API has request limits so we want to limit requestst to Once a Day
""")
VIEW_Model['STEP1Text2'] = ("""
Create App Metadata To Store When Last Request Was made
""")
VIEW_Model['STEP1Code1'] = ("""
App_Model = {}
App_Model['GCP_Bucket_Name'] = '20220615-datastore'
App_Model['GCP_Client'] = storage.Client()
App_Model['GCP_Bucket'] = App_Model['GCP_Client'].bucket(App_Model['GCP_Bucket_Name'])
App_Model['Metadata'] = {'DateOfLastAPIRequest':None}
""")
VIEW_Model['STEP1Text3'] = ("""
Use a function to pickle the metadata and store it in GCP
""")
VIEW_Model['STEP1Code2'] = ("""
import pickle
#pickle doesn't support client objects, so best we dont do the whole app_model
def InitateAppMetadata(StorageClient, Bucket, Metadata = App_Model['Metadata']):
    FileName = 'App_Metadata'
    #Note name should not include file extension
    if storage.Blob(bucket=Bucket, name=FileName).exists(StorageClient):
        #If the file exists, pull
        Blob = bucket.get_blob(FileName)
        Metadata = pickle.loads(Blob.download_as_string())
    else:
        #If the file does not exist, push
        with open(FileName+'.pickle', 'wb') as handle:
            pickle.dump(Metadata, handle, protocol=pickle.HIGHEST_PROTOCOL)
        Blob = Bucket.blob(FileName)
        Blob.upload_from_filename('App_Metadata.pickle')
    return Metadata
""")
VIEW_Model['STEP1Text4'] = ("""
If we Initate the App Metadata we get:
""")
VIEW_Model['STEP2Text0'] = ("""
Step 2: Pull API Data
When we pull the API data we want to note the date we pulled and store it
When we request again we can check the last date it was pulled.
""")
VIEW_Model['STEP2Code0'] = ("""
def API_Request(App_Model):
    Request_URL = 'https://api.transport.nsw.gov.au/v2/gtfs/alerts/buses?format=json'
    Response = {}
    if App_Model['DateOfLastAPIRequest'] == date.today():
        Response['Status'] = 'Fail'
        Response['Description'] = 'You can only make 1 request per a day'
        Response['Payload'] = None
        
        return Response
    else:
        Response = requests.get(Request_URL, headers={
            'Authorization': 'apikey rG3uaQgSxI8LbkMvtwS9fp61tZdQmxDOcqNj'})
        Response['Status'] = 'Pass'
        Response['Description'] = ''
        Response['Payload'] = Response

        App_Model['DateOfLastAPIRequest'] = date.today()
        model.StoreAppModel(App_Model)
        
        return Response
""")

from os.path import exists

def Resources_Save(Resources):
    with open('Resources.pickle', 'wb') as handle:
        pickle.dump(Resources, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return Resources

def Resources_Load(Resources):
    if exists('Resources.pickle'):
        file = open("Resources.pickle",'rb')
        Resources = pickle.load(file)
    return Resources

def GCP_Push(GCP, Resources):
    Bucket = GCP['GCP_Bucket']
    Blob = Bucket.blob('Resources')

    Resources = Resources_Load(Resources)

    Resources['GCP']['AppName'].append(Info['AppName'])
    Resources['GCP']['RequestDate'].append(date.today())
    Resources['GCP']['RequestType'].append('PUSH')
    Resources['GCP']['Response'].append(Blob.__repr__())

    Resources = Resources_Save(Resources)

    Blob.upload_from_filename('Resources.pickle')
    return Resources

def GCP_Pull(GCP, Resources):
    Bucket = GCP['GCP_Bucket']
    Blob = Bucket.get_blob('Resources')

    Resources = pickle.loads(Blob.download_as_string())

    Resources['GCP']['AppName'].append(Info['AppName'])
    Resources['GCP']['RequestDate'].append(date.today())
    Resources['GCP']['RequestType'].append('PULL')
    Resources['GCP']['Response'].append(Blob.__repr__())

    Resources = Resources_Save(Resources)

    return Resources





