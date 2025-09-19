# 🚀 Deployment Guide - Austin Mobility War Room

## 📋 Prerequisites

- Python 3.8 or higher
- pip package manager
- Git (for cloning)

## 🛠️ Local Development Setup

### 1. Clone the Repository
```bash
git clone https://github.com/harshim1/LONGHORN-FettiAI.git
cd LONGHORN-FettiAI
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Setup
```bash
cp .env.example .env
# Edit .env file with your OpenAI API key (optional)
```

### 5. Run the Application
```bash
streamlit run war_room_final.py
```

### 6. Access the War Room
Open your browser to `http://localhost:8501`

## 🌐 Streamlit Cloud Deployment

### 1. Fork the Repository
- Go to https://github.com/harshim1/LONGHORN-FettiAI
- Click "Fork" to create your own copy

### 2. Deploy to Streamlit Cloud
- Go to https://share.streamlit.io/
- Sign in with your GitHub account
- Click "New app"
- Select your forked repository
- Set main file path: `war_room_final.py`
- Click "Deploy!"

### 3. Configure Secrets (Optional)
In Streamlit Cloud, add secrets for API keys:
```toml
[secrets]
OPENAI_API_KEY = "your_api_key_here"
```

## 🐳 Docker Deployment

### 1. Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "war_room_final.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### 2. Build and Run
```bash
docker build -t austin-mobility-war-room .
docker run -p 8501:8501 austin-mobility-war-room
```

## 🔧 Configuration Options

### Environment Variables
- `OPENAI_API_KEY`: OpenAI API key for enhanced AI features (optional)
- `STREAMLIT_SERVER_PORT`: Port for Streamlit server (default: 8501)
- `STREAMLIT_SERVER_ADDRESS`: Server address (default: localhost)

### Streamlit Configuration
Create `.streamlit/config.toml`:
```toml
[server]
port = 8501
address = "0.0.0.0"

[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
```

## 🚨 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   streamlit run war_room_final.py --server.port 8502
   ```

2. **Missing Dependencies**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. **Data Loading Issues**
   - Check internet connection for Google Sheets access
   - Verify the data source URL is accessible

4. **API Key Issues**
   - Ensure `.env` file is in the project root
   - Check API key format and validity

### Performance Optimization

1. **Reduce Data Size**
   - Modify `utils/fetii_data_loader.py` to load fewer rows
   - Add data caching for faster subsequent loads

2. **Memory Usage**
   - Monitor memory usage with large datasets
   - Consider data pagination for very large datasets

## 📊 Monitoring and Analytics

### Streamlit Cloud Analytics
- View app usage statistics
- Monitor performance metrics
- Track user engagement

### Local Development
- Use Streamlit's built-in debugging tools
- Monitor console output for errors
- Check browser developer tools

## 🔄 Updates and Maintenance

### Updating the Application
```bash
git pull origin main
pip install -r requirements.txt
streamlit run war_room_final.py
```

### Backup and Recovery
- Regular git commits for code backup
- Export data snapshots if needed
- Document configuration changes

## 🎯 Production Considerations

### Security
- Use environment variables for sensitive data
- Implement proper authentication if needed
- Regular security updates

### Scalability
- Consider load balancing for high traffic
- Implement caching strategies
- Monitor resource usage

### Monitoring
- Set up error tracking
- Monitor application performance
- Track user analytics

---

*For additional support, check the main README.md or create an issue in the repository.*
