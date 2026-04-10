# 🚀 CLAUDE + TRAVEL ASSISTANT INTEGRATION GUIDE

**Quick Decision:** Which setup do you want?

| Setup                 | Best For                | Difficulty    | Internet          |
| --------------------- | ----------------------- | ------------- | ----------------- |
| **Claude Desktop**    | Personal demos, testing | ⭐⭐ Easy     | ❌ Works offline! |
| **Claude.ai (Web)**   | Browser, no install     | ⭐⭐⭐ Medium | ✅ Needs internet |
| **Claude Code (CLI)** | Terminal users          | ⭐✅ Simple   | ✅ Needs internet |

**My Recommendation:** Start with **Claude Desktop** - easiest setup! ✅

---

## ✅ PART 1: START THE 4 BACKEND SERVERS

### Step 1: Open 4 Terminal Windows

Press `Ctrl + Shift + J` four times in VS Code to open 4 terminals.

Or manually open PowerShell 4 times:

- Start Menu → Search "PowerShell" → Click
- Press `Ctrl + ~` (backtick) in VS Code for new terminal tab

---

### Step 2: Navigate to Project Folder

In **Each terminal**, run:

```powershell
cd C:\Users\harsh\Desktop\VS_code\TravelAssistant-ranjit\TravelAssistant-ranjit
```

**Expected output:**

```
C:\Users\harsh\Desktop\VS_code\TravelAssistant-ranjit\TravelAssistant-ranjit>
```

---

### Step 3: Start Flight Server (Terminal 1)

In **Terminal 1**, paste:

```powershell
python servers/flight_server/flight_server.py
```

**You should see:**

```
✈️  FLIGHT SERVER
Starting on port 8001
Listening for connections...
```

✅ **Keep this running!**

---

### Step 4: Start Hotel Server (Terminal 2)

In **Terminal 2**, paste:

```powershell
python servers/hotel_server/hotel_server.py
```

**You should see:**

```
🏨 HOTEL SERVER
Starting on port 8002
Listening for connections...
```

✅ **Keep this running!**

---

### Step 5: Start Event Server (Terminal 3)

In **Terminal 3**, paste:

```powershell
python servers/event_server/event_server.py
```

**You should see:**

```
🎉 EVENT SERVER
Starting on port 8003
Listening for connections...
```

✅ **Keep this running!**

---

### Step 6: Start Weather Server (Terminal 4)

In **Terminal 4**, paste:

```powershell
python servers/weather_server/weather_server.py
```

**You should see:**

```
🌦️  WEATHER SERVER
Starting on port 8004
Listening for connections...
```

✅ **Keep this running!**

---

## ✅ VERIFICATION

All 4 terminals should show:

```
Terminal 1: ✈️  FLIGHT SERVER - port 8001 ✅
Terminal 2: 🏨 HOTEL SERVER - port 8002 ✅
Terminal 3: 🎉 EVENT SERVER - port 8003 ✅
Terminal 4: 🌦️  WEATHER SERVER - port 8004 ✅
```

**If you see "Error" or "Connection refused"**, run this in a new terminal:

```powershell
python -m pip install requests python-dotenv mcp --upgrade
```

Then restart the servers.

---

## ✅ PART 2: CREATE JSON CONFIGURATION FILE

### What is this JSON file?

- Tells Claude **where your servers are**
- Tells Claude **how to talk to your servers**
- Acts as a **bridge between Claude and your Python servers**

---

### Step 1: Create File

1. In VS Code, right-click on project folder
2. Click "New File"
3. Name it: `claude.json`

**File location should be:**

```
C:\Users\harsh\Desktop\VS_code\TravelAssistant-ranjit\TravelAssistant-ranjit\claude.json
```

---

### Step 2: Copy This Content

**Paste this EXACTLY:**

```json
{
  "mcpServers": {
    "flight-server": {
      "command": "python",
      "args": ["servers/flight_server/flight_server.py"],
      "env": {
        "PYTHONPATH": "."
      }
    },
    "hotel-server": {
      "command": "python",
      "args": ["servers/hotel_server/hotel_server.py"],
      "env": {
        "PYTHONPATH": "."
      }
    },
    "event-server": {
      "command": "python",
      "args": ["servers/event_server/event_server.py"],
      "env": {
        "PYTHONPATH": "."
      }
    },
    "weather-server": {
      "command": "python",
      "args": ["servers/weather_server/weather_server.py"],
      "env": {
        "PYTHONPATH": "."
      }
    }
  }
}
```

---

### Step 3: Save File

Press `Ctrl + S`

**You should now have:**

```
TravelAssistant-ranjit/
├── claude.json          ← NEW FILE
├── demo_app.py
├── utils.py
├── servers/
│   ├── flight_server/
│   ├── hotel_server/
│   ├── event_server/
│   └── weather_server/
└── templates/
```

---

## 🎯 WHAT'S IN THE JSON FILE? (Explained Like You're 10)

```json
{
  "mcpServers": {          ← "Hey Claude, here are my servers"
    "flight-server": {     ← Server #1 name
      "command": "python", ← Use Python to run it
      "args": ["servers/flight_server/flight_server.py"],  ← Location
      "env": {"PYTHONPATH": "."}  ← Settings
    },
    // ... same for other 3 servers
  }
}
```

**In English:**

> "Claude, I have 4 servers. To use them, run Python with these file paths. The servers are in the `servers/` folder."

---

## ✅ PART 3: CHOOSE YOUR SETUP

### 🖥️ **OPTION 1: Claude Desktop (RECOMMENDED)**

**Best for:** Easy setup, works offline, perfect for demos

#### Step 1: Download Claude Desktop

Go to: https://claude.ai/download

- Choose "Windows"
- Install like any other app

#### Step 2: Find Config Folder

Open File Explorer and go to:

```
%APPDATA%\Claude\
```

**Which is actually:**

```
C:\Users\harsh\AppData\Roaming\Claude\
```

If `Claude` folder doesn't exist, create it.

#### Step 3: Create `claude_desktop_config.json`

In the `Claude` folder, create file: `claude_desktop_config.json`

**Content:**

```json
{
  "mcpServers": {
    "flight-server": {
      "command": "python",
      "args": [
        "C:\\Users\\harsh\\Desktop\\VS_code\\TravelAssistant-ranjit\\TravelAssistant-ranjit\\servers\\flight_server\\flight_server.py"
      ]
    },
    "hotel-server": {
      "command": "python",
      "args": [
        "C:\\Users\\harsh\\Desktop\\VS_code\\TravelAssistant-ranjit\\TravelAssistant-ranjit\\servers\\hotel_server\\hotel_server.py"
      ]
    },
    "event-server": {
      "command": "python",
      "args": [
        "C:\\Users\\harsh\\Desktop\\VS_code\\TravelAssistant-ranjit\\TravelAssistant-ranjit\\servers\\event_server\\event_server.py"
      ]
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

#### Step 4: Restart Claude Desktop

1. Close Claude Desktop completely
2. Reopen it
3. You should see MCP servers connected! ✅

#### Step 5: Start Chatting!

Type in Claude:

```
Find me flights from Pune to Jaipur for Feb 20-23
```

Claude will automatically call your servers! 🎉

---

### 🌐 **OPTION 2: Claude.ai (Web Browser)**

**Best for:** Browser access, no installation

#### ⚠️ Requirements:

- Servers must be on **public internet** (with HTTPS)
- Can't work with localhost
- Need to deploy servers to cloud (AWS, Heroku, etc.)

#### Step 1: Deploy Servers to Cloud

This is complex. Skip for now unless you want to host online.

---

### 💻 **OPTION 3: Claude Code (CLI)**

**Best for:** Terminal users, automation

#### Step 1: Install CLI

```powershell
npm install -g @anthropic-ai/claude-code
```

#### Step 2: Create Config File

Save the JSON we created before.

#### Step 3: Run Command

```powershell
claude-code --config claude.json
```

---

## 🎯 QUICK START (Just Do This!)

### **EASIEST PATH: Claude Desktop**

```
STEP 1: Start 4 backend servers (copy the commands from Part 1)
        Terminal 1: python servers/flight_server/flight_server.py
        Terminal 2: python servers/hotel_server/hotel_server.py
        Terminal 3: python servers/event_server/event_server.py
        Terminal 4: python servers/weather_server/weather_server.py

STEP 2: Create claude.json (copy from Part 2)
        Location: C:\Users\harsh\Desktop\VS_code\TravelAssistant-ranjit\TravelAssistant-ranjit\claude.json

STEP 3: Download Claude Desktop
        https://claude.ai/download

STEP 4: Create claude_desktop_config.json
        Location: C:\Users\harsh\AppData\Roaming\Claude\claude_desktop_config.json
        Content: (copy from Option 1, Step 3)

STEP 5: Restart Claude Desktop

STEP 6: Start Chatting!
        "Find flights from Pune to Jaipur"
        Claude does everything else! ✨
```

---

## 📋 CHECKLIST

Before moving forward:

- [ ] 4 backend servers running (see Part 1)
- [ ] `claude.json` created in project folder
- [ ] Claude Desktop installed
- [ ] `claude_desktop_config.json` created in C:\Users\harsh\AppData\Roaming\Claude\
- [ ] Claude Desktop restarted
- [ ] No red errors shown in Claude

---

## 🧪 TEST IT!

Once setup, open Claude Desktop and type:

```
What flights are available from Pune to Delhi?
```

**You should see Claude responding with flight data!**

If you get error, check:

1. Are all 4 backend servers still running?
2. Did you paste the JSON correctly?
3. Is Claude Desktop restarted?

---

## ❓ TROUBLESHOOTING

### "Servers not connecting"

- Check all 4 terminals are showing "Listening for connections..."
- Restart servers: Ctrl+C in each terminal, run again

### "Claude doesn't recognize my servers"

- Check `claude_desktop_config.json` path (must be exact)
- Make sure no typos in file paths
- Use full paths (C:\Users\...) not relative paths

### "JSON error"

- Use online tool: https://jsonlint.com/
- Paste your JSON to validate
- Copy back the corrected version

### "Python: command not found"

- Make sure Python is installed
- Run: `python --version`
- If error, reinstall Python

---

## 🎉 WHAT HAPPENS NEXT

Once everything works:

1. **Ask Claude anything travel-related**
   - "Find hotels in Kerala under ₹5000"
   - "What's the weather in Goa next week?"
   - "Plan a 5-day trip with flights, hotels, and events"

2. **Claude automatically:**
   - Calls your flight server
   - Calls your hotel server
   - Calls your event server
   - Calls your weather server
   - Combines results beautifully

3. **Show to clients:**
   - Open Claude Desktop
   - Ask a travel question
   - Let Claude show the magic! ✨

---

## 📞 SUMMARY

| What            | Where            | How                                 |
| --------------- | ---------------- | ----------------------------------- |
| **4 Servers**   | 4 terminals      | Run Python commands (Part 1)        |
| **JSON Config** | Project folder   | Create `claude.json` file (Part 2)  |
| **Desktop App** | Your computer    | Download from claude.ai             |
| **Config File** | AppData\Claude\  | Create `claude_desktop_config.json` |
| **Testing**     | Claude Desktop   | Type travel questions               |

---

**Ready? Start with Part 1 - Open those 4 terminals! 🚀**

Let me know if you need help with any step!
