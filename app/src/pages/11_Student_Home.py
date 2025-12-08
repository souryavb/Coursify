import streamlit as st
from modules.nav import SideBarLinks
import datetime


st.set_page_config(layout="wide")
SideBarLinks()

#------------------ Back Button ------------------
if st.button("← Back"):
    st.switch_page("Home.py")
#------------------ Back Button ------------------

# Get user info
first_name = st.session_state.get("first_name", "Student")

# Get current time for greeting
current_hour = datetime.datetime.now().hour
if current_hour < 12:
    greeting = "Good morning"
elif current_hour < 18:
    greeting = "Good afternoon"
else:
    greeting = "Good evening"

# Header with personalized greeting
st.markdown(f"# {greeting}, {first_name}! 👋")
st.markdown("### Let's make progress on your academic journey today")

st.markdown("---")

# Quick Actions Section
st.markdown("## 🎯 Quick Actions")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown("### 📚 My Degree Plans")
        st.write("View and manage your academic plans, track your progress, and plan future semesters.")
        if st.button("Manage My Plans", type="primary", use_container_width=True, key="plans_btn"):
            st.switch_page("pages/12_Student_Plans.py")

with col2:
    with st.container(border=True):
        st.markdown("### 🔍 Course Search")
        st.write("Browse courses, check prerequisites, and find classes that fit your schedule and interests.")
        if st.button("Search Courses", type="primary", use_container_width=True, key="search_btn"):
            st.switch_page("pages/14_Course_Search.py")

st.markdown("---")

# Tips & Reminders Section
st.markdown("## 💡 Tips & Reminders")

col3, col4, col5 = st.columns(3)

with col3:
    st.info("""
    **📅 Plan Ahead**
    
    Review course prerequisites before registration to ensure you're on track!
    """)

with col4:
    st.success("""
    **✅ Stay Organized**
    
    Keep your degree plans updated to visualize your path to graduation.
    """)

with col5:
    st.warning("""
    **⏰ Important Dates**
    
    Check registration deadlines and add/drop dates for your semester.
    """)

st.markdown("---")

# Additional resources or stats (optional)
st.markdown("## 📊 At a Glance")
stats_col1, stats_col2, stats_col3 = st.columns(3)

with stats_col1:
    st.metric(label="Current Semester", value="Fall 2024", delta=None)

with stats_col2:
    st.metric(label="Year Standing", value="Sophomore", delta=None)

with stats_col3:
    st.metric(label="Credits Completed", value="45", delta="+15")