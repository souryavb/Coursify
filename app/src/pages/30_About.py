import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

st.set_page_config(layout="wide", page_title="About Coursify")
SideBarLinks()

#------------------ Back Button ------------------
if st.button("← Back"):
    st.switch_page("Home.py")
#-------------------------------------------------

# Header
st.markdown("# About Coursify 🎓")
st.markdown("---")

# Main description
st.markdown("## What is Coursify?")
st.write("""
Coursify is a course planning and academic roadmap platform designed to transform the way students 
and universities approach degree planning. Students are often left to plan their entire college 
education using spreadsheets and scattered course catalogs, a process that is inefficient, stressful, 
and error-prone. Coursify replaces that uncertainty with an interactive, data-driven planning experience.
""")

st.markdown("## Key Features")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown("### 👨‍🎓 For Students")
        st.write("""
        - Build, save, and compare multi-year academic plans
        - Visualize your path to graduation with confidence
        - Check prerequisites and course requirements
        - Search and explore courses easily
        - Plan semester-by-semester schedules
        """)

with col2:
    with st.container(border=True):
        st.markdown("### 🏫 For Universities")
        st.write("""
        - Gain insight into future course demand
        - Better allocate resources and schedule sections
        - Support student success at scale
        - Data-driven decision making
        - Track degree program requirements
        """)

st.markdown("---")

# Project context
st.markdown("## 📚 About This Project")
with st.container(border=True):
    st.info("""
    This application serves as the **Database Design Project for CS 3200 - Fall 2025**, demonstrating 
    the use of relational database systems, API integration, and data-driven application design through 
    a real-world sample of an academic planning platform.
    """)

st.markdown("---")

# Technology stack
st.markdown("## 🛠️ Built With")
tech_col1, tech_col2, tech_col3 = st.columns(3)

with tech_col1:
    st.markdown("**Frontend**")
    st.write("- Streamlit")
    st.write("- Python")

with tech_col2:
    st.markdown("**Backend**")
    st.write("- Flask REST API")
    st.write("- MySQL Database")

with tech_col3:
    st.markdown("**Infrastructure**")
    st.write("- Docker")

st.markdown("---")

# Return button
if st.button("← Return to Home", type="primary", use_container_width=False):
    st.switch_page("Home.py")