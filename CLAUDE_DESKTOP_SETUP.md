# 🖥️ CLAUDE DESKTOP SETUP - EXACT STEPS FOR YOUR PROJECT

## 📍 YOUR PROJECT INFO

**Your Project Location:**

```
C:\Users\harsh\Desktop\VS_code\TravelAssistant-ranjit\TravelAssistant-ranjit
```

**Your 4 Servers:**

```
1. Flight:   servers/flight_server/flight_server.py
2. Hotel:    servers/hotel_server/hotel_server.py
3. Event:    servers/event_server/event_server.py
4. Weather:  servers/weather_server/weather_server.py
```

---

## ✅ STEP 1: START THE 4 BACKEND SERVERS

### Open 4 PowerShell Windows

In VS Code, press `Ctrl + Shift + J` to open terminal, then use the `+` button to open 3 more tabs.

### Terminal 1 - Flight Server

```powershell
cd C:\Users\harsh\Desktop\VS_code\TravelAssistant-ranjit\TravelAssistant-ranjit
python servers/flight_server/flight_server.py
```

**Wait for:**

```
✈️  FLIGHT SERVER
Starting on port 8001
Listening for connections...
```

### Terminal 2 - Hotel Server

```powershell
cd C:\Users\harsh\Desktop\VS_code\TravelAssistant-ranjit\TravelAssistant-ranjit
python servers/hotel_server/hotel_server.py
```

**Wait for:**

```
🏨 HOTEL SERVER
Starting on port 8002
Listening for connections...
```

### Terminal 3 - Event Server

```powershell
cd C:\Users\harsh\Desktop\VS_code\TravelAssistant-ranjit\TravelAssistant-ranjit
python servers/event_server/event_server.py
```

**Wait for:**

```
🎉 EVENT SERVER
Starting on port 8003
Listening for connections...
```

### Terminal 4 - Weather Server

```powershell
cd C:\Users\harsh\Desktop\VS_code\TravelAssistant-ranjit\TravelAssistant-ranjit
python servers/weather_server/weather_server.py
```

**Wait for:**

```
🌦️  WEATHER SERVER
Starting on port 8004
Listening for connections...
```

✅ **Keep all 4 running!**

---

## ✅ STEP 2: LOCATE CLAUDE DESKTOP CONFIG FILE

### Option A: Using File Explorer (Easy)

1. Press `Windows Key + R`
2. Type: `%APPDATA%\Claude`
3. Press Enter

You should see a folder open. If not, create it:

- Right-click in empty space
- Click "New Folder"
- Name: `Claude`

---

### Option B: Using PowerShell

Open new PowerShell and type:

```powershell
$path = "$env:APPDATA\Claude"
if (-not (Test-Path $path)) {
    New-Item -ItemType Directory -Path $path
}
Explorer.exe $path
```

---

## ✅ STEP 3: CREATE CLAUDE DESKTOP CONFIG FILE

### Inside the Claude folder:

1. Right-click in empty space
2. Click "New" → "Text Document"
3. Name it: `claude_desktop_config.json`

### Or using PowerShell:

```powershell
$path = "$env:APPDATA\Claude\claude_desktop_config.json"
New-Item -ItemType File -Path $path -Force
```

---

## ✅ STEP 4: EDIT THE CONFIG FILE

### Open the file with Notepad or VS Code:

**Option A: Right-click → "Open with" → "Notepad"**

**Option B: In VS Code → File → Open → Navigate to %APPDATA%\Claude\claude_desktop_config.json**

---

### COPY THIS ENTIRE TEXT:

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

**Important Notes:**

- ✅ Use `\\` (double backslashes) in Windows paths
- ✅ Include full paths (not relative)
- ✅ `"command": "python"` - uses Python to run servers
- ✅ `"args"` - full path to each server file

---

### Paste into the file:

1. Select all existing text (Ctrl + A)
2. Delete it
3. Paste the JSON above
4. **Save file** (Ctrl + S)

---

## ✅ STEP 5: DOWNLOAD CLAUDE DESKTOP

Go to: https://claude.ai/download

- Click "Windows"
- Download the installer
- Run it and install

---

## ✅ STEP 6: VERIFY CONFIG FILE CONTENTS

### Check that file looks like this:

Open: `%APPDATA%\Claude\claude_desktop_config.json`

Should have:

```
✅ 4 server entries (flight, hotel, event, weather)
✅ Full paths with \\ backslashes
✅ "command": "python"
✅ Proper JSON formatting (no extra commas)
```

**To validate JSON**, go to: https://jsonlint.com/

- Paste your JSON
- Click "Validate"
- Should show "✅ Valid JSON"

---

## ✅ STEP 7: RESTART CLAUDE DESKTOP

1. **Close Claude Desktop completely** (Quit from system tray)
2. **Wait 5 seconds**
3. **Reopen Claude Desktop**
4. You should see a **"Model Context Protocol"** indicator showing your servers connected

---

## ✅ STEP 8: TEST THE CONNECTION

### In Claude Desktop, type:

```
What MCP servers are you connected to?
```

Claude should respond:

```
I'm connected to:
- flight-server
- hotel-server
- event-server
- weather-server
```

If you see this, **you're connected!** ✅

---

## ✅ STEP 9: USE IT!

Now type travel questions:

```
Find me flights from Pune to Jaipur for February 20-23
```

Claude will:

1. ✅ Call your flight server
2. ✅ Get real flight data from SerpAPI
3. ✅ Show you beautiful results

Or ask:

```
Find hotels in Jaipur, events happening there, and the weather for Feb 20-23
```

Claude will:

1. ✅ Call ALL 4 servers
2. ✅ Combine results
3. ✅ Show everything nicely formatted!

---

## 🔍 TROUBLESHOOTING

### Problem 1: "Config file not found"

**Solution:**

- Make sure file path is: `C:\Users\harsh\AppData\Roaming\Claude\claude_desktop_config.json`
- Check AppData folder is visible (View → Hidden items)
- Create Claude folder if missing

---

### Problem 2: "Invalid JSON error"

**Solution:**

- Validate JSON at https://jsonlint.com/
- Check for:
  - Missing commas between server blocks
  - Extra commas at end
  - Typos in quotes
  - Unmatched brackets

---

### Problem 3: "Servers not connecting"

**Check:**

- [ ] All 4 backend servers running in terminals?
- [ ] Config file paths are FULL paths?
- [ ] Paths use `\\` (double backslash)?
- [ ] Claude Desktop fully restarted?
- [ ] No Python errors in terminal?

**Fix:**

- Restart Claude Desktop completely
- Check each terminal shows "Listening for connections..."

---

### Problem 4: "Can't find Python"

**Solution:**

- Make sure Python installed: `python --version`
- Use full Python path in config if needed:
  ```json
  "command": "C:\\Users\\harsh\\AppData\\Local\\Programs\\Python\\Python313\\python.exe"
  ```

---

### Problem 5: "JSON says 'comma expected' at line X"

**Solution:**

- Use online validator: https://jsonlint.com/
- Copy your JSON there
- It will show exact error location with fix

---

## 📋 VERIFICATION CHECKLIST

Before testing, verify:

- [ ] 4 terminals showing "Listening for connections..."
- [ ] File created: `C:\Users\harsh\AppData\Roaming\Claude\claude_desktop_config.json`
- [ ] File size > 500 bytes (not empty)
- [ ] JSON validates at jsonlint.com
- [ ] Claude Desktop installed and working
- [ ] Claude Desktop fully closed and reopened
- [ ] No Python error messages in terminals

---

## 🎯 QUICK REFERENCE

| What           | Location                                      |
| -------------- | --------------------------------------------- |
| Config file    | `%APPDATA%\Claude\claude_desktop_config.json` |
| Flight server  | `servers/flight_server/flight_server.py`      |
| Hotel server   | `servers/hotel_server/hotel_server.py`        |
| Event server   | `servers/event_server/event_server.py`        |
| Weather server | `servers/weather_server/weather_server.py`    |
| Claude Desktop | Download from https://claude.ai/download      |

---

## 📊 WHAT HAPPENS AFTER SETUP

```
YOU (in Claude): "Find flights from Pune to Jaipur"
         ↓
CLAUDE DESKTOP: Recognizes the request
         ↓
CALLS YOUR SERVER: flight_server.py on port 8001
         ↓
SERVER CALLS API: Hits SerpAPI
         ↓
GETS RESULTS: Real flight data
         ↓
CLAUDE FORMATS: Beautiful results
         ↓
YOU READ: Flight options with prices! ✨
```

---

## 🎉 YOU'RE READY!

**All steps done?**
→ Open Claude Desktop
→ Type: "Find flights from Pune to Delhi"
→ Watch the magic! ✨

---

**Need help?** Let me know which step you're stuck on!
