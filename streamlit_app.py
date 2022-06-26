




#google.api_core.exceptions.Forbidden: 403 GET https://storage.googleapis.com/storage/v1/b/20220618-bucket/o/Resources?fields=name&prettyPrint=false: Caller does not have storage.objects.get access to the Google Cloud Storage object.
#https://docs.streamlit.io/knowledge-base/tutorials/databases/gcs

import controller
import model
import streamlit as st

from model import VIEW_Model

from datetime import date

Session_Keys = {
    'APP_STARTED': False
    , 'Total Requests': 0
}

for k,v in Session_Keys.items():
    if k not in st.session_state:
        st.session_state[k] = v

st.title('20220613 - GCP Cloud Storage')

st.write(st.session_state)
st.write(st.secrets['gcp_service_account']["client_email"])

OVERVIEW = st.container()
OVERVIEW.text(VIEW_Model['ContactInfo'])
OVERVIEW.text(VIEW_Model['OVERVIEWText0'])

STEP1 = st.container()
STEP1.write(VIEW_Model['STEP1Text0'])
START_CONTAINER = STEP1.empty()

def BUTTON_START():
    global model
    model.Model_Init(st.secrets['gcp_service_account'])
    model.Resources = controller.App_Init(model.Resources, model.GCP)
    model.Resources = model.GCP_Push(model.GCP, model.Resources)
    st.session_state['APP_STARTED'] = True

if st.session_state['APP_STARTED']:
    START_CONTAINER.empty()
else:
    START_CONTAINER.button('Start!', on_click=BUTTON_START)

STEP2 = st.container()
if st.session_state['APP_STARTED']:
    STEP2.write(VIEW_Model['STEP2Text0'])
    Session_Keys['Total Requests'] = controller.Count_Requests(date.today(), model)
    STEP2.markdown(f"**Total pull requests made today = {Session_Keys['Total Requests']}**")

def BUTTON_PULL():
    global model
    model.Resources = controller.API_Pull(model.Resources, model.Info)
    Session_Keys['Total Requests'] = controller.Count_Requests(date.today(), model)
    model.Resources = model.GCP_Push(model.GCP, model.Resources)
    STEP2.write(model.Resources)

PULL_CONTAINER = STEP2.empty()
PULL_CONTAINER.button('Call API!', on_click=BUTTON_PULL)
if Session_Keys['Total Requests'] > model.Info['API_CAP']:
    PULL_CONTAINER.empty()
    PULL_CONTAINER.write('Maximum pull requests reached, please try again tomorrow')

# #def UNPICKLE_JSON(Container):
# #    try:
# #        st.session_state['API_JSON'] = controller.Unpickle_JSON()
# #        Container.write(str(st.session_state['API_JSON']))
# #    except Exception as e:
# #        Container.error(e)
# #JSON_SAMPLE.button('SHOW ME!', on_click=UNPICKLE_JSON, args=(JSON_SAMPLE, ))


