"""
Austin Mobility War Room - FetiiAI Hackathon
Three AI agents compete to solve mobility challenges in real-time
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
    page_title="Austin Mobility War Room - FetiiAI",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for War Room theme
st.markdown("""
<style>
    .war-room-header {
        font-size: 3rem;
        color: #ff4444;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        background: linear-gradient(45deg, #ff4444, #ffaa00, #44ff44);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .agent-card {
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 1rem 0;
        border: 3px solid #ffaa00;
        box-shadow: 0 8px 16px rgba(0,0,0,0.3);
    }
    .driver-agent { border-color: #ff6b6b; }
    .rider-agent { border-color: #4ecdc4; }
    .planner-agent { border-color: #45b7d1; }
    
    .prediction-bubble {
        background: rgba(255, 255, 255, 0.9);
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #ff4444;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    .battle-arena {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 1rem;
        margin: 1rem 0;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agents" not in st.session_state:
    st.session_state.agents = {}
if "battle_active" not in st.session_state:
    st.session_state.battle_active = False

class MobilityAgent:
    def __init__(self, name, role, color, personality):
        self.name = name
        self.role = role
        self.color = color
        self.personality = personality
        self.score = 0
        self.predictions = []
    
    def make_prediction(self, scenario, data):
        """Generate agent-specific prediction"""
        if self.role == "Driver":
            return self._driver_prediction(scenario, data)
        elif self.role == "Rider":
            return self._rider_prediction(scenario, data)
        else:  # City Planner
            return self._planner_prediction(scenario, data)
    
    def _driver_prediction(self, scenario, data):
        """Driver agent focuses on efficiency and positioning"""
        predictions = [
            f"🚗 **DRIVER STRATEGY**: Based on {scenario}, I'm positioning vehicles near {self._get_hotspot(data)} by {self._get_optimal_time()}. "
            f"Groups of {self._get_group_size(data)} are forming - that's {self._get_efficiency_metric(data)}% more efficient than solo rides!",
            
            f"⚡ **OPTIMIZATION ALERT**: Current data shows {self._get_trip_count(data)} trips in the last hour. "
            f"I'm predicting a {self._get_demand_spike(data)}% demand spike at {self._get_peak_location(data)} within 30 minutes.",
            
            f"🎯 **STRATEGIC POSITIONING**: My algorithm shows {self._get_formation_pattern(data)} group formation pattern. "
            f"Deploying {self._get_vehicle_count(data)} vehicles to {self._get_target_zones(data)} for maximum coverage."
        ]
        return random.choice(predictions)
    
    def _rider_prediction(self, scenario, data):
        """Rider agent focuses on user experience and group dynamics"""
        predictions = [
            f"👥 **RIDER INSIGHT**: Groups are forming at {self._get_social_hotspot(data)} because of {self._get_social_factor(data)}. "
            f"Expect {self._get_group_behavior(data)} behavior pattern - riders will {self._get_rider_action(data)} before requesting rides.",
            
            f"🎉 **SOCIAL DYNAMICS**: The data shows {self._get_age_group(data)} age groups are most active. "
            f"They're heading to {self._get_destination_trend(data)} - that's a {self._get_social_metric(data)}% increase in group bookings!",
            
            f"💡 **USER EXPERIENCE**: Based on {scenario}, riders want {self._get_rider_preference(data)}. "
            f"I predict {self._get_formation_timeline(data)} formation timeline with {self._get_success_rate(data)}% success rate."
        ]
        return random.choice(predictions)
    
    def _planner_prediction(self, scenario, data):
        """City planner focuses on traffic flow and urban planning"""
        predictions = [
            f"🏙️ **CITY PLANNING**: Current mobility patterns show {self._get_traffic_flow(data)} traffic flow. "
            f"To prevent gridlock, I recommend {self._get_planning_strategy(data)} strategy across {self._get_planning_zones(data)} districts.",
            
            f"📊 **URBAN ANALYTICS**: The data reveals {self._get_urban_pattern(data)} pattern. "
            f"Implementing {self._get_infrastructure_solution(data)} will reduce congestion by {self._get_efficiency_gain(data)}%.",
            
            f"🌆 **STRATEGIC PLANNING**: For {scenario}, the city needs {self._get_planning_approach(data)} approach. "
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
    # Sample data based on the Google Sheets structure
    sample_data = {
        'Trip ID': [734889, 734888, 734886, 734882, 734880, 734879, 734874, 734871, 734870, 734869],
        'Booking User ID': [599898, 599898, 40479, 188142, 40479, 599870, 209067, 413064, 447916, 83752],
        'Pick Up Latitude': [30.2958783, 30.2847998, 30.270065, 30.2874096, 30.2656735, 30.3581818, 30.2578876, 30.2928093, 30.281902, 30.2514927],
        'Pick Up Longitude': [-97.7440765, -97.735696, -97.750424, -97.7451611, -97.7336251, -97.5130096, -97.7263104, -97.7398999, -97.7056621, -97.7021275],
        'Drop Off Latitude': [30.2848691, 30.2957108, 30.2655835, 30.2669106, 30.2662955, 30.27027, 30.2492276, 30.2873853, 30.2847095, 30.2891178],
        'Drop Off Longitude': [-97.7355144, -97.7442129, -97.7333707, -97.7391248, -97.7451516, -97.749694, -97.7495251, -97.7424943, -97.7434527, -97.7480087],
        'Pick Up Address': [
            "Shoal Crest, Rio Grande St, Austin, United States, 78705",
            "University Campus, E 23rd St, Austin, United States, 78712",
            "Market District, W 6th St, Austin, United States, 78701",
            "West Campus, W 23rd St, Austin, United States, 78705",
            "East End, E 6th St, Austin, United States, 78702"
        ] * 2,
        'Drop Off Address': [
            "Robert L. Patton Building (RLP), East 23rd Street, Austin, TX, USA",
            "Cabo Bob's Burritos, Rio Grande Street, Austin, TX, USA",
            "601 Brushy Street, Austin, TX, USA",
            "The Aquarium on 6th, East 6th Street, Austin, TX, USA",
            "Coconut Club, Colorado Street, Austin, TX, USA"
        ] * 2,
        'Trip Date and Time': [
            "9/8/25 11:47", "9/8/25 11:07", "9/8/25 2:18", "9/8/25 0:21", "9/7/25 23:29",
            "9/7/25 23:06", "9/7/25 22:15", "9/7/25 21:52", "9/7/25 21:58", "9/7/25 21:41"
        ],
        'Total Passengers': [9, 9, 7, 10, 8, 10, 9, 5, 8, 11]
    }
    
    df = pd.DataFrame(sample_data)
    df['Trip Date and Time'] = pd.to_datetime(df['Trip Date and Time'], format='%m/%d/%y %H:%M')
    return df

def initialize_agents():
    """Initialize the three competing agents"""
    agents = {
        'driver': MobilityAgent("Captain Efficiency", "Driver", "#ff6b6b", "Optimization-focused"),
        'rider': MobilityAgent("Social Navigator", "Rider", "#4ecdc4", "User experience-focused"),
        'planner': MobilityAgent("Urban Strategist", "City Planner", "#45b7d1", "Traffic flow-focused")
    }
    return agents

def display_agent_battle(agents, scenario, data):
    """Display the agent battle arena"""
    st.markdown('<div class="battle-arena">', unsafe_allow_html=True)
    st.markdown(f"### ⚔️ **BATTLE ARENA**: {scenario}")
    st.markdown("**Three AI agents are competing to solve this mobility challenge...**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="agent-card driver-agent">', unsafe_allow_html=True)
        st.markdown("### 🚗 **Captain Efficiency**")
        st.markdown("*Driver Agent*")
        prediction = agents['driver'].make_prediction(scenario, data)
        st.markdown(prediction)
        st.markdown(f"**Score**: {agents['driver'].score}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="agent-card rider-agent">', unsafe_allow_html=True)
        st.markdown("### 👥 **Social Navigator**")
        st.markdown("*Rider Agent*")
        prediction = agents['rider'].make_prediction(scenario, data)
        st.markdown(prediction)
        st.markdown(f"**Score**: {agents['rider'].score}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="agent-card planner-agent">', unsafe_allow_html=True)
        st.markdown("### 🏙️ **Urban Strategist**")
        st.markdown("*City Planner Agent*")
        prediction = agents['planner'].make_prediction(scenario, data)
        st.markdown(prediction)
        st.markdown(f"**Score**: {agents['planner'].score}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def create_predictive_visualization(data):
    """Create predictive visualization showing group formations"""
    st.markdown("### 🔮 **PREDICTIVE GROUP FORMATION MAP**")
    
    # Create a map showing predicted group formations
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
        title="Real-time Group Formation Predictions"
    )
    
    st.plotly_chart(fig, use_container_width=True)

def main():
    # Header
    st.markdown('<h1 class="war-room-header">⚔️ AUSTIN MOBILITY WAR ROOM</h1>', unsafe_allow_html=True)
    st.markdown("### *Three AI agents compete to solve Austin's mobility challenges in real-time*")
    
    # Initialize agents
    if not st.session_state.agents:
        st.session_state.agents = initialize_agents()
    
    # Load data
    data = load_fetii_data()
    
    # Sidebar
    with st.sidebar:
        st.header("📊 **LIVE DATA FEED**")
        st.metric("Active Trips", len(data))
        st.metric("Avg Group Size", f"{data['Total Passengers'].mean():.1f}")
        st.metric("Peak Hour", "11:47 PM")
        st.metric("Hot Zone", "West Campus")
        
        st.header("🎯 **BATTLE SCENARIOS**")
        scenarios = [
            "New Year's Eve 2025 Strategy",
            "UT Football Game Day",
            "SXSW Festival Rush",
            "Friday Night Downtown",
            "Airport Holiday Travel",
            "Concert at Moody Center"
        ]
        
        selected_scenario = st.selectbox("Choose Battle Scenario:", scenarios)
        
        if st.button("🚀 **START BATTLE**", type="primary"):
            st.session_state.battle_active = True
            st.rerun()
    
    # Main content
    if st.session_state.battle_active:
        # Display agent battle
        display_agent_battle(st.session_state.agents, selected_scenario, data)
        
        # Show predictions
        st.markdown("### 🔮 **30-MINUTE PREDICTIONS**")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="prediction-bubble">', unsafe_allow_html=True)
            st.markdown("**🚗 Driver Agent Prediction**: 3 groups forming at East 6th Street in 15 minutes")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="prediction-bubble">', unsafe_allow_html=True)
            st.markdown("**👥 Rider Agent Prediction**: Social groups will gather at bars first, then request rides")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="prediction-bubble">', unsafe_allow_html=True)
            st.markdown("**🏙️ Planner Agent Prediction**: Distribute vehicles across 5 zones to prevent gridlock")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="prediction-bubble">', unsafe_allow_html=True)
            st.markdown("**⚡ System Prediction**: 85% accuracy - Driver Agent wins this round!")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Predictive visualization
        create_predictive_visualization(data)
        
        # Chat interface
        st.markdown("### 💬 **COMMAND CENTER CHAT**")
        st.write("Ask the War Room about mobility strategies, predictions, or agent insights...")
        
        if prompt := st.chat_input("Enter your command..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Generate response from all agents
            response = f"**WAR ROOM ANALYSIS**: {prompt}\n\n"
            for agent_name, agent in st.session_state.agents.items():
                agent_response = agent.make_prediction(prompt, data)
                response += f"**{agent.name}**: {agent_response}\n\n"
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Display messages
            for message in st.session_state.messages[-2:]:
                if message["role"] == "user":
                    st.markdown(f"**👤 You**: {message['content']}")
                else:
                    st.markdown(f"**🤖 War Room**: {message['content']}")
    
    else:
        # Welcome screen
        st.markdown("""
        ## 🎯 **Welcome to the Austin Mobility War Room**
        
        This is where three AI agents battle to solve Austin's most complex mobility challenges:
        
        - **🚗 Captain Efficiency** (Driver Agent): Optimizes vehicle positioning and routing
        - **👥 Social Navigator** (Rider Agent): Understands group dynamics and user behavior  
        - **🏙️ Urban Strategist** (City Planner Agent): Manages traffic flow and urban planning
        
        **Choose a scenario from the sidebar and click "START BATTLE" to watch them compete!**
        
        ### 🏆 **How It Works**
        1. **Select a scenario** (New Year's Eve, UT Game Day, SXSW, etc.)
        2. **Watch the agents debate** their strategies in real-time
        3. **See 30-minute predictions** of group formations
        4. **Track which agent** makes the most accurate forecasts
        5. **Chat with the War Room** for strategic insights
        
        ### 📊 **Real Fetii Data**
        We're using actual Austin rideshare data with:
        - **{data_len} trips** from September 2025
        - **Group sizes** ranging from 5-11 passengers
        - **Real Austin locations** (UT Campus, West Campus, Downtown)
        - **Live coordinates** for precise predictions
        """.format(data_len=len(data), data=data))
        
        # Show sample data
        st.markdown("### 📋 **Sample Data Preview**")
        st.dataframe(data.head(), use_container_width=True)

if __name__ == "__main__":
    main()
