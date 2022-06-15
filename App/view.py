import streamlit as st

st.title('20220615 - GCP Cloud Storage')
st.subheader('Pulling data from NSW Transport API and storing it on GCP')

OVERVIEW = st.container()
contact_details = (
    'Author: Mick Hua \n'
    'Linkedin: https://www.linkedin.com/in/mick-hua-353353a/ \n'
    'github: https://github.com/HuaMick/20220609 \n'
    )

OVERVIEW.text(contact_details)
OVERVIEW.subheader('Project Overview')

Objectives = (
    'Objectives: \n'
    '- Pull alerts from Transport NSW API \n'
    '- Store the data on GCP Cloud Storage'
    )
OVERVIEW.text(Objectives)

STEP1 = st.container()

pip install --upgrade google-cloud-storage

