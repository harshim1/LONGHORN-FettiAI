"""
FetiiAI Hackathon - Austin Rideshare Analytics Chatbot
A Streamlit-powered chatbot that provides insights on Fetii's Austin rideshare data
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="FetiiAI - Austin Rideshare Analytics",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .bot-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #dee2e6;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False

def load_sample_data():
    """Load sample rideshare data for demonstration"""
    # Sample data structure based on typical rideshare datasets
    sample_data = {
        'trip_id': range(1, 1001),
        'pickup_datetime': pd.date_range('2024-01-01', periods=1000, freq='H'),
        'dropoff_datetime': pd.date_range('2024-01-01 00:30:00', periods=1000, freq='H'),
        'pickup_latitude': [30.2672 + (i % 10) * 0.01 for i in range(1000)],
        'pickup_longitude': [-97.7431 + (i % 10) * 0.01 for i in range(1000)],
        'dropoff_latitude': [30.2672 + (i % 15) * 0.01 for i in range(1000)],
        'dropoff_longitude': [-97.7431 + (i % 15) * 0.01 for i in range(1000)],
        'group_size': [2, 3, 4, 5, 6, 7, 8][i % 7] for i in range(1000)],
        'rider_age': [18 + (i % 50) for i in range(1000)],
        'pickup_address': [f"Sample Address {i % 20}" for i in range(1000)],
        'dropoff_address': [f"Destination {i % 25}" for i in range(1000)],
        'trip_duration_minutes': [15 + (i % 60) for i in range(1000)],
        'fare_amount': [20 + (i % 80) for i in range(1000)]
    }
    return pd.DataFrame(sample_data)

def display_chat_message(role, content):
    """Display a chat message with appropriate styling"""
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>You:</strong> {content}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message bot-message">
            <strong>FetiiAI:</strong> {content}
        </div>
        """, unsafe_allow_html=True)

def generate_insight_response(query, data):
    """Generate AI-powered response based on query and data"""
    # This is a placeholder for the actual GPT integration
    # For now, we'll provide basic analytics responses
    
    query_lower = query.lower()
    
    if "moody center" in query_lower:
        moody_trips = data[data['dropoff_address'].str.contains('Moody', case=False, na=False)]
        count = len(moody_trips)
        avg_group_size = moody_trips['group_size'].mean()
        return f"Based on the data, {count} groups went to Moody Center. The average group size was {avg_group_size:.1f} people."
    
    elif "peak" in query_lower and "time" in query_lower:
        hourly_trips = data.groupby(data['pickup_datetime'].dt.hour).size()
        peak_hour = hourly_trips.idxmax()
        peak_count = hourly_trips.max()
        return f"The peak ride time is {peak_hour}:00 with {peak_count} trips. This suggests high demand during this hour."
    
    elif "group size" in query_lower:
        group_stats = data['group_size'].value_counts().sort_index()
        most_common = group_stats.idxmax()
        return f"The most common group size is {most_common} people, with {group_stats[most_common]} trips."
    
    elif "age" in query_lower:
        age_stats = data['rider_age'].describe()
        return f"Rider age statistics: Average age is {age_stats['mean']:.1f} years, ranging from {age_stats['min']:.0f} to {age_stats['max']:.0f} years."
    
    else:
        return "I can help you analyze Austin rideshare data! Try asking about specific locations like 'Moody Center', peak ride times, group sizes, or rider demographics."

def create_visualizations(data):
    """Create interactive visualizations"""
    col1, col2 = st.columns(2)
    
    with col1:
        # Group size distribution
        fig_group = px.histogram(data, x='group_size', title='Group Size Distribution',
                               labels={'group_size': 'Group Size', 'count': 'Number of Trips'})
        st.plotly_chart(fig_group, use_container_width=True)
    
    with col2:
        # Hourly trip distribution
        hourly_trips = data.groupby(data['pickup_datetime'].dt.hour).size().reset_index()
        hourly_trips.columns = ['hour', 'trips']
        fig_hourly = px.line(hourly_trips, x='hour', y='trips', title='Trips by Hour of Day')
        st.plotly_chart(fig_hourly, use_container_width=True)
    
    # Age distribution
    fig_age = px.histogram(data, x='rider_age', title='Rider Age Distribution',
                          labels={'rider_age': 'Age', 'count': 'Number of Riders'})
    st.plotly_chart(fig_age, use_container_width=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🚗 FetiiAI - Austin Rideshare Analytics</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📊 Data Overview")
        
        # Load data
        if not st.session_state.data_loaded:
            with st.spinner("Loading rideshare data..."):
                data = load_sample_data()
                st.session_state.data = data
                st.session_state.data_loaded = True
        
        data = st.session_state.data
        
        # Display key metrics
        st.metric("Total Trips", len(data))
        st.metric("Average Group Size", f"{data['group_size'].mean():.1f}")
        st.metric("Average Trip Duration", f"{data['trip_duration_minutes'].mean():.1f} min")
        st.metric("Average Fare", f"${data['fare_amount'].mean():.2f}")
        
        st.header("🎯 Quick Insights")
        st.write("• Most common group size:", data['group_size'].mode().iloc[0])
        st.write("• Peak hour:", data.groupby(data['pickup_datetime'].dt.hour).size().idxmax(), ":00")
        st.write("• Average rider age:", f"{data['rider_age'].mean():.1f} years")
    
    # Main chat interface
    st.header("💬 Chat with FetiiAI")
    st.write("Ask me anything about Austin rideshare patterns, group sizes, popular destinations, and more!")
    
    # Display chat history
    for message in st.session_state.messages:
        display_chat_message(message["role"], message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about rideshare data..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        display_chat_message("user", prompt)
        
        # Generate and display bot response
        with st.spinner("Analyzing data..."):
            response = generate_insight_response(prompt, data)
            st.session_state.messages.append({"role": "assistant", "content": response})
            display_chat_message("assistant", response)
    
    # Visualizations section
    st.header("📈 Data Visualizations")
    create_visualizations(data)
    
    # Sample queries section
    st.header("💡 Try These Sample Queries")
    sample_queries = [
        "How many groups went to Moody Center?",
        "What are the peak ride times?",
        "What's the most common group size?",
        "Tell me about rider age demographics",
        "Show me popular pickup locations"
    ]
    
    for query in sample_queries:
        if st.button(f"💬 {query}", key=f"sample_{query}"):
            st.session_state.messages.append({"role": "user", "content": query})
            display_chat_message("user", query)
            
            with st.spinner("Analyzing..."):
                response = generate_insight_response(query, data)
                st.session_state.messages.append({"role": "assistant", "content": response})
                display_chat_message("assistant", response)

if __name__ == "__main__":
    main()
