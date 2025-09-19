#!/usr/bin/env python3
"""
Austin Transportation Assistant - Smart ML Version
"""

import subprocess
import sys
import os

def main():
    print("Austin Transportation Assistant - Smart ML")
    print("=" * 50)
    print("Launching ML-powered transportation system...")
    print()
    
    # Check if streamlit is installed
    try:
        import streamlit
        print("Streamlit ready")
    except ImportError:
        print("Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Install scikit-learn if not present
    try:
        import sklearn
        print("Scikit-learn ready")
    except ImportError:
        print("Installing scikit-learn...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "scikit-learn"])
    
    print()
    print("Smart Features:")
    print("  • ML Travel Time Prediction")
    print("  • Real-time Departure Planning")
    print("  • Group Size Optimization")
    print("  • Traffic Pattern Analysis")
    print("  • Real Austin rideshare data")
    print()
    print("Starting smart application...")
    print("   Open your browser to: http://localhost:8501")
    print()
    
    # Run the smart app
    subprocess.run([sys.executable, "-m", "streamlit", "run", "war_room_smart.py", "--server.port", "8501"])

if __name__ == "__main__":
    main()
