#!/usr/bin/env python3
"""
Simple script to run the FetiiAI Streamlit app
"""

import subprocess
import sys
import os

def main():
    # Check if streamlit is installed
    try:
        import streamlit
    except ImportError:
        print("Streamlit not found. Installing requirements...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Check for .env file
    if not os.path.exists('.env'):
        print("⚠️  .env file not found. Creating from template...")
        if os.path.exists('.env.example'):
            with open('.env.example', 'r') as src, open('.env', 'w') as dst:
                dst.write(src.read())
            print("📝 Please edit .env file and add your OpenAI API key")
        else:
            print("❌ .env.example not found")
    
    # Run the app
    print("🚀 Starting FetiiAI Streamlit App...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app_enhanced.py"])

if __name__ == "__main__":
    main()
