import streamlit as st
import requests
from modules.nav import SideBarLinks


st.set_page_config(layout="wide")
SideBarLinks()


BASE_URL = "http://localhost:4000"


st.title("Course Details")


preselected = st.session_state.get("selected_course_id")
default_text = str(preselected) if preselected is not None else ""


course_id_str = st.text_input("Course ID", value=default_text)
if not course_id_str.strip():
   st.info("Enter a course ID or navigate here from the course search page.")
   st.stop()


try:
   course_id = int(course_id_str)
except ValueError:
   st.error("Course ID must be an integer.")
   st.stop()


if st.button("Load course"):
   # ---- Course core info ----
   try:
       resp = requests.get(f"{BASE_URL}/c/courses/{course_id}")
   except requests.exceptions.RequestException as e:
       st.error(f"Error contacting API: {e}")
       st.stop()


   if resp.status_code == 404:
       st.error("Course not found.")
       st.stop()
   elif resp.status_code != 200:
       st.error(f"Error fetching course. Status {resp.status_code}")
       st.stop()


   course = resp.json()


   st.subheader(f"{course['courseID']} – {course['course_name']}")
   col1, col2, col3 = st.columns(3)


   with col1:
       st.metric("Credits", course["credits"])
       st.write(f"**Status:** {course['Status']}")


   with col2:
       st.write(f"**Semesters offered:** {course['semesters_offered']}")
       st.write(f"**Department ID:** {course['deptID']}")


   with col3:
       st.write(f"**Department name:** {course.get('deptName', 'N/A')}")


   st.write("### Description")
   st.write(course["description"])


   # ---- Requirements ----
   st.write("### Requirements / Requisites")


   try:
       req_resp = requests.get(f"{BASE_URL}/c/courses/{course_id}/requirements")
   except requests.exceptions.RequestException as e:
       st.error(f"Error contacting API for requirements: {e}")
       st.stop()


   if req_resp.status_code == 404:
       st.info("No requirements found for this course.")
   elif req_resp.status_code != 200:
       st.error(f"Error fetching requirements. Status {req_resp.status_code}")
   else:
       req_data = req_resp.json()
       reqs = req_data.get("requirements", [])
       if not reqs:
           st.info("No requirements defined for this course.")
       else:
           st.table(reqs)

