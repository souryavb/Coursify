import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import pandas as pd 
import plotly.express as px
import matplotlib.pyplot as plt 


prof_id = st.session_state['selected_prof_id']


API_URL = f"http://web-api:4000/d/data/professor/{prof_id}"
data = requests.get(API_URL).json()

prof = data[0]


# Back button
if st.button("← Back"):
    st.switch_page("pages/43_professor.py")

full_name = f"{prof['first_name']} {prof['last_name']}"

st.header(f"Ratings for {full_name} 👨‍🏫")

# display data

if prof:

    #ratings_df = pd.DataFrame(prof)
    #ratings_df['rating'] = ratings_df['rating'].astype(float)

    tab1, tab2 = st.tabs(["📋 All Ratings", "📊 Distribution"])

    with tab1:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("⭐ Rating", f"{prof['ratings']}")
        
        with col2:
            st.write("**💬 Comment**")
            st.write(prof['comment'])
        
        with col3:
            st.write("**📅 Time**")
            st.write(prof['rating_time'])
        
        st.divider()

    with tab2: 
        st.dataframe(prof)

        # Get all individual ratings (not the summary)
        ratings_df = pd.DataFrame([prof])  # This has all ratings
        ratings_df['rating'] = ratings_df['ratings'].astype(float)

        # Count how many of each star rating (1, 2, 3, 4, 5)
        rating_counts = ratings_df['ratings'].value_counts().sort_index()

        # Ensure all ratings 1-5 exist (even if 0)
        for i in range(1, 6):
            if float(i) not in rating_counts.index:
                rating_counts[float(i)] = 0
        rating_counts = rating_counts.sort_index()

        # Create bar chart
        fig = px.bar(
            x=rating_counts.index,
            y=rating_counts.values,
            labels={'x': '⭐ Star Rating', 'y': 'Number of Ratings'},
            title='Rating Distribution',
            text=rating_counts.values
        )

        fig.update_traces(textposition='outside')
        fig.update_layout(xaxis=dict(tickvals=[1, 2, 3, 4, 5]))

        st.plotly_chart(fig, use_container_width=True)