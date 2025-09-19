# 🚁 Austin Mobility War Room - FetiiAI Hackathon

## 🎯 Project Overview

The **Austin Mobility War Room** is a strategic command center where 3 AI agents (Driver, Rider, City Planner) compete in real-time to solve mobility challenges using Fetii's Austin rideshare dataset. This project was built for the FetiiAI Hackathon and showcases advanced AI agent interactions, predictive analytics, and real-time strategic decision-making.

## 🚀 Key Features

### 🤖 Multi-Agent System
- **Driver Agent**: Optimizes vehicle positioning and route efficiency
- **Rider Agent**: Understands user behavior and demand patterns  
- **City Planner Agent**: Manages traffic flow and urban mobility

### 📊 Real-Time Analytics
- Live trip data analysis from Fetii's Austin dataset
- Hourly pattern recognition and peak time predictions
- Group size optimization and demand forecasting
- Interactive visualizations and strategic insights

### 🎮 Interactive War Room
- Real-time agent battles and strategic debates
- Live predictions and scenario planning
- Agent scoring system and performance tracking
- Dynamic visualizations with improved readability

## 🛠️ Tech Stack

- **Frontend**: Streamlit with custom CSS styling
- **Data Processing**: Pandas, NumPy for analytics
- **Visualizations**: Plotly for interactive charts
- **AI Integration**: Custom agent logic with data-driven insights
- **Data Source**: Real Fetii Austin rideshare data from Google Sheets

## 📁 Project Structure

```
LONGHORN-FettiAI/
├── war_room_final.py          # Main Streamlit application
├── utils/
│   ├── data_processor.py      # Data cleaning and analysis
│   ├── fetii_data_loader.py   # Google Sheets data loader
│   └── ai_agents.py          # AI agent implementations
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/harshim1/LONGHORN-FettiAI.git
cd LONGHORN-FettiAI
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
streamlit run war_room_final.py
```

### 4. Access the War Room
Open your browser to `http://localhost:8501`

## 🎯 How to Use

1. **Ask Strategic Questions**: Type mobility challenges like "What's the best strategy for rush hour?"
2. **Watch Agent Battles**: See the 3 AI agents compete with different strategies
3. **View Live Predictions**: Get real-time forecasts and recommendations
4. **Analyze Data**: Explore Austin mobility patterns and insights

## 📊 Sample Queries

- "What's the optimal strategy for rush hour?"
- "How should we handle campus traffic?"
- "What's the best approach for downtown events?"
- "When is peak demand for group rides?"

## 🏆 Hackathon Highlights

### 🥇 Killer Combination: Predictive + Multi-Agent + Time Travel
- **Strategic Command Center**: 3 AI agents competing for optimal solutions
- **Real-time Predictions**: 30-minute ahead group formation forecasts
- **Data-Driven Insights**: Based on actual Fetii Austin rideshare data
- **Interactive Theater**: Watch AI agents debate and strategize

### 🎨 Enhanced User Experience
- **Improved Readability**: High-contrast colors for better visibility
- **Responsive Design**: Works on desktop and mobile
- **Real-time Updates**: Live agent scoring and battle logs
- **Professional UI**: Military-inspired War Room aesthetic

## 📈 Data Insights

The application analyzes real Fetii Austin data including:
- Trip patterns and peak hours
- Group size distributions
- Popular pickup/dropoff locations
- Rider demographics and behavior
- Traffic flow optimization opportunities

## 🔧 Configuration

### Environment Variables
Create a `.env` file with:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### Data Source
The app automatically loads data from the provided Google Sheets URL with Fetii Austin rideshare information.

## 🎯 Future Enhancements

- [ ] Real-time data streaming integration
- [ ] Advanced ML models for demand prediction
- [ ] Multi-city expansion capabilities
- [ ] API endpoints for external integrations
- [ ] Mobile app development

## 🤝 Contributing

This project was built for the FetiiAI Hackathon. Feel free to fork and enhance!

## 📄 License

This project is part of the FetiiAI Hackathon submission.

## 🏆 Hackathon Submission

**Team**: LONGHORN-FettiAI  
**Project**: Austin Mobility War Room  
**Category**: AI-Powered Mobility Solutions  
**Tech Stack**: Streamlit, Python, Pandas, Plotly, Custom AI Agents

---

*Built with ❤️ for the FetiiAI Hackathon - Transforming urban mobility through AI-powered strategic planning*
