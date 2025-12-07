import streamlit as st
import requests
from modules.nav import SideBarLinks


st.set_page_config(layout="wide")
SideBarLinks()


BASE_URL = "http://localhost:4000"


student_id = st.session_state.get("user_id")
plan_id = st.session_state.get("selected_plan_id")


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
st.subheader(f"Plan {plan['planID']}: {plan['plan_name']}")
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


# ---------- current courses ----------
st.subheader("Courses in this plan")


courses = plan.get("courses", [])
if not courses:
   st.info("This plan has no courses yet.")
else:
   st.table(courses)


course_ids_in_plan = [c["courseID"] for c in courses]


# ---------- add new course ----------
st.markdown("### Add a course to this plan")


with st.form("add_course_form"):
   new_course_id = st.number_input(
       "Course ID", min_value=1, step=1, value=101
   )
   planned_sem = st.text_input("Planned semester (e.g. 'Fall 2025')")
   new_status = st.selectbox(
       "Course status",
       ["Planned", "In Progress", "Completed", "Dropped"],
       index=0,
   )


   add_submitted = st.form_submit_button("Add course")


   if add_submitted:
       payload = {
           "courseID": int(new_course_id),
           "planned_semester": planned_sem.strip(),
           "course_status": new_status,
       }
       try:
           # NOTE: /p prefix for plan routes
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
               st.success("Course added to plan.")
               st.experimental_rerun()


st.markdown("---")


# ---------- update / delete existing course ----------
st.markdown("### Update or remove a course in this plan")


if not course_ids_in_plan:
   st.info("Nothing to update/delete yet.")
else:
   selected_course = st.selectbox(
       "Select course in this plan",
       course_ids_in_plan,
   )


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
                       st.success("Course in plan updated.")
                       st.experimental_rerun()


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
                   st.success("Course removed from plan.")
                   st.experimental_rerun()

