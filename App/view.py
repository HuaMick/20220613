#Need to create APP Metadata data, then can make sure pull request is only done once per a day.

from re import L
import controller
import model
from model import VIEW_Model
import streamlit as st

st.title('20220615 - GCP Cloud Storage')

OVERVIEW = st.container()
OVERVIEW.text(VIEW_Model['ContactInfo'])

st.subheader('Pulling data from NSW Transport API and storing it on GCP')

STEP1 = st.container()
STEP1.text(VIEW_Model['STEP1Text0'])
STEP1.text(VIEW_Model['STEP1Text1'])
STEP1.text(VIEW_Model['STEP1Text2'])
STEP1.code(VIEW_Model['STEP1Code1'], language='python')
STEP1.text(VIEW_Model['STEP1Text3'])
STEP1.code(VIEW_Model['STEP1Code2'], language='python')

#Initate the App Model
App_Model = model.InitiateAppModel(model.GCP_Model, model.App_Model)

STEP1.text(VIEW_Model['STEP1Text4'])
STEP1.write(App_Model)

STEP2 = st.container()
STEP2.text(VIEW_Model['STEP2Text0'])
STEP2.code(VIEW_Model['STEP2Code0'])

#Pull The API Data
if 'API_Response' not in st.session_state:
    st.session_state['API_Response'] = None

def Button_Request(App_Model):
    st.session_state['API_Response'] = controller.API_Request(App_Model)
    STEP2.write(st.session_state['API_Response'])

STEP2.button('Request API Data!', on_click=Button_Request, args=(App_Model, ))



#def UNPICKLE_JSON(Container):
#    try:
#        st.session_state['API_JSON'] = controller.Unpickle_JSON()
#        Container.write(str(st.session_state['API_JSON']))
#    except Exception as e:
#        Container.error(e)
#JSON_SAMPLE.button('SHOW ME!', on_click=UNPICKLE_JSON, args=(JSON_SAMPLE, ))

STEP99 = st.container()
STEP99.subheader('Setting Up GCP Cloud Storage')
Step1Overview = (
    'We want to use Cloud Storage as it has a free tier \n'
    'Note: Was orginally looking at Cloud SQL but there is no free tier \n'
    'Might be able to setup a E2 Virtual Machine and host a small database on there \n'
    'However will try with cloud storage first. ' 
    'Might even be able to store a SQLite database here..'
    )
STEP99.write(Step1Overview)

Step99Text = (
    'First we want to setup a cloud storage bucket. \n'
    'Its No SQL so these buckets literally just store files \n'
    'Once we have the bucket setup we need to setup a service account \n'
    'We can allocate the service account permissions to our bucket \n'
    'Then we can generate a key for the service account,\n'
    'this is just a json file that we can download to our local machine'
)
STEP99.text(Step99Text)
STEP99.code('pip install --upgrade google-cloud-storage')



