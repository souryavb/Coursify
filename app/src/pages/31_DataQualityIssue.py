import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks


# 1. Page Configuration
st.set_page_config(layout="wide")
SideBarLinks()


# 2. Back Button
if st.button("← Back"):
   st.switch_page("pages/20_Admin_Home.py")


# Removed emoji from title
st.title("Data Quality Issues")


# 3. Define API URL
API_URL = "http://localhost:4000/dj/data-quality/checks"


# 4. Helper function to delete an issue
def resolve_issue(issue_id):
   try:
       delete_url = f"{API_URL}?issueID={issue_id}"
       response = requests.delete(delete_url)
      
       if response.status_code == 200:
           st.success(f"Issue {issue_id} resolved successfully!")
           st.rerun()
       else:
           st.error(f"Failed to resolve. Status: {response.status_code}")
   except Exception as e:
       st.error(f"Error connecting to API: {e}")


# 5. Main Data Fetching & Display
try:
   response = requests.get(API_URL)
   response.raise_for_status()
   data = response.json()
  
   if data:
       df = pd.DataFrame(data)


       # --- Filters Section ---
       col1, col2 = st.columns(2)
       with col1:
           severities = ["All"] + sorted(df['severity'].unique().tolist())
           selected_severity = st.selectbox("Filter by Severity", severities)
       with col2:
           statuses = ["All"] + sorted(df['status'].unique().tolist())
           selected_status = st.selectbox("Filter by Status", statuses)


       # Apply Filters
       filtered_df = df.copy()
       if selected_severity != "All":
           filtered_df = filtered_df[filtered_df['severity'] == selected_severity]
       if selected_status != "All":
           filtered_df = filtered_df[filtered_df['status'] == selected_status]


       st.divider()
       st.write(f"### Found {len(filtered_df)} issues")


       # --- Display Issues as Cards ---
       h1, h2, h3, h4 = st.columns([3, 2, 2, 1])
       h1.write("**Issue Type**")
       h2.write("**Detected At**")
       h3.write("**Severity**")
       h4.write("**Action**")
       st.divider()


       for _, row in filtered_df.iterrows():
           c1, c2, c3, c4 = st.columns([3, 2, 2, 1])
          
           with c1:
               st.write(f"**{row['issue_type']}**")
               st.caption(f"ID: {row['issueID']}")
          
           with c2:
               st.write(row['detected_at'])


           with c3:
               st.write(row['severity'])


           with c4:
               if st.button("Resolve", key=f"btn_{row['issueID']}"):
                   resolve_issue(row['issueID'])
          
           st.divider()
          
   else:
       st.write("No data quality issues found.")


except Exception as e:
   st.error(f"Error fetching data: {e}")