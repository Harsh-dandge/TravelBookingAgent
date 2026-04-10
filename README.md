# 🚀 Travel Assistant - AI-Powered Travel Planning with MCP

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![FastMCP](https://img.shields.io/badge/FastMCP-Latest-green.svg)](https://github.com/anthropics/mcp)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()

> An intelligent travel planning application powered by **Model Context Protocol (MCP)** microservices. Search flights, hotels, events, and get weather forecasts - all integrated with Claude AI.

## ✨ Features

### 🎯 Core Capabilities
- **✈️ Flight Search** - Real-time flight data from Google Flights API via SerpAPI
- **🏨 Hotel Search** - Comprehensive hotel search with ratings, prices, and amenities
- **🎉 Events Discovery** - Find cultural events, festivals, and concerts worldwide
- **🌦️ Weather Forecast** - 15-day weather predictions for travel planning
- **🤖 Claude AI Integration** - Intelligent travel assistant powered by MCP

### 🏗️ Architecture Highlights
- **4 Independent Microservices** - Flight, Hotel, Event, Weather servers run independently
- **Model Context Protocol (MCP)** - Standard protocol for LLM integration
- **FastMCP Framework** - Lightweight, efficient Python MCP implementation
- **Scalable Design** - Each service on separate port (8001-8004) for easy scaling
- **Claude Desktop Compatible** - Native integration with Claude Desktop app

### 🌐 Multiple Interfaces
- **Web UI** - Beautiful Flask-based web application
- **Claude Desktop** - Native MCP integration for intelligent queries
- **CLI Tools** - Command-line interface for automation
- **API Endpoints** - RESTful API for third-party integration

## 🛠️ Technology Stack

### Backend
```
• Python 3.13.7
• FastMCP (Model Context Protocol)
• Flask Web Framework
• requests HTTP Client
```

### External APIs
```
• SerpAPI - Flights, Hotels, Events data
• Open-Meteo - Weather & Geocoding (Free)
• Google Flights/Hotels/Events Integration
```

### Frontend
```
• HTML5 with Semantic markup
• CSS3 with Flexbox/Grid & Animations
• Vanilla JavaScript (No frameworks)
• Responsive Mobile Design
```

### Deployment
```
• Docker & Docker Compose Ready
• Multi-OS Support (Windows, macOS, Linux)
• Cloud-agnostic Architecture
```

## 📋 Project Structure

```
TravelAssistant-ranjit/
├── servers/
│   ├── flight_server/              # ✈️  Flight search microservice
│   │   ├── flight_server.py        #     FastMCP server implementation
│   │   └── __pycache__/
│   ├── hotel_server/               # 🏨 Hotel search microservice
│   │   ├── hotel_server.py         #     Hotel discovery & filtering
│   │   └── __pycache__/
│   ├── event_server/               # 🎉 Events microservice
│   │   ├── event_server.py         #     Event & festival discovery
│   │   └── __pycache__/
│   └── weather_server/             # 🌦️  Weather microservice
│       ├── weather_server.py       #     15-day forecasts
│       └── __pycache__/
├── templates/
│   └── index.html                  # Main web application UI (HTML)
├── static/
│   ├── style.css                   # Styling (CSS3)
│   └── script.js                   # Frontend interactivity (JavaScript)
├── demo_app.py                     # Flask web server application
├── utils.py                        # Utility functions & helpers
├── .env                            # API keys & configuration (git-ignored)
├── .env.example                    # Example environment template
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore rules
├── README.md                       # This file
├── LICENSE                         # MIT License
└── docs/
    ├── CLAUDE_DESKTOP_SETUP.md    # Claude Desktop integration guide
    ├── DEMO_STEPS.md              # Detailed demo instructions
    ├── MCP_SERVER_DETAILS.md      # MCP configuration details
    ├── DEPLOYMENT_GUIDE.md        # Production deployment
    └── TESTING.md                 # Testing procedures
```

## 🚀 Quick Start Guide

### Prerequisites
- **Python 3.13+** (Download from python.org)
- **pip** package manager
- **Git** version control

### Installation Steps

#### 1. Clone Repository
```bash
git clone https://github.com/harsh-dandge/TravelAssistant.git
cd TravelAssistant
```

#### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your API key
# Add your SERPAPI_KEY from https://serpapi.com
```

#### 5. Start Backend Servers (Open 4 terminals)

**Terminal 1 - Flight Server:**
```bash
python servers/flight_server/flight_server.py
```

**Terminal 2 - Hotel Server:**
```bash
python servers/hotel_server/hotel_server.py
```

**Terminal 3 - Event Server:**
```bash
python servers/event_server/event_server.py
```

**Terminal 4 - Weather Server:**
```bash
python servers/weather_server/weather_server.py
```

#### 6. Start Web Application
```bash
python demo_app.py
```

**Access:** http://localhost:5000

## 💡 Usage Examples

### Web Interface
1. Navigate to http://localhost:5000
2. Click tabs (Flights, Hotels, Events, Weather)
3. Enter search parameters
4. Click Search/Get buttons
5. View results

### Claude Desktop Integration
1. Download: https://claude.ai/download
2. Configure MCP servers (see [CLAUDE_DESKTOP_SETUP.md](docs/CLAUDE_DESKTOP_SETUP.md))
3. Open Claude Desktop
4. Ask travel questions:

```
"Find flights from Pune to Jaipur for Feb 20-23"
"Show me 5-star hotels in Delhi under ₹10,000/night"
"What events are happening in Kerala next month?"
"Plan a 3-day trip to Goa with flights, hotels, and weather"
```

Claude will automatically call your MCP servers!

## 📡 API Endpoints

### Flight Server (Port 8001)
```
GET /flights
  Params: from (City Code), to (City Code), date (YYYY-MM-DD)
  Example: /flights?from=PNQ&to=JAI&date=2026-02-20
```

### Hotel Server (Port 8002)
```
GET /hotels
  Params: location, checkin, checkout, guests
  Example: /hotels?location=Jaipur&checkin=2026-02-20&checkout=2026-02-23&guests=2
```

### Event Server (Port 8003)
```
GET /events
  Params: type (festivals/concerts), location
  Example: /events?type=festivals&location=Jaipur
```

### Weather Server (Port 8004)
```
GET /weather
  Params: location, days (forecast length)
  Example: /weather?location=Jaipur&days=15
```

## ⚙️ Configuration

### Environment Variables
```bash
# Required
SERPAPI_KEY=your_serpapi_api_key_here

# Optional (defaults work fine)
FLASK_ENV=development
DEBUG=True
```

### Server Ports
| Service | Port | Purpose |
|---------|------|---------|
| Flight Server | 8001 | Flight search microservice |
| Hotel Server | 8002 | Hotel search microservice |
| Event Server | 8003 | Events microservice |
| Weather Server | 8004 | Weather microservice |
| Flask Web App | 5000 | Web interface |

Modify port numbers in respective server files if needed.

## 🧪 Testing

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Tests
```bash
pytest tests/test_flight.py -v
pytest tests/test_hotel.py -v
pytest tests/test_events.py -v
pytest tests/test_weather.py -v
```

### Manual Testing
See [TESTING.md](docs/TESTING.md) for comprehensive testing procedures.

## 📚 Documentation

- **[CLAUDE_DESKTOP_SETUP.md](docs/CLAUDE_DESKTOP_SETUP.md)** - Complete Claude Desktop integration guide
- **[DEMO_STEPS.md](docs/DEMO_STEPS.md)** - Step-by-step demonstration instructions
- **[MCP_SERVER_DETAILS.md](docs/MCP_SERVER_DETAILS.md)** - MCP configuration and setup
- **[DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md)** - Production deployment options
- **[TESTING.md](docs/TESTING.md)** - Comprehensive testing guide

## 🌍 Deployment Options

### Local Development
```bash
python demo_app.py
```

### Production with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 demo_app:app
```

### Docker Deployment
```bash
docker-compose up --build
```

### Cloud Platforms
See [DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md) for detailed instructions:
- AWS EC2 & Elastic Beanstalk
- Azure App Service
- Google Cloud Platform
- Heroku
- DigitalOcean

## 📊 Performance Metrics

| Component | Response Time | Notes |
|-----------|---------------|-------|
| Flight Search | 2-3 seconds | Via SerpAPI Google Flights |
| Hotel Search | 2-3 seconds | Via SerpAPI Google Hotels |
| Event Search | 1-2 seconds | Via SerpAPI |
| Weather Forecast | <1 second | Open-Meteo free API |
| Web UI Load | <500ms | Optimized static files |

## 🐛 Troubleshooting

### "SERPAPI_KEY not found"
```bash
# Verify .env file exists
ls -la .env

# Check .env content
cat .env

# Ensure format: SERPAPI_KEY=your_key_here
```

### "Port 8001 already in use"
```bash
# Windows: Find and kill process
netstat -ano | findstr :8001
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8001 | xargs kill -9
```

### "Module not found errors"
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Verify installation
python -c "import mcp; print('MCP installed')"
```

### "Claude Desktop not connecting"
1. Verify config: `%APPDATA%\Claude\claude_desktop_config.json` (Windows)
2. Check all servers running: Should show port messages
3. Restart Claude Desktop completely
4. Check browser console for errors

See extended troubleshooting in documentation.

## 🚀 Roadmap

### Current ✅
- [x] Flight search microservice
- [x] Hotel search microservice
- [x] Events discovery microservice
- [x] Weather forecast microservice
- [x] Web UI interface
- [x] Claude Desktop integration
- [x] Comprehensive documentation

### Upcoming 🔄
- [ ] User authentication & profiles
- [ ] Trip itinerary generation
- [ ] Price tracking & alerts
- [ ] Mobile app (React Native/Flutter)
- [ ] Advanced filtering & sorting
- [ ] Multi-language support
- [ ] Recommendation engine
- [ ] Social features (trip sharing)

### Future 🌟
- [ ] Payment gateway integration
- [ ] Hotel/Flight booking
- [ ] Travel insurance integration
- [ ] Visa & documentation helper
- [ ] Currency converter
- [ ] Restaurant recommendations
- [ ] Activity suggestions

## 🤝 Contributing

We welcome contributions! Here's how:

### Code Contribution Steps
1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Make changes & test
4. Commit with clear messages: `git commit -m 'Add amazing feature'`
5. Push branch: `git push origin feature/amazing-feature`
6. Open Pull Request with description

### Contribution Guidelines
- Follow PEP 8 Python style guide
- Add docstrings to functions
- Write tests for new features
- Update documentation
- Keep commits atomic & meaningful

## 📄 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

You are free to:
- Use commercially
- Modify the code
- Distribute the software
- Use privately
- Use with patent use

## 📞 Support & Contact

### Need Help?
- 📧 Email: harsh@example.com
- 🐛 Report bugs: [GitHub Issues](https://github.com/harsh-dandge/TravelAssistant/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/harsh-dandge/TravelAssistant/discussions)
- 📖 Read docs: Check `/docs` folder

### Community
- Star the repository ⭐
- Share with friends
- Contribute improvements
- Report issues & feedback

## 🙏 Acknowledgments

Special thanks to:
- **Anthropic** - Model Context Protocol (MCP)
- **SerpAPI** - Flight, Hotel & Event data APIs
- **Open-Meteo** - Free weather data API
- **Flask** - Web framework
- **Python Community** - Amazing language & tools

## 👨‍💻 Author

**Harsh Dandge**
- GitHub: [@harsh-dandge](https://github.com/harsh-dandge)
- Project: Travel Assistant (TravelAssistant-ranjit)
- Email: harsh.dandge@example.com

---

## 📈 Stats

- 📊 4 Microservices
- 🌐 3 User Interfaces (Web, Claude, CLI)
- 📦 Fully documented codebase
- 🧪 Comprehensive test suite
- 📚 Extensive documentation

---

<div align="center">

**⭐ If this project helped you, please star it on GitHub! ⭐**

**Made with ❤️ by Harsh Dandge**

[GitHub](https://github.com/harsh-dandge/TravelAssistant) • [Issues](https://github.com/harsh-dandge/TravelAssistant/issues) • [Discussions](https://github.com/harsh-dandge/TravelAssistant/discussions)

**Happy Traveling! 🚀✈️**

</div>
