
import model
import requests

import pickle
from datetime import date
from os.path import exists
from google.cloud import storage

#model.Resources = App_Init(model.Resources, model.GCP)
#api_requests = pd.DataFrame({k:v for k,v in model.Resources['API'].items() if k in ['RequestDate', 'Status']})
    
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
    if Date in R:
        Rn = ({str(k):R.count(k) for k in set(R)})[str(Date)]
    else:
        Rn = 0    
    return Rn

Testing = False
if Testing:
    import toml
    import datetime
    import pandas as pd
    Secrets = (toml.load(".streamlit\secrets.toml"))['gcp_service_account']
    model.Model_Init(Secrets)
    model.Resources = App_Init(Resources = model.Resources, GCP = model.GCP)

    

    json_response = model.Resources['API']['Response'][0].json()
    header = json_response['header']
    body = {v['id']:v['alert'] for v in json_response['entity']}
    

    dataset = {
        'id':[]
        , 'start': []
    }

    for n0, (id, alert) in enumerate(body.items()):
        print(id)
        print(alert['activePeriod'][0]['start'])
        packet = {
            'id':id
            , 'start': datetime.datetime.fromtimestamp(int(alert['activePeriod'][0]['start']))
        }
        for k,v in packet.items():
            dataset[k].append(v)
            
    df = pd.DataFrame.from_dict(dataset)   


#MAX and Min of Dataset
"""
datetime.datetime(2022, 6, 22, 22, 2)
, datetime.datetime(2022, 6, 24, 20, 0)
, datetime.datetime(2022, 6, 30, 22, 0)
, datetime.datetime(2022, 6, 20, 19, 0)
, datetime.datetime(2022, 6, 27, 7, 0)
, datetime.datetime(2022, 6, 24, 20, 0)
, datetime.datetime(2022, 7, 10, 19, 0)
, datetime.datetime(2022, 7, 2, 2, 0)
, datetime.datetime(2022, 6, 6, 5, 0)
, datetime.datetime(2022, 7, 3, 0, 0)
, datetime.datetime(2022, 6, 27, 10, 0)
, datetime.datetime(2022, 4, 26, 4, 0)
, datetime.datetime(2022, 6, 13, 4, 0)
, datetime.datetime(2022, 5, 30, 2, 0)
, datetime.datetime(2022, 5, 23, 0, 1)
, datetime.datetime(2021, 11, 22, 12, 0)
, datetime.datetime(2022, 5, 23, 4, 0)
, datetime.datetime(2022, 4, 4, 4, 0)
, datetime.datetime(2022, 4, 14, 8, 17, 53)
, datetime.datetime(2022, 4, 26, 15, 19, 25)
, datetime.datetime(2022, 5, 10, 2, 0)
, datetime.datetime(2022, 5, 11, 4, 0)
, datetime.datetime(2022, 5, 23, 6, 0)]
"""




