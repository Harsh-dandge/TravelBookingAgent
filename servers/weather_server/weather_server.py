import json
import logging
import os
from datetime import date, datetime
from statistics import mean
from typing import Any, Dict

import requests
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from utils import (
    HTTP_SESSION,
    get_data_dir,
    get_request_timeout,
    get_search_file,
    make_search_id,
    parse_iso_date,
    require_text,
)

load_dotenv()
logger = logging.getLogger(__name__)
mcp = FastMCP("weather-server")
WEATHER_DIR = get_data_dir("weather")
FORECAST_DAYS = 15


def get_coordinates(place: str) -> dict:
    place = require_text(place, "place")
    response = HTTP_SESSION.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": place, "count": 1},
        timeout=get_request_timeout(),
    )
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, dict):
        raise ValueError("Geocoding provider returned an invalid response")
    results = data.get("results") or []
    if not results:
        raise ValueError(f"Location not found: {place}")
    result = results[0]
    return {
        "latitude": result["latitude"],
        "longitude": result["longitude"],
        "resolved_name": result.get("name", place),
        "admin1": result.get("admin1", ""),
        "country": result.get("country", ""),
    }


def analyze_hourly(hourly: dict, target_date: str) -> dict:
    rain = hourly.get("rain") or []
    cloudcover = hourly.get("cloudcover") or []
    humidity = hourly.get("relativehumidity_2m") or []
    wind = hourly.get("windspeed_10m") or []

    rainy_hours = sum(1 for amount in rain if amount > 0)
    rain_probability = (rainy_hours / len(rain)) * 100 if rain else 0
    total_rain = sum(rain)
    avg_cloud = mean(cloudcover) if cloudcover else 0
    avg_humidity = mean(humidity) if humidity else 0
    max_wind = max(wind) if wind else 0

    thunderstorm = "Low"
    if avg_cloud > 70 and avg_humidity > 60:
        thunderstorm = "Moderate"
    if avg_humidity > 70 and max_wind > 30:
        thunderstorm = "High"

    return {
        "date": target_date,
        "rain_probability_percent": round(rain_probability, 1),
        "total_rain_mm": round(total_rain, 2),
        "average_cloud_cover_percent": round(avg_cloud, 1),
        "average_humidity_percent": round(avg_humidity, 1),
        "max_wind_speed_kmh": max_wind,
        "thunderstorm_likelihood": thunderstorm,
    }


@mcp.tool()
def get_weather(place: str, target_date: str) -> Dict[str, Any]:
    """Return a forecast up to 15 days ahead or historical weather for a date."""
    try:
        place = require_text(place, "place")
        requested_date = parse_iso_date(target_date, "target_date")
        today = date.today()
        if (requested_date - today).days > FORECAST_DAYS:
            raise ValueError("Forecast available only up to 15 days ahead")
        geo = get_coordinates(place)
        endpoint = (
            "https://api.open-meteo.com/v1/forecast"
            if requested_date >= today
            else "https://archive-api.open-meteo.com/v1/archive"
        )
        params = {
            "latitude": geo["latitude"],
            "longitude": geo["longitude"],
            "start_date": requested_date.isoformat(),
            "end_date": requested_date.isoformat(),
            "hourly": "rain,cloudcover,relativehumidity_2m,windspeed_10m",
            "timezone": "auto",
        }
        response = HTTP_SESSION.get(
            endpoint, params=params, timeout=get_request_timeout()
        )
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, dict):
            raise ValueError("Weather provider returned an invalid response")
        hourly = data.get("hourly")
        if not isinstance(hourly, dict):
            raise ValueError("Weather provider returned no hourly data")

        summary = analyze_hourly(hourly, requested_date.isoformat())
        search_id = make_search_id(
            geo["resolved_name"],
            requested_date.isoformat(),
            datetime.now().strftime("%Y%m%d_%H%M%S_%f"),
        )
        os.makedirs(WEATHER_DIR, exist_ok=True)
        with get_search_file(WEATHER_DIR, search_id).open(
            "w", encoding="utf-8"
        ) as file:
            json.dump(data, file, indent=2)

        summary.update(
            {
                "search_id": search_id,
                "location": geo["resolved_name"],
                "state_or_region": geo["admin1"],
                "country": geo["country"],
                "coordinates": {
                    "latitude": geo["latitude"],
                    "longitude": geo["longitude"],
                },
            }
        )
        return summary
    except requests.RequestException as exc:
        logger.warning("Weather provider request failed (%s)", type(exc).__name__)
        return {"error": "Weather provider request failed; please retry shortly"}
    except (ValueError, TypeError, KeyError, OSError) as exc:
        logger.warning("Weather request rejected or could not be saved: %s", exc)
        return {"error": str(exc)}


@mcp.tool()
def get_weather_details(search_id: str) -> str:
    """Return the saved raw weather response as JSON."""
    try:
        path = get_search_file(WEATHER_DIR, search_id)
        with path.open(encoding="utf-8") as file:
            return json.dumps(json.load(file), indent=2)
    except (ValueError, FileNotFoundError, json.JSONDecodeError, OSError) as exc:
        return f"Unable to read weather search: {exc}"


@mcp.resource("weather://searches")
def list_weather_searches() -> str:
    """List IDs of saved weather searches."""
    if not os.path.isdir(WEATHER_DIR):
        return "No weather searches found."
    searches = sorted(
        filename[:-5]
        for filename in os.listdir(WEATHER_DIR)
        if filename.endswith(".json")
    )
    return json.dumps(searches, indent=2) if searches else "No weather searches found."


@mcp.prompt()
def weather_analysis_prompt(destination: str, travel_date: str) -> str:
    return (
        f"Check the weather for {destination} on {travel_date}. Report the "
        "provider forecast, precipitation, wind, and humidity. Identify the "
        "thunderstorm value as a rough heuristic rather than an official warning."
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
