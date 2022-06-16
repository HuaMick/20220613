
import requests

def TNSW_API_request():
    response = requests.get(
    'https://api.transport.nsw.gov.au/v2/gtfs/alerts/buses?format=json'
    , headers={'Authorization': 'apikey rG3uaQgSxI8LbkMvtwS9fp61tZdQmxDOcqNj'})
    return response.json()

