# 🧪 TRAVEL ASSISTANT - TESTING GUIDE

## Quick Reference - Run Tests

```powershell
# Run comprehensive test (tests all 4 servers)
python Test/test_all_servers.py

# Run individual tests
python Test/test_flight.py        # Flight API
python Test/weatherapi.py         # Weather API
python Test/geocode.py            # Location Geocoding
python Test/test1.py              # Flight Response Parsing
```

---

## Testing Strategies

### **1. API Connection Tests** ✅

Tests if APIs are reachable and responding

**File:** [Test/test_all_servers.py](Test/test_all_servers.py)

Tests:

- ✅ Flight API (Google Flights)
- ✅ Hotel API (Google Hotels)
- ✅ Event API (Google Events)
- ✅ Weather API (Open-Meteo)

**Run:** `python Test/test_all_servers.py`

---

### **2. Individual Component Tests**

#### **Flight Server Tests**

```powershell
python Test/test_flight.py
```

- Tests flight search with real parameters
- Departure: PNQ (Pune)
- Arrival: JAI (Jaipur)
- Validates HTTP response status

#### **Weather API Tests**

```powershell
python Test/weatherapi.py
```

- Tests Open-Meteo weather API
- Retrieves hourly precipitation data
- Validates weather data structure

#### **Geocoding Tests**

```powershell
python Test/geocode.py
```

- Tests location geocoding
- Converts city names to coordinates
- Example: "Jodhpur" → (26.26841, 73.00594)

#### **Response Parsing Tests**

```powershell
python Test/test1.py
```

- Parses flight response JSON
- Extracts flight details (airline, duration, price)
- Validates data structure

---

### **3. Testing Specific Scenarios**

#### Scenario 1: Search Flights

```python
import requests

params = {
    "engine": "google_flights",
    "api_key": YOUR_API_KEY,
    "departure_id": "PNQ",
    "arrival_id": "BLR",
    "outbound_date": "2026-04-15",
    "return_date": "2026-04-20",
    "type": 1,  # round trip
    "adults": 2
}

response = requests.get("https://serpapi.com/search", params=params)
print(response.json())
```

#### Scenario 2: Search Hotels

```python
params = {
    "q": "Hotels in Mumbai",
    "check_in_date": "2026-04-15",
    "check_out_date": "2026-04-17",
    "adults": 2,
    "sort_by": 8,  # highest rating
    "api_key": YOUR_API_KEY
}

response = requests.get("https://serpapi.com/search", params=params)
print(response.json())
```

#### Scenario 3: Get Weather

```python
# Step 1: Get coordinates
geocode_params = {"name": "Delhi", "count": 1}
geocode = requests.get("https://geocoding-api.open-meteo.com/v1/search", params=geocode_params)
coords = geocode.json()["results"][0]

# Step 2: Get weather
weather_params = {
    "latitude": coords["latitude"],
    "longitude": coords["longitude"],
    "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum"
}
weather = requests.get("https://api.open-meteo.com/v1/forecast", params=weather_params)
print(weather.json())
```

---

## Testing Checklist

### Pre-Testing

- [ ] `.env` file has valid `SERPAPI_KEY`
- [ ] Internet connection is active
- [ ] All dependencies installed (`pip install -r requirements.txt`)

### API Tests

- [ ] Flight search returns data
- [ ] Hotel search returns data
- [ ] Event search responds
- [ ] Weather API responds
- [ ] Geocoding works for cities

### Data Validation

- [ ] Flight prices are numbers
- [ ] Hotel ratings are valid
- [ ] Temperature values are realistic
- [ ] Coordinates are valid lat/long

### Edge Cases

- [ ] Past dates are rejected
- [ ] Invalid city names raise errors
- [ ] Missing API key raises error
- [ ] No results returns empty list (not error)

---

## Expected Test Results

### ✅ All Green

```
✅ Flight API Connection: SUCCESS
✅ Hotel API Connection: SUCCESS
✅ Event API Connection: SUCCESS
✅ Geocoding API Connection: SUCCESS
✅ Weather API Connection: SUCCESS
```

### Common Errors & Fixes

| Error                           | Cause                 | Fix                         |
| ------------------------------- | --------------------- | --------------------------- |
| `ModuleNotFoundError: requests` | Missing dependency    | `pip install requests`      |
| `cannot fetch api key`          | `.env` not configured | Add `SERPAPI_KEY` to `.env` |
| `cannot be in the past`         | Test date is in past  | Use tomorrow's date         |
| `429 Too Many Requests`         | API rate limit        | Wait 1 hour / upgrade plan  |

---

## Test Execution Commands

```powershell
# CD to project directory
cd c:\Users\harsh\Desktop\VS_code\TravelAssistant-ranjit\TravelAssistant-ranjit

# Run comprehensive test
python Test/test_all_servers.py

# Run flight test
python Test/test_flight.py

# Run weather test
python Test/weatherapi.py

# Run geocoding test
python Test/geocode.py

# Test response parsing
python Test/test1.py
```

---

## Next Steps

After testing:

1. ✅ Verify all services respond
2. ✅ Check API keys are valid
3. ✅ Test with different locations/dates
4. ✅ Validate response data structure
5. ✅ Ready to integrate with LLMs!

---

**Happy Testing! 🚀**
