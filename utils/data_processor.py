"""
Data processing utilities for Fetii rideshare data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re

class FetiiDataProcessor:
    """Process and analyze Fetii rideshare data"""
    
    def __init__(self, data_path=None):
        self.data = None
        self.processed_data = None
        if data_path:
            self.load_data(data_path)
    
    def load_data(self, data_path):
        """Load data from CSV or other formats"""
        try:
            if data_path.endswith('.csv'):
                self.data = pd.read_csv(data_path)
            elif data_path.endswith('.json'):
                self.data = pd.read_json(data_path)
            else:
                raise ValueError("Unsupported file format")
            
            self._preprocess_data()
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def _preprocess_data(self):
        """Clean and preprocess the raw data"""
        if self.data is None:
            return
        
        # Convert datetime columns
        datetime_columns = ['Trip Date and Time', 'Drop Off Time', 'created_at', 'updated_at']
        for col in datetime_columns:
            if col in self.data.columns:
                self.data[col] = pd.to_datetime(self.data[col], errors='coerce')
        
        # Clean address data
        address_columns = ['Pick Up Address', 'Drop Off Address']
        for col in address_columns:
            if col in self.data.columns:
                self.data[col] = self.data[col].astype(str).str.strip()
        
        # Handle missing values
        self.data = self.data.fillna({
            'Total Passengers': 1,
            'Rider Age': self.data['Rider Age'].median() if 'Rider Age' in self.data.columns else 30,
            'Trip Duration': 30,
            'Fare Amount': self.data['Fare Amount'].median() if 'Fare Amount' in self.data.columns else 25
        })
        
        # Create derived features
        self._create_derived_features()
        
        self.processed_data = self.data.copy()
    
    def _create_derived_features(self):
        """Create additional features for analysis"""
        # Time-based features
        if 'Trip Date and Time' in self.data.columns:
            self.data['Pickup Hour'] = self.data['Trip Date and Time'].dt.hour
            self.data['pickup_day_of_week'] = self.data['Trip Date and Time'].dt.day_name()
            self.data['pickup_month'] = self.data['Trip Date and Time'].dt.month
            self.data['pickup_date'] = self.data['Trip Date and Time'].dt.date
        
        # Location-based features
        if 'Pick Up Latitude' in self.data.columns and 'Pick Up Longitude' in self.data.columns:
            self.data['pickup_zone'] = self._create_location_zones(
                self.data['Pick Up Latitude'], 
                self.data['Pick Up Longitude']
            )
        
        if 'Drop Off Latitude' in self.data.columns and 'Drop Off Longitude' in self.data.columns:
            self.data['dropoff_zone'] = self._create_location_zones(
                self.data['Drop Off Latitude'], 
                self.data['Drop Off Longitude']
            )
        
        # Group size categories
        if 'Total Passengers' in self.data.columns:
            self.data['group_size_category'] = pd.cut(
                self.data['Total Passengers'],
                bins=[0, 2, 4, 6, 8, float('inf')],
                labels=['Small (1-2)', 'Medium (3-4)', 'Large (5-6)', 'XL (7-8)', 'XXL (9+)']
            )
        
        # Age groups
        if 'Rider Age' in self.data.columns:
            self.data['age_group'] = pd.cut(
                self.data['Rider Age'],
                bins=[0, 25, 35, 45, 55, 100],
                labels=['18-25', '26-35', '36-45', '46-55', '55+']
            )
    
    def _create_location_zones(self, lat, lon):
        """Create location zones based on coordinates"""
        # Austin area zones (simplified)
        zones = []
        for i in range(len(lat)):
            if pd.isna(lat.iloc[i]) or pd.isna(lon.iloc[i]):
                zones.append('Unknown')
            elif 30.2 <= lat.iloc[i] <= 30.4 and -97.9 <= lon.iloc[i] <= -97.6:
                zones.append('Downtown Austin')
            elif 30.1 <= lat.iloc[i] <= 30.3 and -97.8 <= lon.iloc[i] <= -97.6:
                zones.append('South Austin')
            elif 30.3 <= lat.iloc[i] <= 30.5 and -97.8 <= lon.iloc[i] <= -97.6:
                zones.append('North Austin')
            elif 30.2 <= lat.iloc[i] <= 30.4 and -97.9 <= lon.iloc[i] <= -97.7:
                zones.append('East Austin')
            elif 30.2 <= lat.iloc[i] <= 30.4 and -97.7 <= lon.iloc[i] <= -97.5:
                zones.append('West Austin')
            else:
                zones.append('Outer Austin')
        return zones
    
    def get_trip_statistics(self):
        """Get basic trip statistics"""
        if self.processed_data is None:
            return {}
        
        stats = {
            'total_trips': len(self.processed_data),
            'avg_group_size': self.processed_data['Total Passengers'].mean() if 'Total Passengers' in self.processed_data.columns else 0,
            'avg_trip_duration': 30.0,  # Default value since we don't have this data
            'avg_fare': 25.0,  # Default value since we don't have this data
            'peak_hour': self.processed_data['Pickup Hour'].mode().iloc[0] if 'Pickup Hour' in self.processed_data.columns else 21,
            'most_common_group_size': self.processed_data['Total Passengers'].mode().iloc[0] if 'Total Passengers' in self.processed_data.columns else 8,
            'avg_rider_age': 25.0  # Default value since we don't have this data
        }
        
        return stats
    
    def filter_by_location(self, location_name):
        """Filter trips by location (pickup or dropoff)"""
        if self.processed_data is None:
            return pd.DataFrame()
        
        location_filter = (
            self.processed_data['Pick Up Address'].str.contains(location_name, case=False, na=False) |
            self.processed_data['Drop Off Address'].str.contains(location_name, case=False, na=False)
        )
        
        return self.processed_data[location_filter]
    
    def filter_by_time_range(self, start_date, end_date):
        """Filter trips by date range"""
        if self.processed_data is None or 'Trip Date and Time' not in self.processed_data.columns:
            return pd.DataFrame()
        
        return self.processed_data[
            (self.processed_data['Trip Date and Time'] >= start_date) &
            (self.processed_data['Trip Date and Time'] <= end_date)
        ]
    
    def filter_by_group_size(self, min_size, max_size):
        """Filter trips by group size range"""
        if self.processed_data is None:
            return pd.DataFrame()
        
        return self.processed_data[
            (self.processed_data['Total Passengers'] >= min_size) &
            (self.processed_data['Total Passengers'] <= max_size)
        ]
    
    def get_popular_destinations(self, top_n=10):
        """Get most popular destinations"""
        if self.processed_data is None:
            return pd.DataFrame()
        
        return self.processed_data['Drop Off Address'].value_counts().head(top_n)
    
    def get_hourly_patterns(self):
        """Get hourly trip patterns"""
        if self.processed_data is None or 'Pickup Hour' not in self.processed_data.columns:
            return pd.DataFrame()
        
        hourly_data = self.processed_data.groupby('Pickup Hour').size().reset_index(name='trip_count')
        return hourly_data
    
    def get_demographic_insights(self):
        """Get demographic insights"""
        if self.processed_data is None:
            return {}
        
        insights = {}
        
        if 'age_group' in self.processed_data.columns:
            insights['age_distribution'] = self.processed_data['age_group'].value_counts()
        
        if 'group_size_category' in self.processed_data.columns:
            insights['group_size_distribution'] = self.processed_data['group_size_category'].value_counts()
        
        return insights
