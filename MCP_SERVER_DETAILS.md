# 📋 YOUR MCP SERVER DETAILS - COMPLETE INFORMATION

## ✅ ANSWER TO ALL YOUR QUESTIONS

### 1️⃣ Full Path to Your MCP Server Folder

```
C:\Users\harsh\Desktop\VS_code\TravelAssistant-ranjit\TravelAssistant-ranjit
```

**With Servers:**

```
C:\Users\harsh\Desktop\VS_code\TravelAssistant-ranjit\TravelAssistant-ranjit\servers
```

**Individual Server Paths:**

```
Flight Server:   C:\Users\harsh\Desktop\VS_code\TravelAssistant-ranjit\TravelAssistant-ranjit\servers\flight_server
Hotel Server:    C:\Users\harsh\Desktop\VS_code\TravelAssistant-ranjit\TravelAssistant-ranjit\servers\hotel_server
Event Server:    C:\Users\harsh\Desktop\VS_code\TravelAssistant-ranjit\TravelAssistant-ranjit\servers\event_server
Weather Server:  C:\Users\harsh\Desktop\VS_code\TravelAssistant-ranjit\TravelAssistant-ranjit\servers\weather_server
```

---

### 2️⃣ Main Python File Names

| Server      | Main File           | Full Path                                     |
| ----------- | ------------------- | --------------------------------------------- |
| **Flight**  | `flight_server.py`  | `...servers\flight_server\flight_server.py`   |
| **Hotel**   | `hotel_server.py`   | `...servers\hotel_server\hotel_server.py`     |
| **Event**   | `event_server.py`   | `...servers\event_server\event_server.py`     |
| **Weather** | `weather_server.py` | `...servers\weather_server\weather_server.py` |

---

### 3️⃣ Python Command

```
python
```

**Version Installed:**

```
Python 3.13.7
```

**Usage:**

```powershell
python flight_server.py
python hotel_server.py
python event_server.py
python weather_server.py
```

---

### 4️⃣ Environment Variables / API Keys

You have **1 required API key:**

```
SERPAPI_KEY=49ced1d153d6c133fccab2cbebc1dfe92881c4e5d0b60815bca101e9b6c2f7dd
```

**Location:** `.env` file (already in your project)

**What it's used for:**

- Flight searches (via Google Flights API)
- Hotel searches (via Google Hotels API)
- Event searches (via SerpAPI)

**Weather server:** Uses Open-Meteo API (free, no key needed)

---

## 🔧 DEPENDENCIES

Your project uses these libraries (from `requirements.txt`):

```
requests      - For making HTTP API calls
python-dotenv - For loading .env file
mcp           - Model Context Protocol library
```

---

## 📝 COMPLETE CONFIG FOR CLAUDE DESKTOP

Here's the EXACT config file for your MCP servers:

**File Location:**

```
C:\Users\harsh\AppData\Roaming\Claude\claude_desktop_config.json
```

**File Content:**

```json
{
  "mcpServers": {
    "flight-server": {
      "command": "python",
      "args": [
        "C:\\Users\\harsh\\Desktop\\VS_code\\TravelAssistant-ranjit\\TravelAssistant-ranjit\\servers\\flight_server\\flight_server.py"
      ],
      "env": {
        "SERPAPI_KEY": "49ced1d153d6c133fccab2cbebc1dfe92881c4e5d0b60815bca101e9b6c2f7dd"
      }
    },
    "hotel-server": {
      "command": "python",
      "args": [
        "C:\\Users\\harsh\\Desktop\\VS_code\\TravelAssistant-ranjit\\TravelAssistant-ranjit\\servers\\hotel_server\\hotel_server.py"
      ],
      "env": {
        "SERPAPI_KEY": "49ced1d153d6c133fccab2cbebc1dfe92881c4e5d0b60815bca101e9b6c2f7dd"
      }
    },
    "event-server": {
      "command": "python",
      "args": [
        "C:\\Users\\harsh\\Desktop\\VS_code\\TravelAssistant-ranjit\\TravelAssistant-ranjit\\servers\\event_server\\event_server.py"
      ],
      "env": {
        "SERPAPI_KEY": "49ced1d153d6c133fccab2cbebc1dfe92881c4e5d0b60815bca101e9b6c2f7dd"
      }
    },
    "weather-server": {
      "command": "python",
      "args": [
        "C:\\Users\\harsh\\Desktop\\VS_code\\TravelAssistant-ranjit\\TravelAssistant-ranjit\\servers\\weather_server\\weather_server.py"
      ]
    }
  }
}
```

**Note:** Weather server doesn't need SERPAPI_KEY since it uses Open-Meteo (free API).

---

## 🚀 QUICK SETUP SUMMARY

| Item                | Answer                                                                         |
| ------------------- | ------------------------------------------------------------------------------ |
| **Main Folder**     | `C:\Users\harsh\Desktop\VS_code\TravelAssistant-ranjit\TravelAssistant-ranjit` |
| **Servers Folder**  | `...TravelAssistant-ranjit\servers`                                            |
| **Python Command**  | `python` (Version 3.13.7)                                                      |
| **Main Files**      | `flight_server.py`, `hotel_server.py`, `event_server.py`, `weather_server.py`  |
| **API Key Needed**  | `SERPAPI_KEY` (already in `.env`)                                              |
| **Other Keys**      | None (Weather uses free API)                                                   |
| **Config Location** | `%APPDATA%\Claude\claude_desktop_config.json`                                  |

---

## ✅ COPY-PASTE READY PATHS

### For Terminal Commands:

```powershell
# Flight Server
python C:\Users\harsh\Desktop\VS_code\TravelAssistant-ranjit\TravelAssistant-ranjit\servers\flight_server\flight_server.py

# Hotel Server
python C:\Users\harsh\Desktop\VS_code\TravelAssistant-ranjit\TravelAssistant-ranjit\servers\hotel_server\hotel_server.py

# Event Server
python C:\Users\harsh\Desktop\VS_code\TravelAssistant-ranjit\TravelAssistant-ranjit\servers\event_server\event_server.py

# Weather Server
python C:\Users\harsh\Desktop\VS_code\TravelAssistant-ranjit\TravelAssistant-ranjit\servers\weather_server\weather_server.py
```

Or simpler (from project folder):

```powershell
cd C:\Users\harsh\Desktop\VS_code\TravelAssistant-ranjit\TravelAssistant-ranjit

python servers/flight_server/flight_server.py
python servers/hotel_server/hotel_server.py
python servers/event_server/event_server.py
python servers/weather_server/weather_server.py
```

---

## 🎯 NEXT STEPS

1. **Copy the config JSON above** to `%APPDATA%\Claude\claude_desktop_config.json`
2. **Download Claude Desktop** from https://claude.ai/download
3. **Restart Claude Desktop**
4. **Start your servers** (all 4 in separate terminals)
5. **Open Claude Desktop** and test:
   ```
   Find flights from Pune to Jaipur for Feb 20
   ```

All set! ✅

---

## 📊 ARCHITECTURE SUMMARY

```
YOUR SERVERS:
├── Flight Server (Port 8001)
│   └── Uses: SerpAPI → Google Flights
├── Hotel Server (Port 8002)
│   └── Uses: SerpAPI → Google Hotels
├── Event Server (Port 8003)
│   └── Uses: SerpAPI → Event Data
└── Weather Server (Port 8004)
    └── Uses: Open-Meteo API (Free, No Key)

FRAMEWORK: FastMCP (Model Context Protocol)
LANGUAGE: Python 3.13.7
CONFIG: Claude Desktop config file
```

---

**Ready to set up Claude Desktop? Use the config JSON above!** 🚀
