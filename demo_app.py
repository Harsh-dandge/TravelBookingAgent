import logging
import os
from datetime import date

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

from utils import (
    HTTP_SESSION,
    get_api_key,
    get_request_timeout,
    parse_iso_date,
    require_text,
    validate_date_range,
)

load_dotenv()
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper())
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024


class ApiConfigurationError(Exception):
    pass


class ProviderResponseError(Exception):
    pass


def _payload() -> dict:
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValueError("Request body must be a JSON object")
    return data


def _serpapi_search(params: dict) -> dict:
    try:
        params["api_key"] = get_api_key()
    except ValueError as exc:
        raise ApiConfigurationError("SERPAPI_KEY is not configured") from exc
    response = HTTP_SESSION.get(
        "https://serpapi.com/search", params=params, timeout=get_request_timeout()
    )
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, dict):
        raise ProviderResponseError("Search provider returned an invalid response")
    if data.get("error"):
        raise ProviderResponseError("Search provider could not complete the search")
    return data


def _validate_passengers(value: object, name: str, default: int, maximum: int) -> int:
    if value is None:
        return default
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= maximum:
        raise ValueError(f"{name} must be an integer from 1 to {maximum}")
    return value


@app.errorhandler(413)
def request_too_large(_error):
    return jsonify({"success": False, "error": "Request body is too large"}), 413


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/flights", methods=["POST"])
def search_flights():
    try:
        data = _payload()
        departure = require_text(data.get("departure"), "departure", 8).upper()
        arrival = require_text(data.get("arrival"), "arrival", 8).upper()
        if not departure.isalnum() or len(departure) < 3:
            raise ValueError("departure must be a valid airport or city code")
        if not arrival.isalnum() or len(arrival) < 3:
            raise ValueError("arrival must be a valid airport or city code")
        if departure == arrival:
            raise ValueError("Departure and arrival must be different")
        outbound = parse_iso_date(data.get("date"), "date")
        if outbound < date.today():
            raise ValueError("date cannot be in the past")

        return_date = data.get("return_date") or None
        if return_date:
            returned = parse_iso_date(return_date, "return_date")
            validate_date_range(outbound, returned, "date", "return_date")
        adults = _validate_passengers(data.get("adults"), "adults", 1, 9)
        children = data.get("children", 0)
        if isinstance(children, bool) or not isinstance(children, int) or not 0 <= children <= 9:
            raise ValueError("children must be an integer from 0 to 9")

        result = _serpapi_search(
            {
                "engine": "google_flights",
                "departure_id": departure,
                "arrival_id": arrival,
                "outbound_date": outbound.isoformat(),
                "return_date": return_date,
                "type": 1 if return_date else 2,
                "adults": adults,
                "children": children,
                "currency": "INR",
                "gl": "in",
                "hl": "en",
                "max_results": 10,
            }
        )
        best_flights = result.get("best_flights") or []
        other_flights = result.get("other_flights") or []
        if not isinstance(best_flights, list) or not isinstance(other_flights, list):
            raise ProviderResponseError("Flight provider returned an invalid results list")
        flights = best_flights + other_flights
        if any(not isinstance(flight, dict) for flight in flights):
            raise ProviderResponseError("Flight provider returned an invalid flight record")
        formatted = [
            {
                "price": flight.get("price"),
                "duration": flight.get("total_duration", flight.get("duration")),
                "airline": ", ".join(
                    dict.fromkeys(
                        segment.get("airline", "N/A")
                        for segment in flight.get("flights", [])
                        if isinstance(segment, dict)
                    )
                )
                or flight.get("airline", "N/A"),
                "departure_time": (flight.get("flights") or [{}])[0]
                .get("departure_airport", {})
                .get("time", "N/A"),
                "arrival_time": (flight.get("flights") or [{}])[-1]
                .get("arrival_airport", {})
                .get("time", "N/A"),
                "stops": max(len(flight.get("flights") or []) - 1, 0),
            }
            for flight in flights[:5]
        ]
        return jsonify({"success": True, "flights": formatted, "count": len(formatted)})
    except ApiConfigurationError as exc:
        return jsonify({"success": False, "error": str(exc)}), 503
    except ProviderResponseError as exc:
        logger.warning("%s", exc)
        return jsonify({"success": False, "error": str(exc)}), 502
    except requests.RequestException as exc:
        logger.warning("Flight provider request failed (%s)", type(exc).__name__)
        return jsonify({"success": False, "error": "Flight search failed; please retry shortly"}), 502
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400


@app.route("/api/hotels", methods=["POST"])
def search_hotels():
    try:
        data = _payload()
        location = require_text(data.get("location"), "location")
        check_in = parse_iso_date(data.get("check_in"), "check_in")
        check_out = parse_iso_date(data.get("check_out"), "check_out")
        validate_date_range(check_in, check_out, "check_in", "check_out")
        if check_in < date.today():
            raise ValueError("check_in cannot be in the past")
        guests = _validate_passengers(data.get("guests"), "guests", 2, 30)
        result = _serpapi_search(
            {
                "engine": "google_hotels",
                "q": f"Hotels in {location}",
                "check_in_date": check_in.isoformat(),
                "check_out_date": check_out.isoformat(),
                "currency": "INR",
                "hl": "en",
                "adults": guests,
                "sort_by": 8,
            }
        )
        hotels = result.get("properties") or []
        if not isinstance(hotels, list) or any(
            not isinstance(hotel, dict) for hotel in hotels
        ):
            raise ProviderResponseError("Hotel provider returned an invalid results list")
        formatted = [
            {
                "name": hotel.get("name", hotel.get("title", "N/A")),
                "price": (hotel.get("rate_per_night") or {}).get(
                    "lowest", hotel.get("price", "N/A")
                ),
                "rating": hotel.get("overall_rating", hotel.get("rating", "N/A")),
                "reviews": hotel.get("reviews", hotel.get("review_count", 0)),
                "address": hotel.get("address", "N/A"),
                "image": hotel.get("images", [{}])[0].get("thumbnail", "")
                if hotel.get("images")
                else hotel.get("image", ""),
            }
            for hotel in hotels[:5]
        ]
        return jsonify({"success": True, "hotels": formatted, "count": len(formatted)})
    except ApiConfigurationError as exc:
        return jsonify({"success": False, "error": str(exc)}), 503
    except ProviderResponseError as exc:
        logger.warning("%s", exc)
        return jsonify({"success": False, "error": str(exc)}), 502
    except requests.RequestException as exc:
        logger.warning("Hotel provider request failed (%s)", type(exc).__name__)
        return jsonify({"success": False, "error": "Hotel search failed; please retry shortly"}), 502
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400


@app.route("/api/events", methods=["POST"])
def search_events():
    try:
        data = _payload()
        event_type = require_text(data.get("event_type"), "event_type")
        location = require_text(data.get("location"), "location")
        result = _serpapi_search(
            {
                "engine": "google_events",
                "q": f"{event_type} in {location}",
                "hl": "en",
                "gl": "in",
            }
        )
        events = result.get("events_results") or []
        if not isinstance(events, list) or any(
            not isinstance(item, dict) for item in events
        ):
            raise ProviderResponseError("Event provider returned an invalid results list")
        formatted = [
            {
                "title": event.get("title", "N/A"),
                "date": (event.get("date") or {}).get("when", "N/A")
                if isinstance(event.get("date"), dict)
                else event.get("date", "N/A"),
                "location": (event.get("venue") or {}).get("name", location)
                if isinstance(event.get("venue"), dict)
                else location,
                "ticket_price": event.get("ticket_price", "N/A"),
                "event_link": event.get("link", ""),
            }
            for event in events[:5]
        ]
        return jsonify({"success": True, "events": formatted, "count": len(formatted)})
    except ApiConfigurationError as exc:
        return jsonify({"success": False, "error": str(exc)}), 503
    except ProviderResponseError as exc:
        logger.warning("%s", exc)
        return jsonify({"success": False, "error": str(exc)}), 502
    except requests.RequestException as exc:
        logger.warning("Event provider request failed (%s)", type(exc).__name__)
        return jsonify({"success": False, "error": "Event search failed; please retry shortly"}), 502
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400


@app.route("/api/weather", methods=["POST"])
def get_weather():
    try:
        data = _payload()
        location = require_text(data.get("location"), "location")
        geocode_response = HTTP_SESSION.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": location, "count": 1},
            timeout=get_request_timeout(),
        )
        geocode_response.raise_for_status()
        geocode_data = geocode_response.json()
        if not isinstance(geocode_data, dict):
            raise ProviderResponseError("Geocoding provider returned an invalid response")
        results = geocode_data.get("results") or []
        if not results:
            return jsonify({"success": False, "error": "Location not found"}), 404
        coordinates = results[0]
        weather_response = HTTP_SESSION.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": coordinates["latitude"],
                "longitude": coordinates["longitude"],
                "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code",
                "forecast_days": 5,
                "timezone": "auto",
            },
            timeout=get_request_timeout(),
        )
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        if not isinstance(weather_data, dict):
            raise ProviderResponseError("Weather provider returned an invalid response")
        daily = weather_data.get("daily") or {}
        dates = daily.get("time") or []
        formatted = []
        for index, forecast_date in enumerate(dates[:5]):
            formatted.append(
                {
                    "date": forecast_date,
                    "temp_max": (daily.get("temperature_2m_max") or [])[index],
                    "temp_min": (daily.get("temperature_2m_min") or [])[index],
                    "precipitation": (daily.get("precipitation_sum") or [])[index],
                    "weather_code": (daily.get("weather_code") or [])[index],
                }
            )
        return jsonify(
            {
                "success": True,
                "location": coordinates.get("name", location),
                "weather": formatted,
            }
        )
    except ProviderResponseError as exc:
        logger.warning("%s", exc)
        return jsonify({"success": False, "error": str(exc)}), 502
    except (KeyError, IndexError, TypeError) as exc:
        logger.warning("Weather provider returned invalid data (%s)", type(exc).__name__)
        return jsonify({"success": False, "error": "Weather provider returned invalid data"}), 502
    except requests.RequestException as exc:
        logger.warning("Weather provider request failed (%s)", type(exc).__name__)
        return jsonify({"success": False, "error": "Weather lookup failed; please retry shortly"}), 502
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400


@app.route("/api/demo")
def demo_data():
    return jsonify(
        {
            "message": "Live searches are available for flights, hotels, events, and weather.",
            "serpapi_searches_require_key": True,
            "weather_requires_key": False,
        }
    )


@app.route("/api/health")
def health():
    return jsonify({"status": "running", "version": "2.0.0"})


if __name__ == "__main__":
    app.run(
        host=os.getenv("FLASK_HOST", "127.0.0.1"),
        port=int(os.getenv("FLASK_PORT", "5000")),
        debug=os.getenv("FLASK_DEBUG", "false").casefold() == "true",
    )
