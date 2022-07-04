# pip install --upgrade google-cloud-storage
import datetime
from datetime import date
from urllib.request import Request
from google.cloud import storage
from google.oauth2 import service_account

import toml
import pickle

Info = {}
Info['AppName'] = '20220613'
Info['API_CAP'] = 10

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

VIEW_Model={}
VIEW_Model['ContactInfo'] = ("""

Author: Mick Hua
Linkedin: https://www.linkedin.com/in/mick-hua-3    53353a/
github: https://github.com/HuaMick/20220609

""")
VIEW_Model['OVERVIEWText0'] = ("""
This is a learning project to experiment with Googlce Cloud Platform
(GCP) Cloud Storage. Cloud Storage is a no-sql datastore that has a
generous free tier.
""")

VIEW_Model['STEP1Text0'] = ("""
To Start Press the Start Button!
""")

VIEW_Model['STEP1Text1'] = ("""
The start button authenticates with GCP cloud using Streamlit's 
secrets manager. GCP will generate a secrets file when you register
you can pass the contents of this secrets file to the GCP library.
""")

VIEW_Model['STEP1Code0'] = ("""
credentials = service_account.Credentials.from_service_account_info(Secrets)
GCP['GCP_Client'] = storage.Client(credentials=credentials)
""")

VIEW_Model['STEP1Text2'] = ("""
Once authenticated the app will
1. Check if a resources file exists on GCP Cloud Storage
2. Initate a pull request if found, else create a new one
3. Push the existing or new one back to GCP 
4. Delete the start button (so trolls don't keep clicking it)
""")

VIEW_Model['STEP1Text3'] = ("""
Heres a Chart showing the number of PULL and PUSH requests we have
made to the GCP API.
""")

VIEW_Model['STEP2Text0'] = ("""
Of course we want to store more on GCP, so we can also pull data
from the transport of NSW API. Here's a button that does just that.
Note the button won't show if we have made the max number of requests.
""")

VIEW_Model['STEP2Text1'] = ("""
The Pull Button will:
1. Execute an API pull request from transport NSW
2. Store the request in resources file
3. Push the resources file up to GCP
""")

from os.path import exists
#Secrets = (toml.load(".streamlit\secrets.toml"))['gcp_service_account']
#requests = pd.DataFrame({k:v for k,v in Resources['GCP'].items() if k in ['RequestDate', 'RequestType']})
def Model_Init(Secrets):
    global GCP
    credentials = service_account.Credentials.from_service_account_info(Secrets)
    GCP['GCP_Client'] = storage.Client(credentials=credentials)
    GCP['GCP_BucketName'] = '20220618-bucket'
    GCP['GCP_Bucket'] = GCP['GCP_Client'].bucket(GCP['GCP_BucketName'])

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





# VIEW_Model['STEP1Text1'] = ("""
# API has request limits so we want to limit requestst to Once a Day
# """)