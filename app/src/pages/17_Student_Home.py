import streamlit as st
from modules.nav import SideBarLinks


st.set_page_config(layout="wide")
SideBarLinks()


first_name = st.session_state.get("first_name", "Student")


st.title(f"Welcome, {first_name}")
st.write("What do you want to do today?")


if st.button("View & manage my degree plans", type="primary", use_container_width=True):
   st.switch_page("pages/31_Student_Plans.py")


if st.button("Search courses", type="primary", use_container_width=True):
   st.switch_page("pages/24_Course_Search.py")

