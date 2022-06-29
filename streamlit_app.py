#google.api_core.exceptions.Forbidden: 403 GET https://storage.googleapis.com/storage/v1/b/20220618-bucket/o/Resources?fields=name&prettyPrint=false: Caller does not have storage.objects.get access to the Google Cloud Storage object.
#https://docs.streamlit.io/knowledge-base/tutorials/databases/gcs

import controller
import model
import streamlit as st
import pandas as pd
import plotly.express as px

from model import VIEW_Model

from datetime import date

Session_Keys = {
    'GCP': None 
    , 'Resources': None
    , 'APP_STARTED': False
    , 'Total Requests': 0
}

for k,v in Session_Keys.items():
    if k not in st.session_state:
        st.session_state[k] = v

#st.set_page_config(layout="wide")
st.title('20220613 - GCP Cloud Storage')
#st.write(st.session_state)

OVERVIEW = st.container()
OVERVIEW.text(VIEW_Model['ContactInfo'])
OVERVIEW.text(VIEW_Model['OVERVIEWText0'])

STEP1 = st.container()
STEP1.write(VIEW_Model['STEP1Text0'])
STEP1.code(VIEW_Model['STEP1Code0'],language='python')
STEP1.write(VIEW_Model['STEP1Text1'])
START_CONTAINER = STEP1.empty()

def BUTTON_START():
    global model
    st.session_state['Resources'] = model.Resources
    model.Model_Init(st.secrets['gcp_service_account'])
    st.session_state['Resources'] = controller.App_Init(st.session_state['Resources'], model.GCP)
    st.session_state['Resources'] = model.GCP_Push(model.GCP, model.Resources)
    st.session_state['GCP'] = model.GCP
    st.session_state['APP_STARTED'] = True
    
if st.session_state['APP_STARTED']:
    START_CONTAINER.empty()
else:
    START_CONTAINER.button('Start!', on_click=BUTTON_START)

STEP2 = st.container()
#STEP2.write(st.session_state['Resources'])
#STEP2.write({k:v for k,v in st.session_state['Resources']['API'].items() if k in ['RequestDate', 'RequestType']})
#STEP2.write(pd.DataFrame({k:v for k,v in st.session_state['Resources']['API'].items() if k in ['RequestDate', 'RequestType']}))

if st.session_state['APP_STARTED']:
    STEP2.write(VIEW_Model['STEP2Text0'])
    Session_Keys['Total Requests'] = controller.Count_Requests(date.today(), model)
    STEP2.markdown(f"**Total pull requests made today = {Session_Keys['Total Requests']}**")

def BUTTON_PULL():
    global model
    st.session_state['Resources'] = controller.API_Pull(st.session_state['Resources'], model.Info)
    Session_Keys['Total Requests'] = controller.Count_Requests(date.today(), model)
    st.session_state['Resources'] = model.GCP_Push(model.GCP, st.session_state['Resources'])


PULL_CONTAINER = STEP2.empty()
PULL_CONTAINER.button('Call API!', on_click=BUTTON_PULL)
if Session_Keys['Total Requests'] > model.Info['API_CAP']:
    PULL_CONTAINER.empty()
    PULL_CONTAINER.write('Maximum pull requests reached, please try again tomorrow')

STEP3 = st.container()
if st.session_state['APP_STARTED']:
    requests = pd.DataFrame({k:v for k,v in st.session_state['Resources']['GCP'].items() if k in ['RequestDate', 'RequestType']})
    requests_count = requests.groupby(['RequestDate', 'RequestType'], as_index=False).agg(
        Count=pd.NamedAgg(column='RequestType', aggfunc="count")
    )

    fig = px.bar(requests_count
    , x="RequestDate"
    , y="Count"
    , color="RequestType"
    , barmode="group"
    , title="GCP Requests"
    , width=800
    , height=500)
    fig.update_layout(xaxis = dict(tickfont = dict(size=10)))
    STEP2.write(fig)

# #def UNPICKLE_JSON(Container):
# #    try:
# #        st.session_state['API_JSON'] = controller.Unpickle_JSON()
# #        Container.write(str(st.session_state['API_JSON']))
# #    except Exception as e:
# #        Container.error(e)
# #JSON_SAMPLE.button('SHOW ME!', on_click=UNPICKLE_JSON, args=(JSON_SAMPLE, ))




