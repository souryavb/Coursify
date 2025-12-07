import streamlit as st
import requests
from modules.nav import SideBarLinks


st.set_page_config(layout="wide")
SideBarLinks()


st.title("Find Courses")


BASE_URL = "http://localhost:4000"


# --- Filters ---
col1, col2, col3 = st.columns(3)


with col1:
   subject = st.text_input("Subject prefix (e.g. CS, MA)", value="CS")


with col2:
   level = st.selectbox(
       "Course level",
       ["Any", "1000", "2000", "2500", "3000", "4000"],
       index=1,
   )


with col3:
   credits_choice = st.selectbox("Credits", ["Any", 1, 2, 3, 4, 5])


search = st.text_input("Search in course name/description", value="")
semester = st.selectbox("Semester offered", ["Any", "Fall", "Spring", "Summer"], index=1)
status = st.selectbox("Status", ["Any", "Active", "Inactive"], index=1)


if st.button("Search"):
   params = {}


   if subject.strip():
       params["subject"] = subject.strip().upper()
   if level != "Any":
       params["level"] = level
   if credits_choice != "Any":
       params["credits"] = credits_choice
   if search.strip():
       params["search"] = search.strip()
   if semester != "Any":
       params["semester"] = semester
   if status != "Any":
       params["status"] = status


   try:
       # NOTE: /c prefix
       resp = requests.get(f"{BASE_URL}/c/courses", params=params)
   except requests.exceptions.RequestException as e:
       st.error(f"Error contacting API: {e}")
   else:
       if resp.status_code != 200:
           st.error(f"Could not load courses. Status {resp.status_code}")
       else:
           data = resp.json()
           if not data:
               st.info("No courses match those filters.")
           else:
               st.subheader("Matching courses")
               st.dataframe(data)


               course_ids = [row["courseID"] for row in data]
               selected_id = st.selectbox(
                   "Select a course to view details",
                   course_ids,
               )


               if st.button("View course details"):
                   st.session_state["selected_course_id"] = selected_id
                   st.switch_page("pages/25_Course_Detail.py")







