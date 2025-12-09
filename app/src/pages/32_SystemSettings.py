import streamlit as st
import requests
from modules.nav import SideBarLinks


# 1. Page Config
st.set_page_config(layout="wide")
SideBarLinks()


# 2. Back Button
if st.button("← Back"):
   st.switch_page("pages/20_Admin_Home.py")


st.title("🛠️ System Settings")
st.write("Manage global variables for the course scheduling system.")
st.divider()


# 3. Define API URL
# Matches backend route: /dj/system-settings/<key>
BASE_API_URL = "http://web-api:4000/sj/system-settings"


# 4. Helper Function to Update Settings
def update_setting(key, new_value, new_desc):
   try:
       url = f"{BASE_API_URL}/{key}"
       payload = {
           "value": new_value,
           "description": new_desc
       }
       # PUT request to update the database
       response = requests.put(url, json=payload)
      
       if response.status_code == 200:
           st.success(f"✅ Setting '{key}' updated successfully!")
       else:
           st.error(f"Failed to update. Status: {response.status_code}")
   except Exception as e:
       st.error(f"Error connecting to API: {e}")


# 5. List of Settings to Manage
settings_to_manage = ["max_enroll", "override_deadline_days"]


# 6. Loop through keys and display cards
for key in settings_to_manage:
   try:
       # Fetch current data using the rubric-required route
       response = requests.get(f"{BASE_API_URL}/{key}")
      
       if response.status_code == 200:
           data = response.json()
          
           # Backend returns a list like [{'settingKey': '...', ...}]
           if data and len(data) > 0:
               current_setting = data[0]
              
               # Create a visual container for each setting
               with st.container(border=True):
                   st.subheader(f"Setting: {key}")
                  
                   c1, c2, c3 = st.columns([1, 2, 1])
                  
                   with c1:
                       new_val = st.text_input(
                           "Value",
                           value=current_setting.get('settingValue', ''),
                           key=f"val_{key}"
                       )
                  
                   with c2:
                       new_desc = st.text_input(
                           "Description",
                           value=current_setting.get('description', ''),
                           key=f"desc_{key}"
                       )
                  
                   with c3:
                       st.write("Action")
                       if st.button(f"Update", key=f"btn_{key}"):
                           update_setting(key, new_val, new_desc)
                          
           else:
               st.warning(f"Setting '{key}' not found in database.")
       else:
           st.error(f"Could not load '{key}'. Status: {response.status_code}")
          
   except Exception as e:
       st.error(f"Error connecting to API for {key}: {e}")