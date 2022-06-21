
import model
import requests

import pickle
from datetime import date
from os.path import exists
from google.cloud import storage

def API_Pull(Resources, Info):
    Request_URL = 'https://api.transport.nsw.gov.au/v2/gtfs/alerts/buses?format=json'
    Resources['API']['AppName'].append(Info['AppName'])
    Resources['API']['RequestDate'].append(date.today())
    try:
        Payload = requests.get(
        Request_URL, headers={
            'Authorization': 'apikey rG3uaQgSxI8LbkMvtwS9fp61tZdQmxDOcqNj'
            })
        Resources['API']['Status'].append('Pass')
        Resources['API']['Response'].append(None)
    except Exception as e:
        Resources['API']['Status'] = 'Fail'
        Resources['API']['Response'].append(e[0:100])
    
    Resources = model.Resources_Save(Resources)
    return Resources

def Model_Init():
    if exists('Resources.pickle'):
        file = open("Resources.pickle",'rb')
        Resources = pickle.load(file)
        R = Resources['GCP']['RequestDate']
        if date.today() in R:
            Rn = ({k:R.count(k) for k in set(R)})[date.today()]
        else:
            Rn = 0
        print(Rn)
    
    return Resources

#Do all the stuff that needs to be done when the app starts
def App_Init(Resources, GCP):
    #If Resources doesnt exist create it
    if not exists('Resources.pickle'):
        with open('Resources.pickle', 'wb') as handle:
            pickle.dump(Resources, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    #If Resources is not on GCP -> Push else Pull
    if not storage.Blob(bucket=GCP['GCP_Bucket'], name='Resources').exists(GCP['GCP_Client']):
        Resources = model.GCP_Push(GCP, Resources)
    else:
        Resources = model.GCP_Pull(GCP, Resources)
    return Resources
    
Run = False
if Run:
    model.Resources = App_Init(Resources = model.Resources, GCP = model.GCP)
    model.Resources = API_Pull(Resources = model.Resources, Info = model.Info)
    model.Resources = model.GCP_Push(GCP = model.GCP, Resources=model.Resources)





def API_Request(App_Model):
    Request_URL = 'https://api.transport.nsw.gov.au/v2/gtfs/alerts/buses?format=json'
    Response = {}
    if App_Model['DateOfLastAPIRequest'] == date.today():
        Response['Status'] = 'Fail'
        Response['Description'] = 'You can only make 1 request per a day'
        Response['Payload'] = None
        
        return Response
    else:
        Response['Payload'] = (requests.get(Request_URL, headers={
            'Authorization': 'apikey rG3uaQgSxI8LbkMvtwS9fp61tZdQmxDOcqNj'})).json()
        Response['Status'] = 'Pass'
        Response['Description'] = ''

        App_Model['DateOfLastAPIRequest'] = date.today()
        App_Model['API_Response'] = Response['Payload']
        model.StoreAppModel(model.GCP_Model, App_Model)
        
        return Response






def TNSW_API_request():
    response = requests.get(
    'https://api.transport.nsw.gov.au/v2/gtfs/alerts/buses?format=json'
    , headers={'Authorization': 'apikey rG3uaQgSxI8LbkMvtwS9fp61tZdQmxDOcqNj'})
    return response.json()

