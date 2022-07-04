
import model
import requests

import pickle
from datetime import date
from os.path import exists
from google.cloud import storage

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

def API_Pull(Resources, Info):
    Request_URL = 'https://api.transport.nsw.gov.au/v2/gtfs/alerts/buses?format=json'
    Resources['API']['AppName'].append(Info['AppName'])
    Resources['API']['RequestDate'].append(date.today())
    try:
        Resources['API']['Response'].append(requests.get(
        Request_URL, headers={
            'Authorization': 'apikey rG3uaQgSxI8LbkMvtwS9fp61tZdQmxDOcqNj'
            }))
        Resources['API']['Status'].append('Pass')
    except Exception as e:
        Resources['API']['Status'] = 'Fail'
        Resources['API']['Response'].append(e[0:100])
    
    Resources = model.Resources_Save(Resources)
    return Resources

def Count_Requests(Date, Resources):
    R = Resources['API']['RequestDate']
    if date in R:
        Rn = ({str(k):R.count(k) for k in set(R)})[str(Date)]
        print(Rn)
    else:
        Rn = 0    
    return 200

Run = False
if Run:
    model.Resources = App_Init(Resources = model.Resources, GCP = model.GCP)
    model.Resources = API_Pull(Resources = model.Resources, Info = model.Info)
    model.Resources = model.GCP_Push(GCP = model.GCP, Resources=model.Resources)
