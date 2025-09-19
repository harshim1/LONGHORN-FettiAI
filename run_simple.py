#!/usr/bin/env python3
"""
Austin Transportation Assistant - Simple Launch Script
"""

import subprocess
import sys
import os

def main():
    print("Austin Transportation Assistant")
    print("=" * 50)
    print("Launching the transportation analysis system...")
    print()
    
    # Check if streamlit is installed
    try:
        import streamlit
        print("Streamlit ready")
    except ImportError:
        print("Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    print()
    print("Features:")
    print("  • Three transportation assistants")
    print("  • Real Austin rideshare data")
    print("  • 30-minute predictions")
    print("  • Interactive scenarios")
    print("  • Live data visualizations")
    print()
    print("Starting application...")
    print("   Open your browser to: http://localhost:8501")
    print()
    
    # Run the simple app
    subprocess.run([sys.executable, "-m", "streamlit", "run", "war_room_simple.py", "--server.port", "8501"])

if __name__ == "__main__":
    main()
