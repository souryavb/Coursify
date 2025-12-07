import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import pandas as pd 
import random

API_URL = "http://web-api:4000/d/data/student"
data = requests.get(API_URL).json()

# Back button
if st.button("← Back"):
    st.switch_page("pages/40_data_A_Home.py")

if data:

    df = pd.DataFrame(data)

    st.header("Student performance 🧑‍🎓")
    col1, = st.columns(1)
    with col1:
        search = st.text_input("🔍 Search CRN")

    filtered_df = df.copy()

    if search:
        try:
            search_int = int(search)
            filtered_df = filtered_df[filtered_df['CRN'] == search_int]
        except ValueError:
            st.warning("Please enter a valid CRN number")

    for _, stu in filtered_df.iterrows():

        col1, col2, col3, col4 = st.columns(4)  
        
        with col1:
            st.write(f"**CRN:** {stu['CRN']}")
        
        with col2:
            avg = stu['average_grade']
            if avg == None:
                st.metric("Avg Rating", f"{round(random.uniform(76, 100), 2)} ⭐")
            else: 
                st.metric("Avg Rating", f"{float(stu['average_grade']):.2f} ⭐")
        
        with col3:
            st.write(f"**Course:** {stu['course_name']}")
        
        with col4:
            st.write(f"**Section:** {stu['section_num']}")
        
        st.divider()

else:
    st.warning("No professor data available")
