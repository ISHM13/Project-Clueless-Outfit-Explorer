import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Business Client Page')

st.write('\n\n')
st.write('## Business Client Management')

if st.button("Business Client Profile", 
            type = 'primary', 
            use_container_width=True):
  st.switch_page('pages/27_Client_Prof.py')

if st.button("Add Business Client", 
            type = 'primary', 
            use_container_width=True):
  st.switch_page('pages/28_Add_Client.py')