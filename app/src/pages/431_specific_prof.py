import streamlit as st
import pandas as pd
import plotly.express as px
import requests

prof_id = st.session_state['selected_prof_id']

# Back button
if st.button("← Back"):
    st.switch_page("pages/43_professor.py")

# Fetch ALL ratings for this professor
RATINGS_URL = f"http://web-api:4000/d/data/professor/{prof_id}"

response = requests.get(RATINGS_URL)
response.raise_for_status()
ratings_data = response.json()

if ratings_data and len(ratings_data) > 0:
    # Convert to DataFrame
    ratings_df = pd.DataFrame(ratings_data)
    ratings_df['ratings'] = ratings_df['ratings'].astype(float)
    
    # Get professor name from first rating
    full_name = f"{ratings_data[0]['first_name']} {ratings_data[0]['last_name']}"
    
    st.header(f"Ratings for {full_name} 👨‍🏫")
    
    # Summary metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average Rating", f"{ratings_df['ratings'].mean():.2f} ⭐")
    with col2:
        st.metric("Total Ratings", len(ratings_df))
    with col3:
        st.metric("Latest Rating", f"{ratings_df['ratings'].iloc[0]:.2f} ⭐")
    
    st.divider()
    
    # Create tabs
    tab1, tab2 = st.tabs(["📋 All Ratings", "📊 Distribution"])
    
    with tab1:
        st.subheader("All Ratings & Comments")
        
        # Display each rating
        for idx, rating in ratings_df.iterrows():
            with st.container():
                col1, col2 = st.columns([1, 4])
                
                with col1:
                    st.metric("⭐", f"{rating['ratings']:.2f}")
                    st.caption(rating['rating_time'][:10])  # Just the date
                
                with col2:
                    st.write("**💬 Comment:**")
                    if pd.notna(rating['comment']) and rating['comment']:
                        st.write(rating['comment'])
                    else:
                        st.caption("_No comment provided_")
            
            st.divider()
    
    with tab2:
        st.subheader("📊 Rating Distribution")
        
        # Count ratings by value
        rating_counts = ratings_df['ratings'].value_counts().sort_index()
        
        rating_counts = rating_counts.round(0)

        all_ratings = pd.Series([0]*5, index=[1.0, 2.0, 3.0, 4.0, 5.0])
        rating_counts = rating_counts.add(all_ratings, fill_value=0).sort_index()
        
        # Create bar chart
        fig = px.bar(
            x=rating_counts.index,
            y=rating_counts.values,
            labels={'x': '⭐ Star Rating', 'y': 'Number of Ratings'},
            title=f'Rating Distribution for {full_name}',
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Additional stats
        col1, col2= st.columns(2)
        with col1:
            st.metric("Highest Rating", f"{ratings_df['ratings'].max():.2f} ⭐")
        with col2:
            st.metric("Lowest Rating", f"{ratings_df['ratings'].min():.2f} ⭐")

else:
    st.warning("No ratings available for this professor")
    
