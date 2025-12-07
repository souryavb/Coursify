import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

prof_id = st.session_state.get("user_id", 501)

st.title("Override Requests For My Sections")

base_api = "http://web-api:4000"
url = f"{base_api}/prof/professors/{prof_id}/overriderequests"
resp = requests.get(url)

if resp.status_code != 200:
    st.error(f"Could not fetch override requests (status {resp.status_code})")
else:
    requests_list = resp.json()

    if not requests_list:
        st.info("No override requests for your sections.")
        st.stop()

    st.table(requests_list)

    # Dropdown with request IDs
    selected = st.selectbox(
        "Select a request to view details",
        [r["request_id"] for r in requests_list]
    )

    if st.button("View Request"):
        st.session_state["selected_request_id"] = selected
        st.switch_page("pages/23_Professor_Single_Request.py")