#!/usr/bin/env python3
"""
Austin Mobility War Room - Launch Script
"""

import subprocess
import sys
import os

def main():
    print("⚔️  AUSTIN MOBILITY WAR ROOM")
    print("=" * 50)
    print("🚀 Launching the ultimate FetiiAI hackathon experience...")
    print()
    
    # Check if streamlit is installed
    try:
        import streamlit
        print("✅ Streamlit ready")
    except ImportError:
        print("📦 Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Check for .env file
    if not os.path.exists('.env'):
        print("⚠️  Creating .env file...")
        if os.path.exists('.env.example'):
            with open('.env.example', 'r') as src, open('.env', 'w') as dst:
                dst.write(src.read())
            print("📝 Please edit .env file and add your OpenAI API key for full AI features")
        else:
            print("❌ .env.example not found")
    
    print()
    print("🎯 FEATURES READY:")
    print("  • Three competing AI agents (Driver, Rider, City Planner)")
    print("  • Real Fetii Austin rideshare data")
    print("  • 30-minute predictive group formation analysis")
    print("  • Interactive battle scenarios")
    print("  • Live data visualizations")
    print()
    print("🚀 Starting War Room...")
    print("   Open your browser to: http://localhost:8501")
    print()
    
    # Run the war room app
    subprocess.run([sys.executable, "-m", "streamlit", "run", "war_room_app.py", "--server.port", "8501"])

if __name__ == "__main__":
    main()
