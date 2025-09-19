"""
FetiiAI Hackathon - Enhanced Austin Rideshare Analytics Chatbot
Integrated with GPT-4/GPT-3.5 for intelligent responses
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import sys

# Add utils to path
sys.path.append('utils')

from data_processor import FetiiDataProcessor
from ai_integration import FetiiAI
from local_ai_engine import LocalAIEngine

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="FetiiAI - Austin Rideshare Analytics",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
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
        text-align: center;
    }
    .suggestion-button {
        margin: 0.25rem;
        padding: 0.5rem 1rem;
        border-radius: 1rem;
        background-color: #f0f2f6;
        border: 1px solid #d1d5db;
        cursor: pointer;
        transition: all 0.2s;
    }
    .suggestion-button:hover {
        background-color: #e5e7eb;
        transform: translateY(-1px);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False
if "ai_initialized" not in st.session_state:
    st.session_state.ai_initialized = False

# Initialize AI on startup if API key is available
if not st.session_state.ai_initialized:
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        try:
            from ai_integration import FetiiAI
            ai = FetiiAI(api_key)
            st.session_state.ai_initialized = True
            st.session_state.ai_system = ai
        except Exception as e:
            st.session_state.ai_initialized = False

@st.cache_data
def load_sample_data():
    """Load real Fetii Austin rideshare data"""
    from fetii_data_loader import FetiiDataLoader
    
    # Load real Austin data
    loader = FetiiDataLoader()
    loader.load_from_google_sheets()
    
    # Convert to the format expected by the app
    df = loader.data.copy()
    
    # Rename columns to match expected format
    column_mapping = {
        'Trip ID': 'trip_id',
        'Pick Up Latitude': 'pickup_latitude', 
        'Pick Up Longitude': 'pickup_longitude',
        'Drop Off Latitude': 'dropoff_latitude',
        'Drop Off Longitude': 'dropoff_longitude',
        'Pick Up Address': 'pickup_address',
        'Drop Off Address': 'dropoff_address',
        'Trip Date and Time': 'pickup_datetime',
        'Total Passengers': 'group_size'
    }
    
    df = df.rename(columns=column_mapping)
    
    # Convert datetime
    df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'], format='%m/%d/%y %H:%M')
    
    # Create dropoff datetime (assume 30 min average trip)
    df['dropoff_datetime'] = df['pickup_datetime'] + pd.Timedelta(minutes=30)
    
    # Add derived columns
    df['pickup_hour'] = df['pickup_datetime'].dt.hour
    df['trip_duration_minutes'] = 30  # Assume 30 min average
    df['fare_amount'] = df['group_size'] * 15  # Assume $15 per person
    df['rider_age'] = 25  # Assume average age
    
    return df

def initialize_ai():
    """Initialize the AI system"""
    try:
        # Use Local AI Engine instead of external API
        ai = LocalAIEngine()
        st.session_state.ai_initialized = True
        st.session_state.ai_system = ai
        return ai
    except Exception as e:
        st.error(f"Failed to initialize AI: {str(e)}")
        return None

def display_chat_message(role, content):
    """Display a chat message with appropriate styling"""
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>👤 You:</strong> {content}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message bot-message">
            <strong>🤖 FetiiAI:</strong> {content}
        </div>
        """, unsafe_allow_html=True)

def generate_response(question, data_processor, ai_system=None):
    """Generate response using AI or fallback logic"""
    if ai_system and st.session_state.ai_initialized:
        # Use AI system
        try:
            # Analyze query intent
            intent = ai_system.analyze_query_intent(question)
            
            # Prepare data context
            data_context = {
                'stats': data_processor.get_trip_statistics(),
                'filtered_data': None,
                'popular_destinations': data_processor.get_popular_destinations(),
                'hourly_patterns': data_processor.get_hourly_patterns(),
                'demographics': data_processor.get_demographic_insights()
            }
            
            # Apply filters based on intent
            if intent['location']:
                data_context['filtered_data'] = data_processor.filter_by_location(intent['location'])
            elif intent['time_range']:
                # Apply time filter logic here
                pass
            
            # Generate AI response
            response = ai_system.generate_response(question, data_context)
            return response
            
        except Exception as e:
            st.error(f"AI Error: {str(e)}")
            return "I encountered an error while processing your request. Please try again."
    
    else:
        # Fallback to basic responses
        return generate_basic_response(question, data_processor)

def generate_basic_response(query, data_processor):
    """Generate detailed analysis based on real Fetii Austin data"""
    query_lower = query.lower()
    data = data_processor.processed_data
    
    # Handle different question types with detailed analysis
    if any(word in query_lower for word in ["moody center", "moody"]):
        moody_trips = data[data['dropoff_address'].str.contains('Moody|RLP|Robert L. Patton', case=False, na=False)]
        if len(moody_trips) > 0:
            avg_group_size = moody_trips['group_size'].mean()
            peak_hour = moody_trips['pickup_hour'].mode().iloc[0] if len(moody_trips) > 0 else 'N/A'
            return f"🎯 **Moody Center Analysis**: {len(moody_trips)} trips to Moody Center/RLP. Average group size: {avg_group_size:.1f} people. Peak pickup time: {peak_hour}:00. This shows strong demand for UT campus events!"
        else:
            return "No direct trips to Moody Center found, but check UT campus destinations."
    
    elif any(word in query_lower for word in ["ut", "university", "campus"]):
        ut_trips = data[data['dropoff_address'].str.contains('UT|University|Campus|RLP|Patton', case=False, na=False)]
        if len(ut_trips) > 0:
            avg_group = ut_trips['group_size'].mean()
            peak_time = ut_trips['pickup_hour'].mode().iloc[0] if len(ut_trips) > 0 else 'N/A'
            return f"🎓 **UT Campus Analysis**: {len(ut_trips)} trips to UT campus. Average group: {avg_group:.1f} people. Peak time: {peak_time}:00. Popular pickup areas: {ut_trips['pickup_address'].str.split(',').str[0].value_counts().head(3).index.tolist()}"
        return "UT campus data not found in current dataset."
    
    elif any(word in query_lower for word in ["peak", "busy", "rush", "hour", "time"]):
        hourly_counts = data['pickup_hour'].value_counts().sort_index()
        peak_hour = hourly_counts.idxmax()
        peak_count = hourly_counts.max()
        return f"⏰ **Peak Time Analysis**: Busiest hour is {peak_hour}:00 with {peak_count} trips. Hourly distribution: {dict(hourly_counts.head(5))}. This shows when Austin rideshare demand is highest!"
    
    elif any(word in query_lower for word in ["group", "size", "people", "passenger"]):
        group_stats = data['group_size'].describe()
        most_common = data['group_size'].mode().iloc[0]
        return f"👥 **Group Size Analysis**: Average group size: {group_stats['mean']:.1f} people. Most common: {most_common} people. Range: {group_stats['min']:.0f}-{group_stats['max']:.0f} people. This shows Austin's group travel patterns!"
    
    elif any(word in query_lower for word in ["west campus", "west"]):
        west_trips = data[data['pickup_address'].str.contains('West Campus', case=False, na=False)]
        if len(west_trips) > 0:
            avg_group = west_trips['group_size'].mean()
            destinations = west_trips['dropoff_address'].str.split(',').str[0].value_counts().head(3)
            return f"🏠 **West Campus Analysis**: {len(west_trips)} trips from West Campus. Average group: {avg_group:.1f} people. Top destinations: {destinations.index.tolist()}. Peak pickup: {west_trips['pickup_hour'].mode().iloc[0] if len(west_trips) > 0 else 'N/A'}:00"
        return "West Campus data not found."
    
    elif any(word in query_lower for word in ["downtown", "6th street", "6th"]):
        downtown_trips = data[data['dropoff_address'].str.contains('6th|Downtown|Colorado|Brushy', case=False, na=False)]
        if len(downtown_trips) > 0:
            avg_group = downtown_trips['group_size'].mean()
            return f"🌃 **Downtown Analysis**: {len(downtown_trips)} trips to downtown/6th Street area. Average group: {avg_group:.1f} people. Peak time: {downtown_trips['pickup_hour'].mode().iloc[0] if len(downtown_trips) > 0 else 'N/A'}:00. This shows Austin nightlife patterns!"
        return "Downtown data not found."
    
    elif any(word in query_lower for word in ["total", "how many", "count", "number"]):
        unique_users = data['Booking User ID'].nunique() if 'Booking User ID' in data.columns else 'N/A'
        return f"📊 **Dataset Overview**: {len(data)} total trips from {unique_users} unique users. Average group size: {data['group_size'].mean():.1f} people. Date range: {data['pickup_datetime'].min().strftime('%m/%d/%y')} to {data['pickup_datetime'].max().strftime('%m/%d/%y')}. This is real Austin rideshare data!"
    
    elif any(word in query_lower for word in ["popular", "destination", "where", "location"]):
        top_dests = data['dropoff_address'].str.split(',').str[0].value_counts().head(5)
        return f"�� **Top Destinations**: {dict(top_dests)}. These are the most popular drop-off locations in Austin based on real rideshare data!"
    
    elif any(word in query_lower for word in ["fare", "cost", "price", "money"]):
        return f"💰 **Fare Analysis**: Average fare: ${data['fare_amount'].mean():.2f}. Range: ${data['fare_amount'].min():.2f} - ${data['fare_amount'].max():.2f}. Based on group size pricing model."
    
    elif any(word in query_lower for word in ["east austin", "east"]):
        east_trips = data[data['pickup_address'].str.contains('East', case=False, na=False)]
        if len(east_trips) > 0:
            avg_group = east_trips['group_size'].mean()
            return f"🌅 **East Austin Analysis**: {len(east_trips)} trips from East Austin. Average group: {avg_group:.1f} people. Peak time: {east_trips['pickup_hour'].mode().iloc[0] if len(east_trips) > 0 else 'N/A'}:00"
        return "East Austin data not found."
    
    else:
        return f"🚗 **Austin Rideshare Insights**: Analyzing {len(data)} real trips! Key findings: Average group size {data['group_size'].mean():.1f} people, peak hour {data['pickup_hour'].mode().iloc[0] if 'pickup_hour' in data.columns else 'N/A'}:00, {data['Booking User ID'].nunique() if 'Booking User ID' in data.columns else 'N/A'} unique users. Ask about specific areas like West Campus, UT, Downtown, or East Austin!"

def create_visualizations(data_processor):
    """Create interactive visualizations"""
    data = data_processor.processed_data
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Trips", len(data))
    with col2:
        st.metric("Avg Group Size", f"{data['group_size'].mean():.1f}")
    with col3:
        st.metric("Peak Hour", f"{data['pickup_hour'].mode().iloc[0] if 'pickup_hour' in data.columns else 'N/A'}:00")
    with col4:
        st.metric("Avg Fare", f"${data['fare_amount'].mean():.2f}")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        # Group size distribution
        fig_group = px.histogram(data, x='group_size', title='Group Size Distribution',
                               labels={'group_size': 'Group Size', 'count': 'Number of Trips'},
                               color_discrete_sequence=['#1f77b4'])
        fig_group.update_layout(showlegend=False)
        st.plotly_chart(fig_group, use_container_width=True)
    
    with col2:
        # Hourly trip distribution
        hourly_trips = data.groupby(data['pickup_datetime'].dt.hour).size().reset_index()
        hourly_trips.columns = ['hour', 'trips']
        fig_hourly = px.line(hourly_trips, x='hour', y='trips', title='Trips by Hour of Day',
                           color_discrete_sequence=['#ff7f0e'])
        st.plotly_chart(fig_hourly, use_container_width=True)
    
    # Popular destinations
    popular_dests = data_processor.get_popular_destinations(10)
    if len(popular_dests) > 0:
        fig_dests = px.bar(x=popular_dests.values, y=popular_dests.index, 
                          orientation='h', title='Top 10 Destinations',
                          labels={'x': 'Number of Trips', 'y': 'Destination'})
        fig_dests.update_layout(height=400)
        st.plotly_chart(fig_dests, use_container_width=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">�� FetiiAI - Austin Rideshare Analytics</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📊 Data Overview")
        
        # Load data
        if not st.session_state.data_loaded:
            with st.spinner("Loading rideshare data..."):
                raw_data = load_sample_data()
                data_processor = FetiiDataProcessor()
                data_processor.data = raw_data
                data_processor._preprocess_data()
                st.session_state.data_processor = data_processor
                st.session_state.data_loaded = True
        
        data_processor = st.session_state.data_processor
        data = data_processor.processed_data
        
        # Display key metrics
        stats = data_processor.get_trip_statistics()
        st.metric("Total Trips", stats['total_trips'])
        st.metric("Average Group Size", f"{stats['avg_group_size']:.1f}")
        st.metric("Average Trip Duration", f"{stats['avg_trip_duration']:.1f} min")
        st.metric("Average Fare", f"${stats['avg_fare']:.2f}")
        
        st.header("🎯 Quick Insights")
        st.write("• Most common group size:", stats['most_common_group_size'])
        st.write("• Peak hour:", f"{stats['peak_hour']}:00")
        st.write("• Average rider age:", f"{stats['avg_rider_age']:.1f} years")
        
        # AI Status
        st.header("🤖 AI Status")
        if st.session_state.ai_initialized:
            st.success("✅ Local AI Engine Active")
        else:
            st.warning("⚠️ AI System Not Initialized")
    
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
        
        # Initialize AI if not done
        if not st.session_state.ai_initialized:
            ai_system = initialize_ai()
            if ai_system:
                st.session_state.ai_system = ai_system
        
        # Generate and display bot response
        with st.spinner("Analyzing data..."):
            ai_system = st.session_state.get('ai_system', None)
            response = generate_response(prompt, data_processor, ai_system)
            st.session_state.messages.append({"role": "assistant", "content": response})
            display_chat_message("assistant", response)
    
    # Sample queries section
    st.header("💡 Try These Sample Queries")
    
    # Get suggested queries
    if st.session_state.ai_initialized and 'ai_system' in st.session_state:
        suggested_queries = st.session_state.ai_system.get_suggested_queries()
    else:
        suggested_queries = [
            "How many groups went to Moody Center?",
            "What are the peak ride times?",
            "What's the most common group size?",
            "Tell me about rider age demographics",
            "Show me popular destinations"
        ]
    
    # Display suggestion buttons
    cols = st.columns(2)
    for i, query in enumerate(suggested_queries[:6]):  # Show first 6
        col_idx = i % 2
        with cols[col_idx]:
            if st.button(f"💬 {query}", key=f"sample_{i}"):
                st.session_state.messages.append({"role": "user", "content": query})
                display_chat_message("user", query)
                
                with st.spinner("Analyzing..."):
                    ai_system = st.session_state.get('ai_system', None)
                    response = generate_response(query, data_processor, ai_system)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    display_chat_message("assistant", response)
    
    # Visualizations section
    st.header("📈 Data Visualizations")
    create_visualizations(data_processor)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        🚗 Built for the FetiiAI Hackathon | Powered by Streamlit & OpenAI GPT
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
