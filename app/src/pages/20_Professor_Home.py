import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

# TEMP: hard-code user for demo so other pages work
if "user_id" not in st.session_state:
    st.session_state["user_id"] = 501
if "first_name" not in st.session_state:
    st.session_state["first_name"] = "Amelia"

st.title(f"Welcome Professor, {st.session_state.get('first_name', '')}.")
st.write("### What would you like to do today?")

if st.button("View My Sections", type='primary', use_container_width=True):
    st.switch_page("pages/21_Professor_View_Sections.py")

if st.button("View Override Requests", type='primary', use_container_width=True):
    st.switch_page("pages/22_Professor_View_Override_Requests.py")