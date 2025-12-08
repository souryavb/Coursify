import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About this App")

st.markdown(
    """
    **Coursify** is a course planning and academic roadmap platform designed to transform the way students and universities approach degree planning. Students are often left to plan their entire college education using spreadsheets and scattered course catalogs, a process that is inefficient, stressful, and error-prone. Coursify replaces that uncertainty with an interactive, data-driven planning experience.

    With Coursify, students can build, save, and compare multi-year academic plans, helping them visualize their path to graduation with confidence. At the same time, universities gain insight into future course demand as students save their plans, allowing departments to better allocate resources, schedule enough sections, and support student success at scale.

    This application serves as the **Database Design Project for CS 3200 – Fall 2025**, demonstrating the use of relational database systems, API integration, and data-driven application design through a real-world academic planning platform.
    """
)

# Add a button to return to home page
if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")
