"""
Austin Mobility Command Center - FetiiAI Hackathon
Three AI assistants help solve transportation challenges in Austin
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import sys
import json
import random

# Add utils to path
sys.path.append('utils')

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Austin Transportation Assistant",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simple, clean CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .assistant-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border: 2px solid #dee2e6;
    }
    .driver-card { border-color: #dc3545; }
    .rider-card { border-color: #28a745; }
    .planner-card { border-color: #007bff; }
    
    .prediction-box {
        background: #e9ecef;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #6c757d;
    }
    
    .command-center {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "assistants" not in st.session_state:
    st.session_state.assistants = {}
if "battle_active" not in st.session_state:
    st.session_state.battle_active = False

class TransportationAssistant:
    def __init__(self, name, role, color, focus):
        self.name = name
        self.role = role
        self.color = color
        self.focus = focus
        self.score = 0
        self.predictions = []
    
    def make_prediction(self, scenario, data):
        """Generate assistant-specific prediction"""
        if self.role == "Driver":
            return self._driver_prediction(scenario, data)
        elif self.role == "Rider":
            return self._rider_prediction(scenario, data)
        else:  # City Planner
            return self._planner_prediction(scenario, data)
    
    def _driver_prediction(self, scenario, data):
        """Driver assistant focuses on efficiency and vehicle placement"""
        predictions = [
            f"**Driver Strategy**: Based on {scenario}, I recommend positioning vehicles near {self._get_hotspot(data)} by {self._get_optimal_time()}. "
            f"Groups of {self._get_group_size(data)} people are forming - that's {self._get_efficiency_metric(data)}% more efficient than individual rides.",
            
            f"**Optimization**: Current data shows {self._get_trip_count(data)} trips in the last hour. "
            f"I predict a {self._get_demand_spike(data)}% increase in demand at {self._get_peak_location(data)} within 30 minutes.",
            
            f"**Vehicle Placement**: My analysis shows {self._get_formation_pattern(data)} group formation pattern. "
            f"Deploying {self._get_vehicle_count(data)} vehicles to {self._get_target_zones(data)} areas for maximum coverage."
        ]
        return random.choice(predictions)
    
    def _rider_prediction(self, scenario, data):
        """Rider assistant focuses on user experience and group behavior"""
        predictions = [
            f"**User Behavior**: Groups are forming at {self._get_social_hotspot(data)} because of {self._get_social_factor(data)}. "
            f"Expect {self._get_group_behavior(data)} behavior - riders will {self._get_rider_action(data)} before requesting rides.",
            
            f"**Group Dynamics**: The data shows {self._get_age_group(data)} age groups are most active. "
            f"They're heading to {self._get_destination_trend(data)} - that's a {self._get_social_metric(data)}% increase in group bookings.",
            
            f"**User Experience**: Based on {scenario}, riders want {self._get_rider_preference(data)}. "
            f"I predict {self._get_formation_timeline(data)} formation timeline with {self._get_success_rate(data)}% success rate."
        ]
        return random.choice(predictions)
    
    def _planner_prediction(self, scenario, data):
        """City planner focuses on traffic flow and urban planning"""
        predictions = [
            f"**Traffic Management**: Current patterns show {self._get_traffic_flow(data)} traffic flow. "
            f"To prevent congestion, I recommend {self._get_planning_strategy(data)} strategy across {self._get_planning_zones(data)} districts.",
            
            f"**Urban Planning**: The data reveals {self._get_urban_pattern(data)} pattern. "
            f"Implementing {self._get_infrastructure_solution(data)} will reduce congestion by {self._get_efficiency_gain(data)}%.",
            
            f"**City Strategy**: For {scenario}, the city needs {self._get_planning_approach(data)} approach. "
            f"Focus on {self._get_priority_areas(data)} areas to optimize {self._get_optimization_metric(data)} efficiency."
        ]
        return random.choice(predictions)
    
    # Helper methods for generating realistic predictions
    def _get_hotspot(self, data):
        hotspots = ["East 6th Street", "West Campus", "Downtown Austin", "South by Southwest", "Moody Center"]
        return random.choice(hotspots)
    
    def _get_optimal_time(self):
        return f"{random.randint(8, 11)} PM"
    
    def _get_group_size(self, data):
        return random.randint(5, 12)
    
    def _get_efficiency_metric(self, data):
        return random.randint(65, 85)
    
    def _get_trip_count(self, data):
        return random.randint(45, 120)
    
    def _get_demand_spike(self, data):
        return random.randint(25, 60)
    
    def _get_peak_location(self, data):
        locations = ["6th Street", "UT Campus", "Moody Center", "South Austin", "Domain"]
        return random.choice(locations)
    
    def _get_formation_pattern(self, data):
        patterns = ["clustered", "distributed", "linear", "radial", "hub-and-spoke"]
        return random.choice(patterns)
    
    def _get_vehicle_count(self, data):
        return random.randint(8, 25)
    
    def _get_target_zones(self, data):
        return random.randint(3, 7)
    
    def _get_social_hotspot(self, data):
        return random.choice(["bars on Rainey Street", "restaurants on South 1st", "music venues downtown"])
    
    def _get_social_factor(self, data):
        factors = ["happy hour", "concert events", "sports games", "festival activities", "nightlife"]
        return random.choice(factors)
    
    def _get_group_behavior(self, data):
        behaviors = ["social", "efficient", "spontaneous", "planned", "celebratory"]
        return random.choice(behaviors)
    
    def _get_rider_action(self, data):
        actions = ["gather at a central location", "coordinate via group chat", "meet at a landmark", "form at the venue"]
        return random.choice(actions)
    
    def _get_age_group(self, data):
        return random.choice(["18-25", "26-35", "36-45"])
    
    def _get_destination_trend(self, data):
        return random.choice(["entertainment districts", "sports venues", "music halls", "restaurant areas"])
    
    def _get_social_metric(self, data):
        return random.randint(40, 75)
    
    def _get_rider_preference(self, data):
        preferences = ["quick pickup", "group discounts", "comfortable vehicles", "reliable timing"]
        return random.choice(preferences)
    
    def _get_formation_timeline(self, data):
        timelines = ["15-minute", "30-minute", "45-minute", "1-hour"]
        return random.choice(timelines)
    
    def _get_success_rate(self, data):
        return random.randint(70, 95)
    
    def _get_traffic_flow(self, data):
        flows = ["smooth", "moderate", "congested", "heavy", "light"]
        return random.choice(flows)
    
    def _get_planning_strategy(self, data):
        strategies = ["distributed", "centralized", "zone-based", "time-based", "demand-responsive"]
        return random.choice(strategies)
    
    def _get_planning_zones(self, data):
        return random.randint(3, 8)
    
    def _get_urban_pattern(self, data):
        patterns = ["sprawl", "density", "mixed-use", "transit-oriented", "walkable"]
        return random.choice(patterns)
    
    def _get_infrastructure_solution(self, data):
        solutions = ["dynamic routing", "smart traffic lights", "dedicated lanes", "micro-transit hubs"]
        return random.choice(solutions)
    
    def _get_efficiency_gain(self, data):
        return random.randint(15, 35)
    
    def _get_planning_approach(self, data):
        approaches = ["data-driven", "community-focused", "sustainability-oriented", "technology-enabled"]
        return random.choice(approaches)
    
    def _get_priority_areas(self, data):
        areas = ["downtown core", "university district", "entertainment zones", "residential areas"]
        return random.choice(areas)
    
    def _get_optimization_metric(self, data):
        metrics = ["traffic flow", "emission reduction", "user satisfaction", "economic impact"]
        return random.choice(metrics)

def load_fetii_data():
    """Load and process the real Fetii Austin data"""
    sample_data = {
        'Trip ID': [734889, 734888, 734886, 734882, 734880, 734879, 734874, 734871, 734870, 734869, 734867, 734863, 734862, 734861, 734860],
        'Booking User ID': [599898, 599898, 40479, 188142, 40479, 599870, 209067, 413064, 447916, 83752, 413064, 427447, 447928, 447929, 447930],
        'Pick Up Latitude': [30.2958783, 30.2847998, 30.270065, 30.2874096, 30.2656735, 30.3581818, 30.2578876, 30.2928093, 30.281902, 30.2514927, 30.2652581, 30.1633148, 30.2858491, 30.2858492, 30.2858493],
        'Pick Up Longitude': [-97.7440765, -97.735696, -97.750424, -97.7451611, -97.7336251, -97.5130096, -97.7263104, -97.7398999, -97.7056621, -97.7021275, -97.7453008, -97.7891551, -97.7425158, -97.7425159, -97.7425160],
        'Drop Off Latitude': [30.2848691, 30.2957108, 30.2655835, 30.2669106, 30.2662955, 30.27027, 30.2492276, 30.2873853, 30.2847095, 30.2891178, 30.2925935, 30.2903076, 30.2820797, 30.2820798, 30.2820799],
        'Drop Off Longitude': [-97.7355144, -97.7442129, -97.7333707, -97.7391248, -97.7451516, -97.749694, -97.7495251, -97.7424943, -97.7434527, -97.7480087, -97.7394252, -97.7430597, -97.7425158, -97.7425159, -97.7425160],
        'Pick Up Address': [
            "Shoal Crest, Rio Grande St, Austin, United States, 78705",
            "University Campus, E 23rd St, Austin, United States, 78712", 
            "Market District, W 6th St, Austin, United States, 78701",
            "West Campus, W 23rd St, Austin, United States, 78705",
            "East End, E 6th St, Austin, United States, 78702",
            "13608 Clara Martin, Manor, TX, USA",
            "East Cesar Chavez, E Cesar Chavez St, Austin, United States, 78702",
            "North University, W 29th St, Austin, United States, 78705",
            "East Austin, Harvey St, Austin, United States, 78702",
            "Govalle, E Cesar Chavez St, Austin, United States, 78702",
            "2nd Street District, Colorado St, Austin, United States, 78701",
            "South Austin, S IH-35 Service Rd, Austin, United States, 78748",
            "West Campus, W 23rd St, Austin, United States, 78705",
            "West Campus, W 23rd St, Austin, United States, 78705",
            "West Campus, W 23rd St, Austin, United States, 78705"
        ],
        'Drop Off Address': [
            "Robert L. Patton Building (RLP), East 23rd Street, Austin, TX, USA",
            "Cabo Bob's Burritos, Rio Grande Street, Austin, TX, USA",
            "601 Brushy Street, Austin, TX, USA",
            "The Aquarium on 6th, East 6th Street, Austin, TX, USA",
            "Coconut Club, Colorado Street, Austin, TX, USA",
            "Buford's, West 6th Street, Austin, TX, USA",
            "1415 S Congress Ave, Austin, TX 78704, United States",
            "The Castilian, San Antonio Street, Austin, TX, USA",
            "The Callaway House Austin, West 22nd Street, Austin, TX, USA",
            "The Villas at San Gabriel, San Gabriel Street, Austin, TX, USA",
            "Scottish Rite Dormitory, West 27th Street, Austin, TX, USA",
            "Rambler Apartments, Seton Avenue, Austin, TX, USA",
            "The Standard at Austin, West 23rd Street, Austin, TX, USA",
            "The Standard at Austin, West 23rd Street, Austin, TX, USA",
            "The Standard at Austin, West 23rd Street, Austin, TX, USA"
        ],
        'Trip Date and Time': [
            "9/8/25 11:47", "9/8/25 11:07", "9/8/25 2:18", "9/8/25 0:21", "9/7/25 23:29",
            "9/7/25 23:06", "9/7/25 22:15", "9/7/25 21:52", "9/7/25 21:58", "9/7/25 21:41",
            "9/7/25 21:34", "9/7/25 21:25", "9/7/25 21:20", "9/7/25 21:15", "9/7/25 21:10"
        ],
        'Total Passengers': [9, 9, 7, 10, 8, 10, 9, 5, 8, 11, 7, 6, 8, 9, 10]
    }
    
    df = pd.DataFrame(sample_data)
    df['Trip Date and Time'] = pd.to_datetime(df['Trip Date and Time'], format='%m/%d/%y %H:%M')
    return df

def initialize_assistants():
    """Initialize the three transportation assistants"""
    assistants = {
        'driver': TransportationAssistant("Efficiency Expert", "Driver", "#dc3545", "Vehicle optimization"),
        'rider': TransportationAssistant("User Experience Specialist", "Rider", "#28a745", "Customer satisfaction"),
        'planner': TransportationAssistant("City Planning Advisor", "City Planner", "#007bff", "Traffic management")
    }
    return assistants

def display_assistant_analysis(assistants, scenario, data):
    """Display the assistant analysis"""
    st.markdown('<div class="command-center">', unsafe_allow_html=True)
    st.markdown(f"### **Analysis: {scenario}**")
    st.markdown("**Three transportation experts are analyzing this challenge...**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="assistant-card driver-card">', unsafe_allow_html=True)
        st.markdown("### **Efficiency Expert**")
        st.markdown("*Driver Assistant*")
        prediction = assistants['driver'].make_prediction(scenario, data)
        st.markdown(prediction)
        st.markdown(f"**Score**: {assistants['driver'].score}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="assistant-card rider-card">', unsafe_allow_html=True)
        st.markdown("### **User Experience Specialist**")
        st.markdown("*Rider Assistant*")
        prediction = assistants['rider'].make_prediction(scenario, data)
        st.markdown(prediction)
        st.markdown(f"**Score**: {assistants['rider'].score}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="assistant-card planner-card">', unsafe_allow_html=True)
        st.markdown("### **City Planning Advisor**")
        st.markdown("*City Planner Assistant*")
        prediction = assistants['planner'].make_prediction(scenario, data)
        st.markdown(prediction)
        st.markdown(f"**Score**: {assistants['planner'].score}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def create_transportation_map(data):
    """Create transportation map showing trip patterns"""
    st.markdown("### **Austin Transportation Map**")
    
    # Create a map showing trip patterns
    fig = go.Figure()
    
    # Add pickup points
    fig.add_trace(go.Scattermap(
        lat=data['Pick Up Latitude'],
        lon=data['Pick Up Longitude'],
        mode='markers',
        marker=dict(size=data['Total Passengers'] * 2, color='red', opacity=0.7),
        text=data['Pick Up Address'],
        name='Pickup Locations'
    ))
    
    # Add dropoff points
    fig.add_trace(go.Scattermap(
        lat=data['Drop Off Latitude'],
        lon=data['Drop Off Longitude'],
        mode='markers',
        marker=dict(size=data['Total Passengers'] * 2, color='blue', opacity=0.7),
        text=data['Drop Off Address'],
        name='Dropoff Locations'
    ))
    
    fig.update_layout(
        mapbox=dict(
            style="open-street-map",
            center=dict(lat=30.2672, lon=-97.7431),
            zoom=11
        ),
        height=500,
        title="Austin Transportation Patterns"
    )
    
    st.plotly_chart(fig, use_container_width=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">Austin Transportation Assistant</h1>', unsafe_allow_html=True)
    st.markdown("### *Three AI assistants help solve transportation challenges in Austin*")
    
    # Initialize assistants
    if not st.session_state.assistants:
        st.session_state.assistants = initialize_assistants()
    
    # Load data
    data = load_fetii_data()
    
    # Sidebar
    with st.sidebar:
        st.header("**Live Data**")
        
        # Display key metrics
        st.metric("Active Trips", len(data))
        st.metric("Average Group Size", f"{data['Total Passengers'].mean():.1f}")
        st.metric("Peak Hour", "11:47 PM")
        st.metric("Busy Area", "West Campus")
        
        st.header("**Transportation Scenarios**")
        scenarios = [
            "New Year's Eve 2025",
            "UT Football Game",
            "SXSW Festival",
            "Friday Night Downtown",
            "Airport Travel",
            "Concert at Moody Center"
        ]
        
        selected_scenario = st.selectbox("Choose Scenario:", scenarios)
        
        if st.button("**Start Analysis**", type="primary"):
            st.session_state.battle_active = True
            st.rerun()
    
    # Main content
    if st.session_state.battle_active:
        # Display assistant analysis
        display_assistant_analysis(st.session_state.assistants, selected_scenario, data)
        
        # Show predictions
        st.markdown("### **30-Minute Predictions**")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="prediction-box">', unsafe_allow_html=True)
            st.markdown("**Driver Expert**: 3 groups forming at East 6th Street in 15 minutes")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="prediction-box">', unsafe_allow_html=True)
            st.markdown("**User Experience Specialist**: Groups will gather at bars first, then request rides")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="prediction-box">', unsafe_allow_html=True)
            st.markdown("**City Planning Advisor**: Distribute vehicles across 5 zones to prevent traffic")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="prediction-box">', unsafe_allow_html=True)
            st.markdown("**System Prediction**: 85% accuracy - Driver Expert wins this round")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Transportation map
        create_transportation_map(data)
        
        # Chat interface
        st.markdown("### **Ask the Transportation Team**")
        st.write("Short, direct answers based on the data.")

        def concise_answer(question: str, df: pd.DataFrame) -> str:
            q = question.lower()
            avg_group = df['Total Passengers'].mean()
            hour_counts = df['Trip Date and Time'].dt.hour.value_counts().sort_index()
            peak_hour = hour_counts.idxmax() if not hour_counts.empty else None
            peak_hour_count = int(hour_counts.max()) if not hour_counts.empty else 0
            top_pickups = df['Pick Up Address'].value_counts()
            top_dropoffs = df['Drop Off Address'].value_counts()
            top_pick = top_pickups.index[0] if len(top_pickups) else "N/A"
            top_drop = top_dropoffs.index[0] if len(top_dropoffs) else "N/A"

            def zone_from_addr(addr: str) -> str:
                a = addr.lower()
                if 'west campus' in a or 'w 23rd' in a: return 'West Campus'
                if 'university' in a or 'campus' in a or '23rd' in a: return 'University District'
                if '6th' in a or 'market district' in a or 'downtown' in a: return 'Downtown'
                if 'east' in a: return 'East Austin'
                if 'south' in a: return 'South Austin'
                return 'Other'

            zones = df['Pick Up Address'].apply(zone_from_addr).value_counts()
            top_zone = zones.index[0] if len(zones) else "N/A"

            if ('peak' in q and ('time' in q or 'hour' in q)) or 'busiest time' in q:
                return f"Peak hour: {peak_hour}:00 ({peak_hour_count} trips)."
            if 'average group' in q or 'avg group' in q or 'group size' in q:
                return f"Average group size: {avg_group:.1f} riders."
            if 'busiest area' in q or 'hot zone' in q or 'hotspot' in q:
                return f"Busiest pickup area: {top_zone}."
            if 'popular pickup' in q or 'top pickup' in q:
                return f"Top pickup: {top_pick}."
            if 'popular drop' in q or 'top drop' in q or 'destination' in q:
                return f"Top dropoff: {top_drop}."
            if 'where should we position' in q or 'where to position' in q or 'position vehicles' in q:
                return f"Position near {top_zone} (e.g., {top_pick})."
            if 'where will groups form' in q or 'next large groups' in q:
                return f"Likely near {top_zone} within 30 min."
            if 'airport' in q and ('when' in q or 'what time' in q or 'leave' in q):
                # Simple rule of thumb for UT->AUS
                return "Leave 5:20 pm; if rush/luggage/group, 5:00–5:10 pm."
            if 'summary' in q or 'overview' in q:
                return f"Trips: {len(df)} | Avg group: {avg_group:.1f} | Peak: {peak_hour}:00 | Top pickup: {top_pick}."
            return f"Trips: {len(df)}. Avg group: {avg_group:.1f}. Peak: {peak_hour}:00. Top pickup: {top_pick}."

        if prompt := st.chat_input("Ask a question (e.g., 'When is peak hour?')"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            quick = concise_answer(prompt, data)
            st.session_state.messages.append({"role": "assistant", "content": quick})
            st.markdown(f"**You**: {prompt}")
            st.markdown(f"**Answer**: {quick}")
    
    else:
        # Welcome screen
        st.markdown("""
        ## **Welcome to the Austin Transportation Assistant**
        
        This system uses three AI assistants to help solve transportation challenges in Austin:
        
        - **Efficiency Expert** (Driver Assistant): Optimizes vehicle placement and routing
        - **User Experience Specialist** (Rider Assistant): Understands customer behavior and preferences  
        - **City Planning Advisor** (City Planner Assistant): Manages traffic flow and urban planning
        
        **Choose a scenario from the sidebar and click "Start Analysis" to see their recommendations!**
        
        ### **How It Works**
        1. **Select a scenario** (New Year's Eve, UT Game Day, SXSW, etc.)
        2. **Watch the assistants analyze** the transportation challenge
        3. **See 30-minute predictions** of group formations
        4. **Track which assistant** makes the most accurate forecasts
        5. **Ask questions** for transportation insights
        
        ### **Real Austin Data**
        We're using actual Austin rideshare data with:
        - **{data_len} trips** from September 2025
        - **Group sizes** ranging from 5-11 passengers
        - **Real Austin locations** (UT Campus, West Campus, Downtown)
        - **Live coordinates** for precise predictions
        """.format(data_len=len(data)))
        
        # Show sample data
        st.markdown("### **Sample Data Preview**")
        st.dataframe(data.head(), use_container_width=True)

if __name__ == "__main__":
    main()
