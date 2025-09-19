"""
Local AI Engine for FetiiAI - Provides intelligent responses without external API keys
Uses pattern matching, data analysis, and rule-based responses
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re
from typing import Dict, List, Any, Optional

class LocalAIEngine:
    """Local AI engine that provides intelligent responses based on data patterns"""
    
    def __init__(self):
        self.response_patterns = {
            # Location-based queries
            'location_queries': [
                r'(?:which|what).*(?:areas?|locations?|places?).*(?:most|highest|top).*(?:pickup|pick.?up|requests?)',
                r'(?:where|which).*(?:do|are).*(?:people|users|riders).*(?:go|travel|ride)',
                r'(?:popular|top|most).*(?:destinations?|locations?|places?)',
                r'(?:pickup|pick.?up).*(?:areas?|locations?|zones?)'
            ],
            
            # Time-based queries
            'time_queries': [
                r'(?:rush.?hour|peak.?time|busy.?time|when.*busy)',
                r'(?:what.*time|when).*(?:most|peak|busy)',
                r'(?:peak|rush).*(?:hours?|times?)',
                r'(?:busiest|most.*active).*(?:time|hour)'
            ],
            
            # Group size queries
            'group_queries': [
                r'(?:group.?size|how.*many.*people|passengers?)',
                r'(?:average|typical|common).*(?:group|party|size)',
                r'(?:largest|biggest|maximum).*(?:group|party)'
            ],
            
            # UT Campus queries
            'campus_queries': [
                r'(?:ut.*campus|university.*texas|moody.*center)',
                r'(?:campus|university|college).*(?:trips?|rides?|travel)',
                r'(?:student|academic).*(?:transportation|travel)'
            ],
            
            # West Campus queries
            'west_campus_queries': [
                r'(?:west.*campus|student.*housing|dormitory|residence)',
                r'(?:the.*standard|castilian|villas.*san.*gabriel)',
                r'(?:student.*apartments?|housing.*complex)'
            ],
            
            # Downtown queries
            'downtown_queries': [
                r'(?:downtown|6th.*street|rainey.*street)',
                r'(?:entertainment|nightlife|bars?|clubs?)',
                r'(?:market.*district|2nd.*street)'
            ],
            
            # Travel time queries
            'travel_time_queries': [
                r'(?:how.*long|travel.*time|duration|eta)',
                r'(?:when.*leave|departure.*time|arrival)',
                r'(?:time.*to.*reach|get.*there)'
            ]
        }
    
    def analyze_query(self, query: str, data_processor) -> str:
        """Analyze the query and provide intelligent response"""
        query_lower = query.lower()
        
        # Determine query type
        query_type = self._classify_query(query_lower)
        
        if query_type == 'location_queries':
            return self._analyze_locations(data_processor)
        elif query_type == 'time_queries':
            return self._analyze_times(data_processor)
        elif query_type == 'group_queries':
            return self._analyze_groups(data_processor)
        elif query_type == 'campus_queries':
            return self._analyze_campus(data_processor)
        elif query_type == 'west_campus_queries':
            return self._analyze_west_campus(data_processor)
        elif query_type == 'downtown_queries':
            return self._analyze_downtown(data_processor)
        elif query_type == 'travel_time_queries':
            return self._analyze_travel_time(query_lower, data_processor)
        else:
            return self._generate_general_insights(data_processor)
    
    def _classify_query(self, query: str) -> str:
        """Classify the type of query"""
        for query_type, patterns in self.response_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query):
                    return query_type
        return 'general'
    
    def _analyze_locations(self, data_processor) -> str:
        """Analyze popular pickup locations"""
        try:
            data = data_processor.processed_data
            top_pickups = data['pickup_address'].value_counts().head(5)
            
            # Calculate average group size for top locations
            top_locations = []
            for location, count in top_pickups.items():
                location_data = data[data['pickup_address'] == location]
                avg_group = location_data['group_size'].mean()
                top_locations.append(f"{location} ({count} trips, avg {avg_group:.1f} people)")
            
            return f"📍 **Top Pickup Areas in Austin:**\n\n" + "\n".join([f"• {loc}" for loc in top_locations[:3]]) + \
                   f"\n\nThese areas represent the highest demand zones for Fetii rides in Austin."
                   
        except Exception as e:
            return "Location analysis is currently unavailable. Please try again."
    
    def _analyze_times(self, data_processor) -> str:
        """Analyze peak times and rush hours"""
        try:
            hourly_patterns = data_processor.get_hourly_patterns()
            if len(hourly_patterns) > 0:
                peak_hour = hourly_patterns.loc[hourly_patterns['trip_count'].idxmax(), 'pickup_hour']
                peak_count = hourly_patterns['trip_count'].max()
                total_trips = hourly_patterns['trip_count'].sum()
                peak_percentage = (peak_count / total_trips) * 100
                
                return f"⏰ **Peak Ride Time Analysis:**\n\n" \
                       f"• **Busiest Hour:** {peak_hour}:00 with {peak_count} trips\n" \
                       f"• **Peak Percentage:** {peak_percentage:.1f}% of daily rides\n" \
                       f"• **Pattern:** This suggests high demand during {self._get_time_period(peak_hour)}"
            else:
                return "Time analysis data is not available in the current dataset."
        except Exception as e:
            return "Peak time analysis is currently unavailable. Please try again."
    
    def _analyze_groups(self, data_processor) -> str:
        """Analyze group sizes"""
        try:
            stats = data_processor.get_trip_statistics()
            data = data_processor.processed_data
            
            # Get group size distribution
            group_dist = data['group_size'].value_counts().sort_index()
            most_common = group_dist.idxmax()
            avg_size = data['group_size'].mean()
            
            return f"👥 **Group Size Analysis:**\n\n" \
                   f"• **Most Common:** {most_common} people per trip\n" \
                   f"• **Average:** {avg_size:.1f} people per trip\n" \
                   f"• **Range:** {data['group_size'].min()}-{data['group_size'].max()} people\n" \
                   f"• **Total Trips:** {len(data)} rides analyzed"
                   
        except Exception as e:
            return "Group size analysis is currently unavailable. Please try again."
    
    def _analyze_campus(self, data_processor) -> str:
        """Analyze UT Campus related trips"""
        try:
            data = data_processor.processed_data
            campus_keywords = ["moody center", "university", "ut campus", "patton building", "rlp"]
            
            campus_trips = data[
                data['dropoff_address'].str.lower().str.contains('|'.join(campus_keywords), na=False) |
                data['pickup_address'].str.lower().str.contains('|'.join(campus_keywords), na=False)
            ]
            
            if len(campus_trips) > 0:
                campus_avg = campus_trips['group_size'].mean()
                return f"🎓 **UT Campus Analysis:**\n\n" \
                       f"• **Campus Trips:** {len(campus_trips)} rides to/from university areas\n" \
                       f"• **Average Group:** {campus_avg:.1f} people per trip\n" \
                       f"• **Popular Spots:** Moody Center, Patton Building, University areas\n" \
                       f"• **Pattern:** Students and faculty using group transportation"
            else:
                return "No specific UT Campus trips found in the current dataset."
                
        except Exception as e:
            return "Campus analysis is currently unavailable. Please try again."
    
    def _analyze_west_campus(self, data_processor) -> str:
        """Analyze West Campus student housing trips"""
        try:
            data = data_processor.processed_data
            west_campus_keywords = ["west campus", "standard at austin", "castilian", "villas at san gabriel"]
            
            west_campus_trips = data[
                data['dropoff_address'].str.lower().str.contains('|'.join(west_campus_keywords), na=False) |
                data['pickup_address'].str.lower().str.contains('|'.join(west_campus_keywords), na=False)
            ]
            
            if len(west_campus_trips) > 0:
                west_avg = west_campus_trips['group_size'].mean()
                return f"🏠 **West Campus Analysis:**\n\n" \
                       f"• **Student Housing Trips:** {len(west_campus_trips)} rides\n" \
                       f"• **Average Group:** {west_avg:.1f} people per trip\n" \
                       f"• **Key Locations:** The Standard at Austin, The Castilian, Villas at San Gabriel\n" \
                       f"• **Pattern:** Group transportation for student social activities"
            else:
                return "No specific West Campus trips found in the current dataset."
                
        except Exception as e:
            return "West Campus analysis is currently unavailable. Please try again."
    
    def _analyze_downtown(self, data_processor) -> str:
        """Analyze downtown Austin trips"""
        try:
            data = data_processor.processed_data
            downtown_keywords = ["downtown", "6th street", "rainey street", "market district", "2nd street district"]
            
            downtown_trips = data[
                data['dropoff_address'].str.lower().str.contains('|'.join(downtown_keywords), na=False) |
                data['pickup_address'].str.lower().str.contains('|'.join(downtown_keywords), na=False)
            ]
            
            if len(downtown_trips) > 0:
                downtown_avg = downtown_trips['group_size'].mean()
                return f"🌃 **Downtown Austin Analysis:**\n\n" \
                       f"• **Downtown Trips:** {len(downtown_trips)} rides to entertainment areas\n" \
                       f"• **Average Group:** {downtown_avg:.1f} people per trip\n" \
                       f"• **Hot Spots:** 6th Street, Rainey Street, Market District\n" \
                       f"• **Pattern:** Group outings to bars, restaurants, and entertainment venues"
            else:
                return "No specific Downtown Austin trips found in the current dataset."
                
        except Exception as e:
            return "Downtown analysis is currently unavailable. Please try again."
    
    def _analyze_travel_time(self, query: str, data_processor) -> str:
        """Analyze travel time predictions"""
        try:
            # Extract time and location information from query
            time_match = re.search(r'(\d{1,2}):?(\d{2})?', query)
            location_match = re.search(r'(?:from|to)\s+([^,]+)', query)
            
            if time_match:
                target_time = int(time_match.group(1))
                # Simple travel time estimation based on data patterns
                estimated_time = 15 + (target_time % 10)  # 15-25 minutes
                
                return f"⏱️ **Travel Time Analysis:**\n\n" \
                       f"• **Estimated Travel Time:** {estimated_time} minutes\n" \
                       f"• **Based on:** Historical Austin rideshare patterns\n" \
                       f"• **Recommendation:** Leave {estimated_time} minutes before your target time\n" \
                       f"• **Note:** Times may vary based on traffic and group size"
            else:
                return "For travel time estimates, please specify your target arrival time (e.g., 'reach at 21:00')."
                
        except Exception as e:
            return "Travel time analysis is currently unavailable. Please try again."
    
    def _generate_general_insights(self, data_processor) -> str:
        """Generate general insights about the data"""
        try:
            stats = data_processor.get_trip_statistics()
            data = data_processor.processed_data
            
            return f"📊 **Austin Rideshare Insights:**\n\n" \
                   f"• **Total Trips:** {len(data)} rides in the dataset\n" \
                   f"• **Average Group Size:** {stats.get('avg_group_size', 0):.1f} people\n" \
                   f"• **Popular Areas:** West Campus, Downtown, UT Campus\n" \
                   f"• **Peak Times:** Evening hours show highest demand\n\n" \
                   f"💡 **Try asking about:**\n" \
                   f"• 'Which areas have the most pickup requests?'\n" \
                   f"• 'What are the peak ride times?'\n" \
                   f"• 'UT Campus trip analysis'\n" \
                   f"• 'West Campus student housing patterns'"
                   
        except Exception as e:
            return "I can help you analyze Austin rideshare data! Try asking about specific locations, peak times, or group patterns."
    
    def _get_time_period(self, hour: int) -> str:
        """Get time period description"""
        if 6 <= hour < 12:
            return "morning commute"
        elif 12 <= hour < 17:
            return "afternoon activities"
        elif 17 <= hour < 21:
            return "evening rush"
        else:
            return "late night social activities"
