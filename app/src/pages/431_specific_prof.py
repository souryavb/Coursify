import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks


prof_id = st.session_state['selected_prof_id']



API_URL = f"http://web-api:4000/d/data/professor/{prof_id}"
data = requests.get(API_URL).json()

prof = data[0]


# Back button
if st.button("← Back"):
    st.switch_page("pages/43_professor.py")

full_name = f"{prof['first_name']} {prof['last_name']}"

st.header(f"Ratings for {full_name} 👨‍🏫")

# display data

if prof:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("⭐ Rating", f"{prof['ratings']}")
    
    with col2:
        st.write("**💬 Comment**")
        st.write(prof['comment'])
    
    with col3:
        st.write("**📅 Time**")
        st.write(prof['rating_time'])
    
    st.divider()