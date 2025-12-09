import logging
logger = logging.getLogger(__name__)


import streamlit as st
from modules.nav import SideBarLinks
import requests


st.set_page_config(layout = 'wide')


SideBarLinks()


st.title('System Admin Home Page')


if st.button('Update ML Models',
            type='primary',
            use_container_width=True):
 st.switch_page('pages/21_ML_Model_Mgmt.py')


if st.button('Manage Data Quality Issues',
            type='primary',
            use_container_width=True):
   st.switch_page('pages/31_DataQualityIssue.py')


if st.button('Edit System Settings',
            type='primary',
            use_container_width=True):
   st.switch_page('pages/32_SystemSettings.py')