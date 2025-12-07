import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

# Get professor id from session (fallback to 501 while testing)
prof_id = st.session_state.get("user_id", 501)

st.title("My Sections")

term = st.selectbox("Select term", ["All", "Fall 2025", "Spring 2026"])

base_api = "http://web-api:4000" 
url = f"{base_api}/prof/professors/{prof_id}/sections"

resp = requests.get(url)

if resp.status_code != 200:
    st.error(f"Could not load sections. Status {resp.status_code}")
else:
    sections = resp.json()
    
    if not sections:
        st.info("You are not teaching any sections in this dataset.")
    else:
        # Filter by selected term
        if term != "All":
            sections = [s for s in sections if s.get('semester') == term or s.get('term') == term]
        
        if not sections:
            st.info(f"No sections found for {term}.")
        else:
            st.table(sections)