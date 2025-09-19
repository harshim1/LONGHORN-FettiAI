#!/usr/bin/env python3
"""
Test script to verify FetiiAI setup
"""

import sys
import os

def test_imports():
    """Test if all required packages can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import streamlit
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import pandas
        print("✅ Pandas imported successfully")
    except ImportError as e:
        print(f"❌ Pandas import failed: {e}")
        return False
    
    try:
        import plotly
        print("✅ Plotly imported successfully")
    except ImportError as e:
        print(f"❌ Plotly import failed: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ python-dotenv import failed: {e}")
        return False
    
    return True

def test_modules():
    """Test if our custom modules can be imported"""
    print("\n🧪 Testing custom modules...")
    
    # Add utils to path
    sys.path.append('utils')
    
    try:
        from data_processor import FetiiDataProcessor
        print("✅ FetiiDataProcessor imported successfully")
    except ImportError as e:
        print(f"❌ FetiiDataProcessor import failed: {e}")
        return False
    
    try:
        from ai_integration import FetiiAI
        print("✅ FetiiAI imported successfully")
    except ImportError as e:
        print(f"❌ FetiiAI import failed: {e}")
        return False
    
    return True

def test_data_processor():
    """Test data processor functionality"""
    print("\n🧪 Testing data processor...")
    
    try:
        from data_processor import FetiiDataProcessor
        processor = FetiiDataProcessor()
        
        # Test with sample data
        import pandas as pd
        sample_data = pd.DataFrame({
            'trip_id': [1, 2, 3],
            'pickup_datetime': ['2024-01-01 10:00:00', '2024-01-01 11:00:00', '2024-01-01 12:00:00'],
            'group_size': [3, 4, 2],
            'rider_age': [25, 30, 35],
            'trip_duration_minutes': [20, 25, 15],
            'fare_amount': [30, 35, 25]
        })
        
        processor.data = sample_data
        processor._preprocess_data()
        
        stats = processor.get_trip_statistics()
        print(f"✅ Data processor working - Total trips: {stats['total_trips']}")
        return True
        
    except Exception as e:
        print(f"❌ Data processor test failed: {e}")
        return False

def main():
    print("🚗 FetiiAI Setup Test")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Test imports
    if not test_imports():
        all_tests_passed = False
    
    # Test modules
    if not test_modules():
        all_tests_passed = False
    
    # Test data processor
    if not test_data_processor():
        all_tests_passed = False
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 All tests passed! FetiiAI is ready to run.")
        print("\nTo start the app:")
        print("  python run_app.py")
        print("  or")
        print("  streamlit run app_enhanced.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\nTo install missing dependencies:")
        print("  pip install -r requirements.txt")

if __name__ == "__main__":
    main()
