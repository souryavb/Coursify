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

# track whether successfully loaded plans at least once
if "plans_loaded" not in st.session_state:
    st.session_state["plans_loaded"] = False

# Automatically load plans if not loaded yet
if not st.session_state["plans_loaded"]:
    try:
        resp = requests.get(f"{BASE_URL}/s/student{int(student_id)}/plans")
        if resp.status_code == 200:
            st.session_state["plans"] = resp.json()
            st.session_state["plans_loaded"] = True
        else:
            st.session_state["plans"] = []
    except requests.exceptions.RequestException as e:
        st.session_state["plans"] = []

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

        # Create display options: "Plan ID: 35 - Trial Plan 1"
        plan_display_options = {
            p["planID"]: f"Plan ID: {p['planID']} - {p['plan_name']}"
            for p in plans
        }
        
        plan_ids = [p["planID"] for p in plans]
        selected = st.selectbox(
            "Select a plan to view details",
            options=plan_ids,
            format_func=lambda x: plan_display_options[x],
        )

        if st.button("Open selected plan"):
            st.session_state["selected_plan_id"] = int(selected)
            st.switch_page("pages/13_Student_Plan_Detail.py")

st.markdown("---")

# ----------------- Create a new plan -----------------
st.subheader("Create a new what-if plan")

# Fetch available programs
try:
    programs_resp = requests.get(f"{BASE_URL}/p/programs")
    
    if programs_resp.status_code == 200:
        all_programs = programs_resp.json()
        
        # Create display format: "BS Computer Science (Undergraduate)"
        program_options = {
            p['programID']: f"{p['program']} ({p['type']})"
            for p in all_programs
        }
        
        with st.form("create_plan_form"):
            plan_name = st.text_input("Plan name")
            expected_grad = st.date_input("Expected graduation date")
            
            program_id = st.selectbox(
                "Program",
                options=list(program_options.keys()),
                format_func=lambda x: program_options[x],
                index=0,
                key="program_select"
            )
            
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
                            
                            # Set success flag to show AFTER rerun
                            st.session_state["show_create_success"] = True
                            st.session_state["new_plan_name"] = plan_name.strip()
                            st.session_state["new_plan_id"] = data['planID']
                            
                            # Reload plans list
                            try:
                                refresh_resp = requests.get(f"{BASE_URL}/s/student{int(student_id)}/plans")
                                if refresh_resp.status_code == 200:
                                    st.session_state["plans"] = refresh_resp.json()
                                    st.session_state["plans_loaded"] = True
                            except:
                                pass
                            
                            st.rerun()
    else:
        st.error(f"Could not load programs. Status: {programs_resp.status_code}")

except requests.exceptions.RequestException as e:
    st.error(f"Error loading programs: {e}")

# Show success message if plan was just created (MOVED OUTSIDE try/except)
if st.session_state.get("show_create_success", False):
    st.success(
        f"✅ Plan '{st.session_state.get('new_plan_name')}' created successfully "
        f"(planID {st.session_state.get('new_plan_id')})!"
    )
    st.session_state["show_create_success"] = False

