import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

request_id = st.session_state.get("selected_request_id")

if not request_id:
    st.error("No request selected.")
    st.stop()

# Get details
base_api = "http://web-api:4000"

url = f"{base_api}/prof/overriderequests/{request_id}"
resp = requests.get(url)

if resp.status_code != 200:
    st.error(f"Could not fetch request details (status {resp.status_code})")
    st.stop()

data = resp.json()

st.title(f"Override Request #{request_id}")
st.json(data)

new_status = st.selectbox("Update status", ["Approved", "Denied", "Pending"])

if st.button("Update Status"):
    update = {"status": new_status}
    put_url = f"{base_api}/prof/overriderequests/{request_id}"
    put_resp = requests.put(put_url, json=update)

    if put_resp.status_code == 200:
        st.success("Status updated.")
    else:
        st.error(f"Error updating status (status {put_resp.status_code})")