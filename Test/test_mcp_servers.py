"""
ADVANCED TESTING - Direct MCP Server Testing
This script tests the actual MCP server implementations
"""

import subprocess
import time
import json
import requests

print("\n" + "="*80)
print("MCP SERVER HEALTH CHECK")
print("="*80)

# MCP servers typically run on localhost with different ports
# Flight: http://localhost:8000
# Hotel: http://localhost:8001
# Event: http://localhost:8002
# Weather: http://localhost:8003

SERVERS = {
    "flight": {"port": 8000, "name": "Flight Server", "file": "servers/flight_server/flight_server.py"},
    "hotel": {"port": 8001, "name": "Hotel Server", "file": "servers/hotel_server/hotel_server.py"},
    "event": {"port": 8002, "name": "Event Server", "file": "servers/event_server/event_server.py"},
    "weather": {"port": 8003, "name": "Weather Server", "file": "servers/weather_server/weather_server.py"},
}

def check_server_health(server_key, server_info):
    """Check if MCP server is running and healthy"""
    try:
        url = f"http://localhost:{server_info['port']}/health"
        response = requests.get(url, timeout=2)
        
        if response.status_code == 200:
            print(f"✅ {server_info['name']}: RUNNING")
            return True
        else:
            print(f"⚠️  {server_info['name']}: Responding but unexpected status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ {server_info['name']}: NOT RUNNING (connection refused)")
        return False
    except Exception as e:
        print(f"❌ {server_info['name']}: ERROR - {str(e)}")
        return False

# Check all servers
print("\nChecking Server Status:\n")
running_servers = 0

for server_key, server_info in SERVERS.items():
    if check_server_health(server_key, server_info):
        running_servers += 1

print(f"\nServers Running: {running_servers}/{len(SERVERS)}")

# If not all servers running, show how to start them
if running_servers < len(SERVERS):
    print("\n" + "="*80)
    print("SERVERS NOT RUNNING - START THEM WITH:")
    print("="*80)
    for server_key, server_info in SERVERS.items():
        print(f"\nTerminal {server_key.upper()}:")
        print(f"  python {server_info['file']}")

print("\n" + "="*80)
print("MANUAL TESTING GUIDE")
print("="*80)

print("""
To manually test the MCP servers, you can:

1. Test with cURL:
   
   # Test flight search
   curl -X POST http://localhost:8000/search_flight \\
     -H "Content-Type: application/json" \\
     -d '{
       "departure_id": "PNQ",
       "arrival_id": "BLR",
       "outbound_date": "2026-04-15"
     }'

2. Test with Python:
   
   import requests
   
   # Test flight server
   response = requests.post(
       'http://localhost:8000/search_flight',
       json={
           'departure_id': 'PNQ',
           'arrival_id': 'BLR',
           'outbound_date': '2026-04-15'
       }
   )
   print(response.json())

3. Use MCP Client Tools:
   
   # If you have MCP CLI tools installed
   mcp call flight-server search_flight \\
     --departure_id PNQ \\
     --arrival_id BLR \\
     --outbound_date 2026-04-15

4. Integration Testing with Claude or other LLMs:
   - Configure MCP servers in your LLM client
   - Ask the LLM to search for flights, hotels, etc.
   - The LLM will use the MCP tools automatically
""")

print("="*80)
