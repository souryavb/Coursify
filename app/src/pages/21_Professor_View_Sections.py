import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

# Get professor id from session (fallback to 501 while testing)
prof_id = st.session_state.get("user_id", 501)

st.title("My Sections")

# (Optional) you can leave this here for later, but we won’t use it in the URL yet
term = st.selectbox("Select term", ["All", "Fall 2025", "Spring 2026"])

# SIMPLE: no term filter in backend yet
base_api = "http://web-api:4000"  # service name, not localhost
url = f"{base_api}/prof/professors/{prof_id}/sections?term={term}"

resp = requests.get(url)

if resp.status_code != 200:
    st.error(f"Could not load sections. Status {resp.status_code}")
else:
    sections = resp.json()
    if not sections:
        st.info("You are not teaching any sections in this dataset.")
    else:
        st.table(sections)