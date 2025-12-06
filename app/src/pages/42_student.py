import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

API_URL = "http://web-api:4000/d/data/student"
data = requests.get(API_URL).json()

# Back button
if st.button("← Back"):
    st.switch_page("pages/40_data_A_Home.py")

st.dataframe(data)

