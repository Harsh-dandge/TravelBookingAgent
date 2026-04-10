"""
TRAVEL ASSISTANT - WEB DEMO INTERFACE
Simple Flask web UI to showcase the project to clients
"""

from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
API_KEY = os.getenv("SERPAPI_KEY")

# ==================== ROUTES ====================

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('index.html')

# ==================== FLIGHT ENDPOINTS ====================

@app.route('/api/flights', methods=['POST'])
def search_flights():
    """Search for flights"""
    try:
        data = request.json
        
        params = {
            "engine": "google_flights",
            "api_key": API_KEY,
            "departure_id": data.get('departure'),
            "arrival_id": data.get('arrival'),
            "outbound_date": data.get('date'),
            "return_date": data.get('return_date'),
            "type": 1 if data.get('return_date') else 2,
            "adults": data.get('adults', 1),
            "children": data.get('children', 0),
            "currency": "INR",
            "max_results": 10
        }
        
        response = requests.get("https://serpapi.com/search", params=params)
        flights = response.json().get('best_flights', [])
        
        # Format for frontend
        formatted_flights = []
        for flight in flights[:5]:  # Limit to 5 results
            formatted_flights.append({
                'price': flight.get('price'),
                'duration': flight.get('duration'),
                'airline': flight.get('airline', 'N/A'),
                'departure_time': flight.get('departure_time', 'N/A'),
                'arrival_time': flight.get('arrival_time', 'N/A'),
                'stops': flight.get('stops', 0)
            })
        
        return jsonify({
            'success': True,
            'flights': formatted_flights,
            'count': len(formatted_flights)
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ==================== HOTEL ENDPOINTS ====================

@app.route('/api/hotels', methods=['POST'])
def search_hotels():
    """Search for hotels"""
    try:
        data = request.json
        
        params = {
            "q": f"Hotels in {data.get('location')}",
            "check_in_date": data.get('check_in'),
            "check_out_date": data.get('check_out'),
            "engine": "google_hotels",
            "currency": "INR",
            "hl": "en",
            "adults": data.get('guests', 2),
            "sort_by": 8,  # highest rating
            "api_key": API_KEY
        }
        
        response = requests.get("https://serpapi.com/search", params=params)
        hotels = response.json().get('properties', [])
        
        # Format for frontend
        formatted_hotels = []
        for hotel in hotels[:5]:  # Limit to 5 results
            formatted_hotels.append({
                'name': hotel.get('title', 'N/A'),
                'price': hotel.get('price', 'N/A'),
                'rating': hotel.get('rating', 'N/A'),
                'reviews': hotel.get('review_count', 0),
                'address': hotel.get('address', 'N/A'),
                'image': hotel.get('image', '')
            })
        
        return jsonify({
            'success': True,
            'hotels': formatted_hotels,
            'count': len(formatted_hotels)
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ==================== EVENT ENDPOINTS ====================

@app.route('/api/events', methods=['POST'])
def search_events():
    """Search for events"""
    try:
        data = request.json
        
        params = {
            "engine": "google_events",
            "api_key": API_KEY,
            "q": f"{data.get('event_type')} in {data.get('location')}",
            "hl": "en",
            "gl": "in"
        }
        
        response = requests.get("https://serpapi.com/search", params=params)
        events = response.json().get('events', [])
        
        # Format for frontend
        formatted_events = []
        for event in events[:5]:  # Limit to 5 results
            formatted_events.append({
                'title': event.get('title', 'N/A'),
                'date': event.get('date', 'N/A'),
                'location': event.get('location', 'N/A'),
                'ticket_price': event.get('ticket_price', 'N/A'),
                'event_link': event.get('event_link', '#')
            })
        
        return jsonify({
            'success': True,
            'events': formatted_events,
            'count': len(formatted_events)
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ==================== WEATHER ENDPOINTS ====================

@app.route('/api/weather', methods=['POST'])
def get_weather():
    """Get weather forecast"""
    try:
        data = request.json
        location = data.get('location')
        
        # Get coordinates
        geocode_params = {"name": location, "count": 1}
        geocode_response = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params=geocode_params
        )
        geocode_data = geocode_response.json()
        
        if not geocode_data.get('results'):
            return jsonify({'success': False, 'error': 'Location not found'}), 400
        
        coords = geocode_data['results'][0]
        
        # Get weather
        weather_params = {
            "latitude": coords["latitude"],
            "longitude": coords["longitude"],
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode",
            "timezone": "Asia/Kolkata"
        }
        
        weather_response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params=weather_params
        )
        weather_data = weather_response.json()
        
        # Format for frontend
        daily = weather_data.get('daily', {})
        formatted_weather = []
        
        for i, date in enumerate(daily.get('time', [])[:5]):  # 5-day forecast
            formatted_weather.append({
                'date': date,
                'temp_max': daily.get('temperature_2m_max', [])[i] if i < len(daily.get('temperature_2m_max', [])) else 'N/A',
                'temp_min': daily.get('temperature_2m_min', [])[i] if i < len(daily.get('temperature_2m_min', [])) else 'N/A',
                'precipitation': daily.get('precipitation_sum', [])[i] if i < len(daily.get('precipitation_sum', [])) else 0,
            })
        
        return jsonify({
            'success': True,
            'location': coords.get('name'),
            'weather': formatted_weather
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ==================== DEMO ENDPOINTS ====================

@app.route('/api/demo', methods=['GET'])
def demo_data():
    """Get demo data without API calls"""
    demo = {
        'flights': [
            {'price': '₹8,718', 'duration': '2h 30m', 'airline': 'IndiGo', 'stops': 0},
            {'price': '₹9,245', 'duration': '3h 15m', 'airline': 'Air India', 'stops': 0},
            {'price': '₹7,890', 'duration': '4h 45m', 'airline': 'SpiceJet', 'stops': 1},
        ],
        'hotels': [
            {'name': 'Taj Hotel', 'price': '₹8,500', 'rating': '4.8', 'reviews': 2450},
            {'name': 'ITC Hotel', 'price': '₹6,200', 'rating': '4.6', 'reviews': 1890},
            {'name': 'Marriott', 'price': '₹5,890', 'rating': '4.5', 'reviews': 1456},
        ],
        'events': [
            {'title': 'Jazz Festival', 'date': '2026-04-15', 'location': 'Jaipur'},
            {'title': 'Art Exhibition', 'date': '2026-04-20', 'location': 'Jaipur'},
            {'title': 'Cultural Show', 'date': '2026-04-25', 'location': 'Jaipur'},
        ],
        'weather': [
            {'date': '2026-04-10', 'temp_max': '33°C', 'temp_min': '19°C'},
            {'date': '2026-04-11', 'temp_max': '32°C', 'temp_min': '18°C'},
            {'date': '2026-04-12', 'temp_max': '31°C', 'temp_min': '17°C'},
        ]
    }
    return jsonify(demo)

# ==================== HEALTH CHECK ====================

@app.route('/api/health', methods=['GET'])
def health():
    """API health check"""
    return jsonify({'status': 'running', 'version': '1.0.0'})

if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║   TRAVEL ASSISTANT - WEB DEMO                             ║
    ║   🌐 http://localhost:5000                               ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    app.run(debug=True, port=5000)
