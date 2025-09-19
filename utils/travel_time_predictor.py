"""
Travel Time Predictor - ML model to predict departure times based on Fetii data
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import re
from datetime import datetime, timedelta

class TravelTimePredictor:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.location_encoder = LabelEncoder()
        self.is_trained = False
        
    def prepare_training_data(self, df):
        """Prepare training data from Fetii dataset"""
        # Calculate trip duration from coordinates (simplified)
        df['trip_duration'] = self._calculate_trip_duration(df)
        
        # Extract features
        features = []
        for _, row in df.iterrows():
            feature = {
                'pickup_zone': self._extract_zone(row['Pick Up Address']),
                'dropoff_zone': self._extract_zone(row['Drop Off Address']),
                'hour': row['Trip Date and Time'].hour,
                'day_of_week': row['Trip Date and Time'].weekday(),
                'group_size': row['Total Passengers'],
                'distance_estimate': self._estimate_distance(row)
            }
            features.append(feature)
        
        feature_df = pd.DataFrame(features)
        
        # Encode categorical variables
        feature_df['pickup_zone_encoded'] = self.location_encoder.fit_transform(feature_df['pickup_zone'])
        feature_df['dropoff_zone_encoded'] = self.location_encoder.transform(feature_df['dropoff_zone'])
        
        # Prepare training features
        X = feature_df[['pickup_zone_encoded', 'dropoff_zone_encoded', 'hour', 'day_of_week', 'group_size', 'distance_estimate']]
        y = df['trip_duration']
        
        return X, y
    
    def train(self, df):
        """Train the model on Fetii data"""
        X, y = self.prepare_training_data(df)
        self.model.fit(X, y)
        self.is_trained = True
        return self
    
    def predict_departure_time(self, pickup_location, dropoff_location, arrival_time, group_size=1):
        """Predict when to leave to arrive on time"""
        if not self.is_trained:
            return "Model not trained. Please train with data first."
        
        # Parse arrival time
        if isinstance(arrival_time, str):
            try:
                arrival_dt = datetime.strptime(arrival_time, "%H:%M")
            except:
                arrival_dt = datetime.strptime(arrival_time, "%H%M")
        else:
            arrival_dt = arrival_time
        
        # Extract features for prediction
        pickup_zone = self._extract_zone(pickup_location)
        dropoff_zone = self._extract_zone(dropoff_location)
        
        # Encode zones
        try:
            pickup_encoded = self.location_encoder.transform([pickup_zone])[0]
            dropoff_encoded = self.location_encoder.transform([dropoff_zone])[0]
        except ValueError:
            # Handle unknown zones
            pickup_encoded = 0
            dropoff_encoded = 0
        
        # Estimate distance
        distance = self._estimate_distance_from_zones(pickup_zone, dropoff_zone)
        
        # Prepare prediction features
        X_pred = np.array([[pickup_encoded, dropoff_encoded, arrival_dt.hour, arrival_dt.weekday(), group_size, distance]])
        
        # Predict travel time
        predicted_duration = self.model.predict(X_pred)[0]
        
        # Calculate departure time
        departure_dt = arrival_dt - timedelta(minutes=predicted_duration)
        
        # Add buffer time based on group size and time of day
        buffer_minutes = self._calculate_buffer_time(arrival_dt, group_size)
        departure_dt = departure_dt - timedelta(minutes=buffer_minutes)
        
        return {
            'departure_time': departure_dt.strftime("%H:%M"),
            'travel_time': f"{predicted_duration:.0f} minutes",
            'buffer_time': f"{buffer_minutes} minutes",
            'total_time': f"{predicted_duration + buffer_minutes:.0f} minutes"
        }
    
    def _calculate_trip_duration(self, df):
        """Calculate trip duration from coordinates"""
        durations = []
        for _, row in df.iterrows():
            # Calculate distance using Haversine formula (simplified)
            lat1, lon1 = row['Pick Up Latitude'], row['Pick Up Longitude']
            lat2, lon2 = row['Drop Off Latitude'], row['Drop Off Longitude']
            
            # Simple distance calculation
            lat_diff = abs(lat2 - lat1)
            lon_diff = abs(lon2 - lon1)
            distance = (lat_diff + lon_diff) * 69  # Rough miles
            
            # Estimate duration (15-45 minutes for Austin trips)
            duration = max(15, min(45, distance * 3 + 15))
            durations.append(duration)
        
        return durations
    
    def _extract_zone(self, address):
        """Extract zone from address"""
        if pd.isna(address):
            return 'Unknown'
        
        address_lower = address.lower()
        
        if 'airport' in address_lower or 'aus' in address_lower:
            return 'Airport'
        elif 'university' in address_lower or 'campus' in address_lower or '23rd' in address_lower:
            return 'University'
        elif 'west campus' in address_lower or 'w 23rd' in address_lower:
            return 'West Campus'
        elif 'downtown' in address_lower or '6th' in address_lower or 'market' in address_lower:
            return 'Downtown'
        elif 'east' in address_lower or 'e 6th' in address_lower:
            return 'East Austin'
        elif 'south' in address_lower or 's congress' in address_lower:
            return 'South Austin'
        elif 'north' in address_lower or 'n university' in address_lower:
            return 'North Austin'
        else:
            return 'Other'
    
    def _estimate_distance(self, row):
        """Estimate distance from coordinates"""
        lat1, lon1 = row['Pick Up Latitude'], row['Pick Up Longitude']
        lat2, lon2 = row['Drop Off Latitude'], row['Drop Off Longitude']
        
        lat_diff = abs(lat2 - lat1)
        lon_diff = abs(lon2 - lon1)
        distance = (lat_diff + lon_diff) * 69  # Rough miles
        
        return distance
    
    def _estimate_distance_from_zones(self, pickup_zone, dropoff_zone):
        """Estimate distance between zones"""
        # Zone distance matrix (miles)
        distances = {
            ('University', 'Airport'): 12,
            ('West Campus', 'Airport'): 13,
            ('Downtown', 'Airport'): 8,
            ('East Austin', 'Airport'): 10,
            ('South Austin', 'Airport'): 6,
            ('North Austin', 'Airport'): 15,
            ('University', 'Downtown'): 2,
            ('West Campus', 'Downtown'): 1,
            ('East Austin', 'Downtown'): 1,
            ('South Austin', 'Downtown'): 3,
            ('North Austin', 'Downtown'): 4,
        }
        
        # Check both directions
        key1 = (pickup_zone, dropoff_zone)
        key2 = (dropoff_zone, pickup_zone)
        
        if key1 in distances:
            return distances[key1]
        elif key2 in distances:
            return distances[key2]
        else:
            return 5  # Default distance
    
    def _calculate_buffer_time(self, arrival_time, group_size):
        """Calculate buffer time based on arrival time and group size"""
        hour = arrival_time.hour
        
        # Base buffer time
        base_buffer = 10
        
        # Rush hour buffer (7-9 AM, 5-7 PM)
        if (7 <= hour <= 9) or (17 <= hour <= 19):
            base_buffer += 15
        
        # Group size buffer
        group_buffer = (group_size - 1) * 2
        
        # Weekend buffer
        if arrival_time.weekday() >= 5:  # Saturday or Sunday
            base_buffer += 5
        
        return base_buffer + group_buffer

def create_smart_predictor():
    """Create and return a trained predictor"""
    predictor = TravelTimePredictor()
    return predictor
