
import model
import requests

from datetime import date

def API_Request(App_Model):
    Request = {}
    Request['Request_URL'] = 'https://api.transport.nsw.gov.au/v2/gtfs/alerts/buses?format=json'
    
    if App_Model['DateOfLastAPIRequest'] == date.today():
        Request['Status'] = 'Fail'
        Request['Description'] = 'You can only make 1 request per a day'
        Request['Payload'] = None
        
        return Request
    else:
        Response = requests.get(Request['Request_URL'], headers={
            'Authorization': 'apikey rG3uaQgSxI8LbkMvtwS9fp61tZdQmxDOcqNj'})
        Request['Status'] = 'Pass'
        Request['Description'] = ''
        Request['Payload'] = Response

        App_Model['DateOfLastAPIRequest'] = date.today()
        model.StoreAppModel(App_Model)
        
        return Request


API_Request(model.App_Model)




def TNSW_API_request():
    response = requests.get(
    'https://api.transport.nsw.gov.au/v2/gtfs/alerts/buses?format=json'
    , headers={'Authorization': 'apikey rG3uaQgSxI8LbkMvtwS9fp61tZdQmxDOcqNj'})
    return response.json()

