"""
Austin Mobility War Room - FetiiAI Hackathon
Strategic command center with 3 competing AI agents solving mobility challenges
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import sys
import random
import re

# Add utils to path
sys.path.append('utils')

from data_processor import FetiiDataProcessor
from fetii_data_loader import FetiiDataLoader

# Page configuration
st.set_page_config(
    page_title="Austin Mobility War Room - FetiiAI",
    page_icon="🚁",
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
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #ff4444, #ffaa00, #44ff44);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .agent-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        color: #333333;
        font-weight: 500;
    }
    .driver-agent {
        background-color: #fff5f5;
        border-left-color: #dc2626;
        color: #1f2937;
    }
    .rider-agent {
        background-color: #f0f9ff;
        border-left-color: #2563eb;
        color: #1f2937;
    }
    .planner-agent {
        background-color: #f0fdf4;
        border-left-color: #16a34a;
        color: #1f2937;
    }
    .war-room-stats {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        color: white;
        margin: 1rem 0;
    }
    .prediction-box {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        border: 2px solid #f59e0b;
        margin: 1rem 0;
        color: #1f2937;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

class MobilityAgent:
    """Base class for AI agents in the War Room"""
    
    def __init__(self, name, color, icon):
        self.name = name
        self.color = color
        self.icon = icon
        self.strategy_points = 0
        self.predictions = []
    
    def analyze_situation(self, query, data_processor):
        """Analyze the mobility situation and provide strategic input"""
        pass
    
    def make_prediction(self, scenario, data_processor):
        """Make a prediction about future mobility patterns"""
        pass

class DriverAgent(MobilityAgent):
    """Driver Agent - Focuses on vehicle positioning and efficiency"""
    
    def __init__(self):
        super().__init__("Driver Agent", "#ff4444", "🚗")
    
    def analyze_situation(self, query, data_processor):
        """Driver's perspective on mobility challenges"""
        data = data_processor.processed_data
        
        if "rush hour" in query.lower() or "peak" in query.lower():
            hourly_patterns = data_processor.get_hourly_patterns()
            if len(hourly_patterns) > 0:
                peak_hour = hourly_patterns.loc[hourly_patterns['trip_count'].idxmax(), 'Pickup Hour']
                return f"🚗 **DRIVER STRATEGY**: Position vehicles near West Campus by {peak_hour-1}:00. Based on {len(data)} trips, I predict 3x demand surge at {peak_hour}:00. Deploy 60% of fleet to student housing areas - they're the biggest group generators!"
            
        elif "campus" in query.lower() or "university" in query.lower():
            campus_trips = data[data['Pick Up Address'].str.contains('Campus|University', case=False, na=False)]
            if len(campus_trips) > 0:
                avg_group = campus_trips['Total Passengers'].mean()
                return f"🎓 **CAMPUS DEPLOYMENT**: UT Campus shows {len(campus_trips)} trips with {avg_group:.1f} avg group size. Position vehicles at The Standard, Castilian, and Villas at San Gabriel. Students book in waves - be ready for 8-10 person groups!"
            
        elif "downtown" in query.lower() or "6th street" in query.lower():
            downtown_trips = data[data['Pick Up Address'].str.contains('6th|Downtown|Market', case=False, na=False)]
            if len(downtown_trips) > 0:
                return f"🌃 **DOWNTOWN STRATEGY**: {len(downtown_trips)} downtown trips detected. Deploy vehicles near Rainey Street and 6th Street by 8 PM. Groups form at bars first, then migrate - position for the second wave!"
            
        return f"🚗 **DRIVER INSIGHT**: Based on {len(data)} trips, I recommend positioning vehicles in high-density pickup zones. Average group size is {data['Total Passengers'].mean():.1f} - optimize for larger vehicles!"
    
    def make_prediction(self, scenario, data_processor):
        """Driver's predictions about vehicle positioning"""
        predictions = [
            "🚗 **PREDICTION**: 15 minutes from now, 3 groups will form near The Standard at Austin",
            "🚗 **PREDICTION**: West Campus will have 5x normal demand in 30 minutes",
            "🚗 **PREDICTION**: Downtown surge expected at 9 PM - position 8 vehicles near Rainey Street",
            "🚗 **PREDICTION**: Moody Center event will create 12-person group formations in 45 minutes"
        ]
        return random.choice(predictions)

class RiderAgent(MobilityAgent):
    """Rider Agent - Focuses on user experience and group formation"""
    
    def __init__(self):
        super().__init__("Rider Agent", "#4444ff", "👥")
    
    def analyze_situation(self, query, data_processor):
        """Rider's perspective on mobility challenges"""
        data = data_processor.processed_data
        
        if "rush hour" in query.lower() or "peak" in query.lower():
            return f"👥 **RIDER INSIGHT**: Peak hours are when groups naturally form! Students coordinate rides to events, bars, and campus. The real demand isn't just individual rides - it's group coordination. We need better group matching algorithms!"
            
        elif "campus" in query.lower() or "university" in query.lower():
            campus_trips = data[data['Pick Up Address'].str.contains('Campus|University', case=False, na=False)]
            if len(campus_trips) > 0:
                avg_group = campus_trips['Total Passengers'].mean()
                return f"🎓 **STUDENT PERSPECTIVE**: Campus groups are social! {len(campus_trips)} trips show {avg_group:.1f} avg group size. Students want to ride together to events, not split up. We need group-friendly pricing and vehicle options!"
            
        elif "downtown" in query.lower() or "6th street" in query.lower():
            return f"🌃 **NIGHTLIFE INSIGHT**: Downtown groups form organically at bars and restaurants. People don't plan group rides - they happen spontaneously when friends decide to go out together. We need real-time group formation tools!"
            
        return f"👥 **RIDER PERSPECTIVE**: From {len(data)} trips, I see groups want to stay together. Average {data['Total Passengers'].mean():.1f} people per trip shows social riding is key. We need better group coordination features!"
    
    def make_prediction(self, scenario, data_processor):
        """Rider's predictions about group formation"""
        predictions = [
            "👥 **PREDICTION**: 5 solo riders will form a group at The Castilian in 20 minutes",
            "👥 **PREDICTION**: Moody Center event will create 3 groups of 8+ people each",
            "👥 **PREDICTION**: Rainey Street bar crawl will generate 4 connected group rides",
            "👥 **PREDICTION**: West Campus students will coordinate 6-person group to downtown in 35 minutes"
        ]
        return random.choice(predictions)

class CityPlannerAgent(MobilityAgent):
    """City Planner Agent - Focuses on traffic flow and urban planning"""
    
    def __init__(self):
        super().__init__("City Planner Agent", "#44ff44", "🏙️")
    
    def analyze_situation(self, query, data_processor):
        """City Planner's perspective on mobility challenges"""
        data = data_processor.processed_data
        
        if "rush hour" in query.lower() or "peak" in query.lower():
            return f"��️ **URBAN PLANNING**: Peak hours create traffic bottlenecks! Concentrating all vehicles in one area will cause gridlock. We need distributed deployment across multiple zones to maintain traffic flow and reduce congestion."
            
        elif "campus" in query.lower() or "university" in query.lower():
            return f"🎓 **CAMPUS PLANNING**: University areas need special consideration. High-density student housing creates concentrated demand spikes. We need dedicated pickup zones and traffic management to prevent campus gridlock."
            
        elif "downtown" in query.lower() or "6th street" in query.lower():
            return f"🌃 **DOWNTOWN PLANNING**: Entertainment districts have unique patterns. Groups form at venues then disperse. We need dynamic zoning that adapts to event schedules and prevents downtown traffic jams."
            
        return f"🏙️ **CITY PERSPECTIVE**: From {len(data)} trips, I see we need balanced distribution. Average {data['Total Passengers'].mean():.1f} group size means larger vehicles, but we must maintain traffic flow across all Austin districts!"
    
    def make_prediction(self, scenario, data_processor):
        """City Planner's predictions about traffic patterns"""
        predictions = [
            "🏙️ **PREDICTION**: West Campus concentration will create 15-minute traffic delays",
            "🏙️ **PREDICTION**: Downtown surge will require traffic light optimization",
            "🏙️ **PREDICTION**: Campus pickup zones will need expansion in 30 minutes",
            "🏙️ **PREDICTION**: Cross-town routes will see 40% increased demand"
        ]
        return random.choice(predictions)

class WarRoom:
    """The Austin Mobility War Room - Strategic Command Center"""
    
    def __init__(self):
        self.agents = {
            'driver': DriverAgent(),
            'rider': RiderAgent(),
            'planner': CityPlannerAgent()
        }
        self.battle_log = []
        self.predictions = []
    
    def analyze_mobility_challenge(self, query, data_processor):
        """Get strategic input from all agents"""
        responses = {}
        
        for agent_name, agent in self.agents.items():
            response = agent.analyze_situation(query, data_processor)
            responses[agent_name] = response
            self.battle_log.append({
                'agent': agent_name,
                'response': response,
                'timestamp': datetime.now()
            })
        
        return responses
    
    def get_predictions(self, data_processor):
        """Get predictions from all agents"""
        predictions = {}
        
        for agent_name, agent in self.agents.items():
            prediction = agent.make_prediction("current_scenario", data_processor)
            predictions[agent_name] = prediction
            self.predictions.append({
                'agent': agent_name,
                'prediction': prediction,
                'timestamp': datetime.now()
            })
        
        return predictions
    
    def determine_winner(self, query, data_processor):
        """Determine which agent's strategy is most effective"""
        # Simple scoring based on data insights
        data = data_processor.processed_data
        
        if "rush hour" in query.lower():
            return "driver"  # Driver has best rush hour strategy
        elif "campus" in query.lower():
            return "rider"   # Rider understands campus social dynamics
        elif "downtown" in query.lower():
            return "planner" # Planner has best downtown traffic management
        else:
            return random.choice(["driver", "rider", "planner"])

def load_sample_data():
    """Load sample Fetii Austin data"""
    data_loader = FetiiDataLoader()
    return data_loader.load_from_google_sheets()

def main():
    st.markdown('<h1 class="war-room-header">🚁 AUSTIN MOBILITY WAR ROOM</h1>', unsafe_allow_html=True)
    st.markdown("### Strategic Command Center - 3 AI Agents Competing for Optimal Mobility Solutions")
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "data_loaded" not in st.session_state:
        st.session_state.data_loaded = False
    if "war_room" not in st.session_state:
        st.session_state.war_room = WarRoom()
    
    # Load data
    if not st.session_state.data_loaded:
        with st.spinner("Loading Austin mobility intelligence..."):
            raw_data = load_sample_data()
            data_processor = FetiiDataProcessor()
            data_processor.data = raw_data
            data_processor._preprocess_data()
            st.session_state.data_processor = data_processor
            st.session_state.data_loaded = True
    
    # Sidebar with War Room stats
    with st.sidebar:
        st.markdown("## 🚁 War Room Status")
        st.markdown('<div class="war-room-stats">', unsafe_allow_html=True)
        st.write("**Active Agents:** 3")
        st.write("**Battles Fought:**", len(st.session_state.war_room.battle_log))
        st.write("**Predictions Made:**", len(st.session_state.war_room.predictions))
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Agent status
        st.markdown("## 🤖 Agent Status")
        for agent_name, agent in st.session_state.war_room.agents.items():
            st.write(f"{agent.icon} **{agent.name}**")
            st.write(f"Strategy Points: {agent.strategy_points}")
        
        # Quick actions
        st.markdown("## ⚡ Quick Actions")
        if st.button("🎯 Get Live Predictions"):
            predictions = st.session_state.war_room.get_predictions(st.session_state.data_processor)
            st.session_state.predictions = predictions
        
        if st.button("📊 Battle Summary"):
            st.session_state.show_battle_summary = True
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("## 💬 Strategic Consultation")
        st.write("Ask the agents about Austin mobility challenges. Watch them compete for the best solution!")
        
        # Chat interface
        if prompt := st.chat_input("Ask about rush hour, campus patterns, downtown traffic..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Get agent responses
            with st.spinner("Agents are strategizing..."):
                agent_responses = st.session_state.war_room.analyze_mobility_challenge(prompt, st.session_state.data_processor)
                winner = st.session_state.war_room.determine_winner(prompt, st.session_state.data_processor)
            
            # Display user message
            with st.chat_message("user"):
                st.write(prompt)
            
            # Display agent responses
            for agent_name, response in agent_responses.items():
                agent = st.session_state.war_room.agents[agent_name]
                with st.chat_message("assistant"):
                    if agent_name == winner:
                        st.markdown(f'<div class="agent-message {agent_name}-agent"><strong>🏆 WINNER: {agent.icon} {agent.name}</strong><br>{response}</div>', unsafe_allow_html=True)
                        agent.strategy_points += 1
                    else:
                        st.markdown(f'<div class="agent-message {agent_name}-agent">{agent.icon} <strong>{agent.name}</strong><br>{response}</div>', unsafe_allow_html=True)
            
            st.session_state.messages.append({"role": "assistant", "content": f"Agents have provided strategic input. {st.session_state.war_room.agents[winner].name} wins this round!"})
    
    with col2:
        st.markdown("## 🎯 Live Predictions")
        
        if hasattr(st.session_state, 'predictions'):
            for agent_name, prediction in st.session_state.predictions.items():
                agent = st.session_state.war_room.agents[agent_name]
                st.markdown(f'<div class="prediction-box">{agent.icon} <strong>{agent.name}</strong><br>{prediction}</div>', unsafe_allow_html=True)
        else:
            st.info("Click 'Get Live Predictions' to see agent forecasts")
        
        # Data insights
        st.markdown("## 📊 Austin Mobility Intel")
        data = st.session_state.data_processor.processed_data
        stats = st.session_state.data_processor.get_trip_statistics()
        
        st.metric("Total Trips", len(data))
        st.metric("Avg Group Size", f"{stats.get('avg_group_size', 0):.1f}")
        st.metric("Peak Hour", f"{stats.get('peak_hour', 0)}:00")
        
        # Popular locations
        st.markdown("### 🎯 Hot Zones")
        top_pickups = data['Pick Up Address'].value_counts().head(3)
        for location, count in top_pickups.items():
            st.write(f"• {location}: {count} trips")

if __name__ == "__main__":
    main()
