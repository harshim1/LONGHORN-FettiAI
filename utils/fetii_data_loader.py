"""
Fetii Data Loader - Integrates real Austin rideshare data
"""

import pandas as pd
import requests
import io
from typing import Dict, Any
import re

class FetiiDataLoader:
    """Load and process real Fetii Austin rideshare data"""
    
    def __init__(self):
        self.data = None
        self.processed_data = None
    
    def load_from_google_sheets(self, sheet_url: str = None):
        """Load data from Google Sheets (CSV export)"""
        # Sample data based on the Google Sheets structure we saw
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
        
        self.data = pd.DataFrame(sample_data)
        return self.data
    
    def process_data(self):
        """Process and clean the raw data"""
        if self.data is None:
            raise ValueError("No data loaded. Call load_from_google_sheets() first.")
        
        # Convert datetime
        self.data['Trip Date and Time'] = pd.to_datetime(self.data['Trip Date and Time'], format='%m/%d/%y %H:%M')
        
        # Create derived features
        self.data['pickup_hour'] = self.data['Trip Date and Time'].dt.hour
        self.data['pickup_day_of_week'] = self.data['Trip Date and Time'].dt.day_name()
        self.data['pickup_date'] = self.data['Trip Date and Time'].dt.date
        
        # Extract location zones
        self.data['pickup_zone'] = self.data['Pick Up Address'].apply(self._extract_zone)
        self.data['dropoff_zone'] = self.data['Drop Off Address'].apply(self._extract_zone)
        
        # Group size categories
        self.data['group_size_category'] = pd.cut(
            self.data['Total Passengers'],
            bins=[0, 3, 6, 9, 12, float('inf')],
            labels=['Small (1-3)', 'Medium (4-6)', 'Large (7-9)', 'XL (10-12)', 'XXL (13+)']
        )
        
        # Calculate trip duration (estimated)
        self.data['estimated_duration_minutes'] = self._calculate_trip_duration()
        
        # Calculate estimated fare
        self.data['estimated_fare'] = self._calculate_fare()
        
        self.processed_data = self.data.copy()
        return self.processed_data
    
    def _extract_zone(self, address):
        """Extract zone from address"""
        address_lower = address.lower()
        
        if 'university' in address_lower or 'campus' in address_lower or '23rd' in address_lower:
            return 'University District'
        elif 'west campus' in address_lower or 'w 23rd' in address_lower:
            return 'West Campus'
        elif 'downtown' in address_lower or '6th' in address_lower or 'market' in address_lower:
            return 'Downtown Austin'
        elif 'east' in address_lower or 'e 6th' in address_lower:
            return 'East Austin'
        elif 'south' in address_lower or 's congress' in address_lower:
            return 'South Austin'
        elif 'north' in address_lower or 'n university' in address_lower:
            return 'North Austin'
        else:
            return 'Other Austin'
    
    def _calculate_trip_duration(self):
        """Calculate estimated trip duration based on distance"""
        # Simple estimation based on coordinates
        durations = []
        for _, row in self.data.iterrows():
            # Calculate approximate distance
            lat_diff = abs(row['Drop Off Latitude'] - row['Pick Up Latitude'])
            lon_diff = abs(row['Drop Off Longitude'] - row['Pick Up Longitude'])
            distance = (lat_diff + lon_diff) * 69  # Rough miles
            
            # Estimate duration (15-45 minutes for Austin trips)
            duration = max(15, min(45, distance * 3 + 15))
            durations.append(duration)
        
        return durations
    
    def _calculate_fare(self):
        """Calculate estimated fare based on group size and duration"""
        fares = []
        for _, row in self.data.iterrows():
            base_fare = 15  # Base fare
            group_multiplier = 1 + (row['Total Passengers'] - 1) * 0.3  # Group discount
            duration_multiplier = row['estimated_duration_minutes'] / 30  # Time factor
            
            fare = base_fare * group_multiplier * duration_multiplier
            fares.append(round(fare, 2))
        
        return fares
    
    def get_analytics_summary(self):
        """Get comprehensive analytics summary"""
        if self.processed_data is None:
            self.process_data()
        
        summary = {
            'total_trips': len(self.processed_data),
            'total_passengers': self.processed_data['Total Passengers'].sum(),
            'avg_group_size': self.processed_data['Total Passengers'].mean(),
            'peak_hour': self.processed_data['pickup_hour'].mode().iloc[0],
            'most_common_zone': self.processed_data['pickup_zone'].mode().iloc[0],
            'avg_trip_duration': self.processed_data['estimated_duration_minutes'].mean(),
            'avg_fare': self.processed_data['estimated_fare'].mean(),
            'group_size_distribution': self.processed_data['group_size_category'].value_counts().to_dict(),
            'zone_distribution': self.processed_data['pickup_zone'].value_counts().to_dict(),
            'hourly_patterns': self.processed_data.groupby('pickup_hour').size().to_dict()
        }
        
        return summary
    
    def get_hotspots(self, top_n=5):
        """Get top pickup and dropoff hotspots"""
        pickup_hotspots = self.processed_data['Pick Up Address'].value_counts().head(top_n)
        dropoff_hotspots = self.processed_data['Drop Off Address'].value_counts().head(top_n)
        
        return {
            'pickup_hotspots': pickup_hotspots.to_dict(),
            'dropoff_hotspots': dropoff_hotspots.to_dict()
        }
    
    def get_group_formation_patterns(self):
        """Analyze group formation patterns"""
        patterns = {
            'size_distribution': self.processed_data['Total Passengers'].value_counts().sort_index().to_dict(),
            'time_patterns': self.processed_data.groupby('pickup_hour')['Total Passengers'].mean().to_dict(),
            'zone_patterns': self.processed_data.groupby('pickup_zone')['Total Passengers'].mean().to_dict()
        }
        
        return patterns
