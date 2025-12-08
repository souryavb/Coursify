import streamlit as st
import requests
from modules.nav import SideBarLinks


st.set_page_config(layout="wide")
SideBarLinks()


BASE_URL = "http://web-api:4000"

#------------------ Back Button ------------------
if st.button("← Back"):
    st.switch_page("pages/11_Student_Home.py")
#-------------------------------------------------

st.title("My Degree Plans")


# default studentID from session (set on login)
default_student_id = int(st.session_state.get("user_id", 1001))
student_id = st.number_input(
   "Student ID", min_value=1, step=1, value=default_student_id
)
st.session_state["user_id"] = int(student_id)

# ----------------- View existing plans -----------------

# --- session state setup ---
if "plans" not in st.session_state:
    st.session_state["plans"] = []

# track whether we've successfully loaded plans at least once
if "plans_loaded" not in st.session_state:
    st.session_state["plans_loaded"] = False

# convenience alias
plans = st.session_state["plans"]

# -------- load plans button --------
if st.button("Load my plans"):
    try:
        resp = requests.get(f"{BASE_URL}/s/student{int(student_id)}/plans")
    except requests.exceptions.RequestException as e:
        st.error(f"Error contacting API: {e}")
        st.session_state["plans"] = []
        st.session_state["plans_loaded"] = False
    else:
        if resp.status_code != 200:
            st.error(f"Could not load plans. Status {resp.status_code}")
            st.session_state["plans"] = []
            st.session_state["plans_loaded"] = False
        else:
            st.session_state["plans"] = resp.json()
            st.session_state["plans_loaded"] = True

# refresh local variable after possible update
plans = st.session_state["plans"]

# -------- show plans / dropdown / button  --------
if st.session_state["plans_loaded"]:
    if not plans:
        st.info("You have no saved plans yet.")
    else:
        st.subheader("Existing plans")
        st.table(plans)

        plan_ids = [p["planID"] for p in plans]
        selected = st.selectbox(
            "Select a plan to view details",
            plan_ids,
        )

        if st.button("Open selected plan"):
            st.session_state["selected_plan_id"] = int(selected)
            st.switch_page("pages/13_Student_Plan_Detail.py")

st.markdown("---")


# ----------------- Create a new plan -----------------
st.subheader("Create a new what-if plan")


with st.form("create_plan_form"):
   plan_name = st.text_input("Plan name")
   expected_grad = st.date_input("Expected graduation date")
   program_id = st.number_input("Program ID", min_value=1, step=1, value=1)
   is_active = st.checkbox("Set as active plan now?", value=False)


   submitted = st.form_submit_button("Create plan")


   if submitted:
       if not plan_name.strip():
           st.error("Plan name is required.")
       else:
           payload = {
               "plan_name": plan_name.strip(),
               "expected_grad": expected_grad.strftime("%Y-%m-%d"),
               "programID": int(program_id),
               "is_active": 1 if is_active else 0,
           }
           try:
               resp = requests.post(
                   f"{BASE_URL}/s/student{int(student_id)}/plans",
                   json=payload,
               )
           except requests.exceptions.RequestException as e:
               st.error(f"Error contacting API: {e}")
           else:
               if resp.status_code != 201:
                   st.error(
                       f"Could not create plan. Status {resp.status_code}, "
                       f"response: {resp.text}"
                   )
               else:
                   data = resp.json()
                   st.success(
                       f"Plan created successfully (planID {data['planID']})."
                   )

