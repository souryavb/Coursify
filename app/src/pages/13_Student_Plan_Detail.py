import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

BASE_URL = "http://web-api:4000"

student_id = st.session_state.get("user_id")
plan_id = st.session_state.get("selected_plan_id")

#------------------ Back Button ------------------
if st.button("← Back"):
    st.switch_page("pages/12_Student_Plans.py")
#-------------------------------------------------

st.title("Plan Details")

if student_id is None or plan_id is None:
   st.error("No plan selected. Go back to the 'My Degree Plans' page.")
   st.stop()

student_id = int(student_id)
plan_id = int(plan_id)

def load_plan():
   """GET /s/student<id>/plans/<planID>"""
   try:
       resp = requests.get(f"{BASE_URL}/s/student{student_id}/plans/{plan_id}")
   except requests.exceptions.RequestException as e:
       st.error(f"Error contacting API: {e}")
       return None

   if resp.status_code != 200:
       st.error(f"Could not load plan. Status {resp.status_code}")
       return None

   return resp.json()

plan = load_plan()
if plan is None:
   st.stop()



# ---------- header ----------
col_header, col_delete = st.columns([5, 1])
with col_header:
    st.subheader(f"Plan {plan['planID']}: {plan['plan_name']}")
with col_delete:
    if st.button("🗑️ Delete Plan", type="primary", use_container_width=True, key="delete_button"):
        st.session_state['show_delete_confirmation'] = True
        st.rerun()


# ---------- Delete Confirmation Dialog ----------
if st.session_state.get('show_delete_confirmation', False):
    
    if plan['is_active'] == 1:
        st.error("⚠️ **Cannot delete active plan** - This plan is currently active. Deactivate it first before deletion.")
        
        col_empty, col_close = st.columns([5, 1])
        with col_close:
            if st.button("Close", use_container_width=True):
                st.session_state['show_delete_confirmation'] = False
                st.rerun()
    else:
        st.warning(f"⚠️ **Delete this plan** - This action cannot be undone. Only what-if plans can be deleted. This plan is a what-if scenario and can be safely deleted.")
        
        col_msg, col_buttons = st.columns([3, 2])
        
        with col_msg:
            st.write(f"Deleting: **{plan['plan_name']}** (ID: {plan['planID']})")
        
        with col_buttons:
            btn_col1, btn_col2 = st.columns(2)
            
            with btn_col1:
                if st.button("✅ Confirm", use_container_width=True, key="confirm_delete"):
                    try:
                        resp = requests.delete(
                            f"{BASE_URL}/s/student{student_id}/plans/{plan_id}"
                        )
                    except requests.exceptions.RequestException as e:
                        st.error(f"Error: {e}")
                        st.session_state['show_delete_confirmation'] = False
                        st.rerun()
                    else:
                        if resp.status_code != 200:
                            st.error(f"Could not delete. Status {resp.status_code}")
                            st.session_state['show_delete_confirmation'] = False
                            st.rerun()
                        else:
                            st.success("✅ Plan deleted!")
                            st.session_state['show_delete_confirmation'] = False
                            if "selected_plan_id" in st.session_state:
                                del st.session_state["selected_plan_id"]
                            st.switch_page("pages/12_Student_Plans.py")
            
            with btn_col2:
                if st.button("❌ Cancel", use_container_width=True, key="cancel_delete"):
                    st.session_state['show_delete_confirmation'] = False
                    st.rerun()
    
    st.markdown("---")
#-----------------------

#--- Plan details
col1, col2, col3 = st.columns(3)
with col1:
   st.write(f"**Student ID:** {plan['studentID']}")
   st.write(f"**Program:** {plan['program_name']} ({plan['program_type']})")
with col2:
   st.write(f"**Expected grad:** {plan['expected_grad']}")
   st.write(f"**Created:** {plan['date_created']}")
with col3:
   st.write(f"**Active:** {'Yes' if plan['is_active'] == 1 else 'No'}")


# ---------- toggle active ----------
st.markdown("#### Set plan active / inactive")
new_active = st.radio(
   "Active?",
   options=[0, 1],
   index=1 if plan["is_active"] == 1 else 0,
   format_func=lambda v: "Active" if v == 1 else "What-if (inactive)",
   horizontal=True,
)


if st.button("Update active status"):
   try:
       resp = requests.put(
           f"{BASE_URL}/s/student{student_id}/plans/{plan_id}",
           json={"is_active": new_active},
       )
   except requests.exceptions.RequestException as e:
       st.error(f"Error contacting API: {e}")
   else:
       if resp.status_code != 200:
           st.error(
               f"Could not update plan status. "
               f"Status {resp.status_code}, response: {resp.text}"
           )
       else:
           st.success("Plan status updated.")
           # overwrite header fields from response (no courses in payload)
           updated = resp.json()
           for key in updated:
               if key != "courses":
                   plan[key] = updated[key]

st.markdown("---")

# ---------- current courses by semester ----------
st.subheader("Courses in this plan")

courses = plan.get("courses", [])
if not courses:
   st.info("This plan has no courses yet.")
else:
    # Group courses by semester
    from collections import defaultdict
    courses_by_semester = defaultdict(list)
    
    for course in courses:
        semester = course.get('planned_semester', 'Unscheduled')
        courses_by_semester[semester].append(course)
    
    # Sort semesters chronologically
    sorted_semesters = sorted(courses_by_semester.keys())
    
    # Display each semester as an expandable section
    for semester in sorted_semesters:
        semester_courses = courses_by_semester[semester]
        total_credits = sum(c['credits'] for c in semester_courses)
        
        with st.expander(f"📅 {semester} — {len(semester_courses)} courses, {total_credits} credits", expanded=True):
            st.table(semester_courses)

course_ids_in_plan = [c["courseID"] for c in courses]

st.markdown("---")


# ---------- add new course ----------
st.markdown("### Add a course to this plan")

# Fetch available courses
try:
    # Add filters
    col_filter1, col_filter2 = st.columns(2)
    with col_filter1:
        filter_subject = st.selectbox("Filter by subject", ["All", "CS", "MATH", "DS"], index=0, key="filter_subject")
    with col_filter2:
        filter_semester = st.selectbox("Filter by semester offered", 
                                       ["All", "Fall", "Spring", "Summer"], index=0, key="filter_semester")
    
    # Build query params
    params = {}
    if filter_subject != "All":
        params['subject'] = filter_subject
    if filter_semester != "All":
        params['semester'] = filter_semester
    
    courses_resp = requests.get(f"{BASE_URL}/c/courses", params=params)
    
    if courses_resp.status_code == 200:
        all_courses = courses_resp.json()
        
        if not all_courses:
            st.info("No courses match your filters.")
        else:
            course_options = {
                c['courseID']: f"{c['course_name']} ({c['credits']} credits)"
                for c in all_courses
            }
            
            with st.form("add_course_form", clear_on_submit=True):
                new_course_id = st.selectbox(
                    "Select Course",
                    options=list(course_options.keys()),
                    format_func=lambda x: course_options[x],
                    key="new_course_select"
                )
                
                planned_sem = st.text_input(
                    "Planned semester (e.g. 'Fall 2025')",
                    key="planned_semester_input"
                )
                
                new_status = st.selectbox(
                    "Course status",
                    ["Planned", "In Progress", "Completed", "Dropped"],
                    index=0,
                    key="course_status_select"
                )

                add_submitted = st.form_submit_button("Add course")

                if add_submitted:
                    if not planned_sem.strip():
                        st.error("Planned semester is required.")
                    else:
                        payload = {
                            "courseID": int(new_course_id),
                            "planned_semester": planned_sem.strip(),
                            "course_status": new_status,
                        }
                        
                        try:
                            resp = requests.post(
                                f"{BASE_URL}/p/plans/{plan_id}/courses",
                                json=payload,
                            )
                        except requests.exceptions.RequestException as e:
                            st.error(f"Error contacting API: {e}")
                        else:
                            if resp.status_code != 201:
                                st.error(
                                    f"Could not add course. "
                                    f"Status {resp.status_code}, response: {resp.text}"
                                )
                            else:
                                st.success("✅ Course added to plan successfully!")
                                st.rerun()
    else:
        st.error(f"Could not load courses. Status: {courses_resp.status_code}")
        
except requests.exceptions.RequestException as e:
    st.error(f"Error loading courses: {e}")

st.markdown("---")

# ---------- update / delete existing course ----------
st.markdown("### Update or remove a course in this plan")

if not courses:
   st.info("No courses to manage yet.")
else:
   # Create a mapping of courseID to full course info
   course_display_options = {
       c['courseID']: f"{c['course_name']} - {c['planned_semester']} ({c['course_status']})"
       for c in courses
   }
   
   selected_course = st.selectbox(
       "Select course to manage",
       options=[c['courseID'] for c in courses],
       format_func=lambda x: course_display_options[x],
       key="select_course_to_manage"
   )
   
   # Get the full course object
   selected_course_obj = next(c for c in courses if c['courseID'] == selected_course)

   col_u, col_d = st.columns(2)

   # -- update --
   with col_u:
       st.write("**Update course**")
       new_sem = st.text_input(
           "New planned semester (leave blank to keep the same)",
           key="update_sem",
       )
       new_course_status = st.selectbox(
           "New status (leave as current to keep)",
           ["(no change)", "Planned", "In Progress", "Completed", "Dropped"],
           key="update_status",
       )

       if st.button("Apply update"):
           update_payload = {}
           if new_sem.strip():
               update_payload["planned_semester"] = new_sem.strip()
           if new_course_status != "(no change)":
               update_payload["course_status"] = new_course_status

           if not update_payload:
               st.warning("Nothing to update.")
           else:
               try:
                   resp = requests.put(
                       f"{BASE_URL}/p/plans/{plan_id}/courses/{selected_course}",
                       json=update_payload,
                   )
               except requests.exceptions.RequestException as e:
                   st.error(f"Error contacting API: {e}")
               else:
                   if resp.status_code != 200:
                       st.error(
                           f"Could not update course in plan. "
                           f"Status {resp.status_code}, response: {resp.text}"
                       )
                   else:
                       st.success("✅ Course in plan updated.")
                       st.rerun()

   # -- delete --
   with col_d:
       st.write("**Remove course**")
       if st.button("Delete this course from plan"):
           try:
               resp = requests.delete(
                   f"{BASE_URL}/p/plans/{plan_id}/courses/{selected_course}"
               )
           except requests.exceptions.RequestException as e:
               st.error(f"Error contacting API: {e}")
           else:
               if resp.status_code != 200:
                   st.error(
                       f"Could not delete course. "
                       f"Status {resp.status_code}, response: {resp.text}"
                   )
               else:
                   st.success("✅ Course removed from plan.")
                   st.rerun()