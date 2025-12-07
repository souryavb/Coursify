import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

# Back button
if st.button("← Back"):
    st.switch_page("pages/40_data_A_Home.py")

st.title("📚 Course Catalog")

API_URL = "http://web-api:4000/d/data/course"


response = requests.get(API_URL)
response.raise_for_status()
data = response.json()

if data:
    df = pd.DataFrame(data)
    
    # Add filters
    col1, col2 = st.columns(2)
    with col1:
        search = st.text_input("🔍 Search courses")
    with col2:
        departments = ["All"] + sorted(df['deptName'].unique().tolist())
        selected_dept = st.selectbox("Filter by Department", departments)
    
    # Filter data
    filtered_df = df.copy()
    if search:
        filtered_df = filtered_df[filtered_df['course_name'].str.contains(search, case=False, na=False)]
    if selected_dept != "All":
        filtered_df = filtered_df[filtered_df['deptName'] == selected_dept]
    
    # Display courses as clickable cards
    st.write(f"### Showing {len(filtered_df)} courses")
    
    for _, row in filtered_df.iterrows():
        col1, col2, col3 = st.columns([3, 2, 1])
        
        with col1:
            st.write(f"**{row['course_name']}**")
            st.caption(row['deptName'])
        
        with col2:
            st.write(f"Credits: {row['credits']}")
        
        with col3:
            # Button to view course details
            if st.button("View Details", key=f"course_{row['courseID']}"):
                st.session_state['selected_course_id'] = row['courseID']
                st.switch_page("pages/411_specific_course.py")
        
        st.divider()
else:
    st.warning("No course data available")
    
