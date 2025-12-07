import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import pandas as pd

API_URL = "http://web-api:4000/d/data/professor"

# Back button
if st.button("← Back"):
    st.switch_page("pages/40_data_A_Home.py")

response = requests.get(API_URL)
response.raise_for_status()
data = response.json()

options = ["Total Ratings", "Highest rated"]

if data:

    df = pd.DataFrame(data)

    st.header("Professor Ratings 👨‍🏫")
    col1, = st.columns(1)
    with col1:
        sort_option = st.selectbox("Sort by", options)

    if sort_option == "Total Ratings":
        df = df.sort_values('total_ratings', ascending=False)
    if sort_option == "Highest rated":
        df = df.sort_values('average_rating', ascending=False)

    for _, prof in df.iterrows():
        # Your display code here
        col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
        
        with col1:
            st.write(f"**{prof['last_name']}**")
        
        with col2:
            st.metric("Avg Rating", f"{float(prof['average_rating']):.2f} ⭐")
        
        with col3:
            st.metric("Total Ratings", int(prof['total_ratings']))
        
        with col4:
            if st.button("View Details", key=f"prof_{prof['profID']}"):
                st.session_state['selected_prof_id'] = prof['profID']
                st.switch_page("pages/431_specific_prof.py")
        
        st.divider()
    
else:
    st.warning("No professor data available")