import streamlit as st
import requests
from modules.nav import SideBarLinks


st.set_page_config(layout="wide")
SideBarLinks()

#------------------ Back Button ------------------
if st.button("← Back"):
    st.switch_page("pages/14_Course_Search.py")
#-------------------------------------------------

BASE_URL = "http://web-api:4000"

st.title("Course Details")


# Get list of all courses for dropdown
@st.cache_data
def get_all_courses():
    try:
        # Try with /c/ prefix first (based on your course_routes.py)
        resp = requests.get(f"{BASE_URL}/c/courses", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if data:
                return data
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {e}")
    return []


courses_list = get_all_courses()

if not courses_list:
    st.warning("Could not load course list. Please enter a course ID manually.")
    course_id_str = st.text_input("Course ID")
    if not course_id_str.strip():
        st.info("Enter a course ID.")
        st.stop()
    try:
        course_id = int(course_id_str)
    except ValueError:
        st.error("Course ID must be an integer.")
        st.stop()
else:
    # Check if we have a preselected course from the search page
    preselected = st.session_state.get("selected_course_id")
    
    # Create display options for dropdown
    course_display_options = {
        row["courseID"]: f"{row['courseID']} - {row['course_name']}"
        for row in courses_list
    }
    
    course_ids = [row["courseID"] for row in courses_list]
    
    # Find the index of the preselected course, or default to 0
    default_index = 0
    if preselected and preselected in course_ids:
        default_index = course_ids.index(preselected)
    
    course_id = st.selectbox(
        "Select a course",
        options=course_ids,
        format_func=lambda x: course_display_options[x],
        index=default_index,
    )


# Auto-load course details (either when button is clicked OR when navigating from search page)
load_course = st.button("Load course") or preselected is not None

if load_course:
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


    st.subheader(f"{course['courseID']} — {course['course_name']}")
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