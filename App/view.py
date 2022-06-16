#Need to create APP Metadata data, then can make sure pull request is only done once per a day.

import controller
import streamlit as st

st.title('20220615 - GCP Cloud Storage')
st.subheader('Pulling data from NSW Transport API and storing it on GCP')

OVERVIEW = st.container()
ContactDetails = (
    'Author: Mick Hua \n'
    'Linkedin: https://www.linkedin.com/in/mick-hua-353353a/ \n'
    'github: https://github.com/HuaMick/20220609 \n'
    )

OVERVIEW.text(ContactDetails)
OVERVIEW.subheader('Project Overview')

Objectives = (
    'Objectives: \n'
    '- Pull alerts from Transport NSW API \n'
    '- Store the data on GCP Cloud Storage'
    )
OVERVIEW.text(Objectives)

STEP1 = st.container()
STEP1.subheader('Application Metadata')
ContainerText1 = (
    'The API Only takes a limited number of requests. \n'
    'I do not want a user spamming the request button \n'
    'so want to limit the requests to once per a day \n'
    'Will need to store the metadata outside the application \n'
    'so that it persists beyound the browser session \n'
    'To do this will create a application metadata file \n'
    'Can store this file onto GCP Cloud Storage \n'
    'It can be the first thing the application pulls from GCP Cloud \n'
    )
STEP1.text(ContainerText1)

ContainerText2 = (
    'I have created a python module to manage the data operations and called it model \n'
    'model is a standard name from the model view controller design pattern \n'
    'in model we can define a dataframe to store all the app data \n'
    )
STEP1.text(ContainerText2)

ContainerCode1 = (
    """
    App_Model = {}
    App_Model['GCP_Bucket_Name'] = '20220615-datastore'
    App_Model['GCP_Client'] = storage.Client()
    App_Model['GCP_Bucket'] = App_Model['GCP_Client'].bucket(App_Model['GCP_Bucket_Name'])
    App_Model['Metadata'] = {'DateOfLastAPIRequest':None}
    """
)
STEP1.code(ContainerCode1, language='python')

ContainerText3 = (
    """
    We can then create a function to pickle the App_Model and check if it exists \n
    in GCP, if it does we pull it, if it doesnt we can store a new one.
    """
    )
STEP1.text(ContainerText3)

ContainerCode2 = (
    """
    
    """
)

STEP1.code(ContainerCode2, language='python')



STEP2 = st.container()
STEP2.subheader('Pull our API Data')

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
STEP99.text(Step1Text)
STEP99.code('pip install --upgrade google-cloud-storage')



