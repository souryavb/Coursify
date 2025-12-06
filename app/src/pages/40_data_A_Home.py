import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Data Analyst Home Page')

if st.button('View Course data', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/41_courses.py')

if st.button('View Student data', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/42_student.py')

if st.button('View Professors data', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/43_professor.py')