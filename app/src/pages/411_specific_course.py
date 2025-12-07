import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks
import plotly.express as px

st.set_page_config(layout="wide")
SideBarLinks()

# Check if a course was selected
if 'selected_course_id' not in st.session_state:
    st.warning("No course selected. Please go back and select a course.")
    if st.button("← Back to Courses"):
        st.switch_page("pages/41_courses.py")
    st.stop()

course_id = st.session_state['selected_course_id']

# Back button
if st.button("← Back to Course List"):
    st.switch_page("pages/41_courses.py")

st.title("📖 Course Details")

API_URL = f"http://web-api:4000/d/data/course/{course_id}"


response = requests.get(API_URL)
response.raise_for_status()
data = response.json()

if data:
    course = data[0]
    
    # Display course header
    st.header(f"{course['course_name']}")
    st.subheader(f"Department: {course['deptName']}")
    
    # Display metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Enrolled", course['total_enrolled'])
    
    with col2:
        st.metric("Completed", course['completed'])
    
    with col3:
        st.metric("Dropped", course['dropped'])
    
    with col4:
        st.metric("Completion Rate", f"{course['completion_rate']}%")
    
    # Create visualizations
    st.write("---")
    st.subheader("📊 Enrollment Statistics")
    
    # Pie chart for enrollment status
    
    enrollment_data = pd.DataFrame({
        'Status': ['Completed', 'Dropped', 'Active'],
        'Count': [
            course['completed'],
            course['dropped'],
            int(course['total_enrolled']) - int(course['completed']) - int(course['dropped'])
        ]
    })
    
    fig = px.pie(enrollment_data, values='Count', names='Status', 
                title='Enrollment Status Distribution')
    st.plotly_chart(fig)
    
else:
    st.error(f"No data found for course ID: {course_id}")
    