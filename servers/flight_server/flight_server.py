import json
import logging
import math
import os
from datetime import date
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from utils import (
    HTTP_SESSION,
    get_api_key,
    get_data_dir,
    get_request_timeout,
    get_search_file,
    make_search_id,
    parse_iso_date,
)

load_dotenv()
logger = logging.getLogger(__name__)
mcp = FastMCP("flight-server")
FLIGHT_DIR = get_data_dir("flights")


def _read_search(search_id: str) -> dict:
    path = get_search_file(FLIGHT_DIR, search_id)
    with path.open(encoding="utf-8") as file:
        return json.load(file)


@mcp.tool()
def search_flight(
    departure_id: str,
    arrival_id: str,
    outbound_date: str,
    return_date: Optional[str] = None,
    trip_type: int = 1,
    adults: int = 1,
    children: int = 0,
    infants_in_seat: int = 0,
    infants_on_lap: int = 0,
    travel_class: int = 1,
    currency: str = "INR",
    country: str = "in",
    language: str = "en",
    max_results: int = 10,
) -> Dict[str, Any]:
    """Search flights and save the provider response for later filtering."""
    try:
        departure_id = departure_id.strip().upper()
        arrival_id = arrival_id.strip().upper()
        if not (departure_id.isascii() and departure_id.isalnum() and 3 <= len(departure_id) <= 8):
            raise ValueError("departure_id must be a valid airport or city code")
        if not (arrival_id.isascii() and arrival_id.isalnum() and 3 <= len(arrival_id) <= 8):
            raise ValueError("arrival_id must be a valid airport or city code")
        if departure_id == arrival_id:
            raise ValueError("Departure and arrival must be different")
        outbound = parse_iso_date(outbound_date, "outbound_date")
        if outbound < date.today():
            raise ValueError("outbound_date cannot be in the past")
        if isinstance(trip_type, bool) or not isinstance(trip_type, int) or trip_type not in (1, 2):
            raise ValueError("trip_type must be 1 (round trip) or 2 (one way)")
        if trip_type == 1:
            if not return_date:
                raise ValueError("return_date is required for a round trip")
            returned = parse_iso_date(return_date, "return_date")
            if returned <= outbound:
                raise ValueError("return_date must be after outbound_date")
        elif return_date:
            raise ValueError("return_date is only valid for a round trip")
        passenger_counts = {
            "adults": (adults, 1, 9),
            "children": (children, 0, 9),
            "infants_in_seat": (infants_in_seat, 0, 9),
            "infants_on_lap": (infants_on_lap, 0, adults),
        }
        for name, (count, minimum, maximum) in passenger_counts.items():
            if isinstance(count, bool) or not isinstance(count, int) or not minimum <= count <= maximum:
                raise ValueError(f"{name} is outside the supported range")
        if adults + children + infants_in_seat + infants_on_lap > 9:
            raise ValueError("A search can include at most 9 passengers")
        if isinstance(travel_class, bool) or travel_class not in (1, 2, 3, 4):
            raise ValueError("travel_class must be between 1 and 4")
        if isinstance(max_results, bool) or not isinstance(max_results, int) or not 1 <= max_results <= 50:
            raise ValueError("max_results must be between 1 and 50")
        if not isinstance(currency, str) or not currency.isascii() or not currency.isalpha() or len(currency) != 3:
            raise ValueError("currency must be a 3-letter currency code")
        if not isinstance(country, str) or not country.isascii() or not country.isalpha() or len(country) != 2:
            raise ValueError("country must be a 2-letter country code")
        if not isinstance(language, str) or not language.isascii() or not language.isalpha() or not 2 <= len(language) <= 3:
            raise ValueError("language must be a 2- or 3-letter language code")

        params = {
            "engine": "google_flights",
            "api_key": get_api_key(),
            "departure_id": departure_id,
            "arrival_id": arrival_id,
            "outbound_date": outbound.isoformat(),
            "type": trip_type,
            "adults": adults,
            "children": children,
            "infants_in_seat": infants_in_seat,
            "infants_on_lap": infants_on_lap,
            "travel_class": travel_class,
            "currency": currency.upper(),
            "gl": country.lower(),
            "hl": language.lower(),
            "max_results": max_results,
        }
        if return_date:
            params["return_date"] = return_date

        response = HTTP_SESSION.get(
            "https://serpapi.com/search", params=params, timeout=get_request_timeout()
        )
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, dict):
            raise ValueError("Flight provider returned an invalid response")
        if data.get("error"):
            raise ValueError(f"Flight provider error: {data['error']}")

        best_flights = data.get("best_flights") or []
        other_flights = data.get("other_flights") or []
        if not isinstance(best_flights, list) or not isinstance(other_flights, list):
            raise ValueError("Flight provider returned an invalid results list")
        if any(not isinstance(flight, dict) for flight in best_flights + other_flights):
            raise ValueError("Flight provider returned an invalid flight record")
        search_id = make_search_id(
            departure_id,
            arrival_id,
            outbound.isoformat(),
            return_date,
            date.today().isoformat(),
        )
        record = {
            "search_metadata": {
                "search_id": search_id,
                "currency": currency.upper(),
                "created_at": date.today().isoformat(),
            },
            "search_parameters": params | {"api_key": "[redacted]"},
            "search_data": {
                "search_id": search_id,
                "departure_id": departure_id,
                "arrival_id": arrival_id,
                "outbound_date": outbound.isoformat(),
                "return_date": return_date,
                "trip_type": "Round Trip" if trip_type == 1 else "One Way",
                "adults": adults,
                "children": children,
                "infants_in_seat": infants_in_seat,
                "infants_on_lap": infants_on_lap,
                "currency": currency.upper(),
            },
            "best_flights": best_flights[:max_results],
            "other_flights": other_flights[:max_results],
            "price_insights": data.get("price_insights") or {},
        }
        os.makedirs(FLIGHT_DIR, exist_ok=True)
        with get_search_file(FLIGHT_DIR, search_id).open("w", encoding="utf-8") as file:
            json.dump(record, file, indent=2)

        return {
            "search_id": search_id,
            "route": f"{departure_id} -> {arrival_id}",
            "trip_type": record["search_data"]["trip_type"],
            "dates": {"outbound": outbound.isoformat(), "return": return_date},
            "passengers": adults + children + infants_in_seat + infants_on_lap,
            "best_flights_found": len(best_flights),
            "other_flights_found": len(other_flights),
            "price_insights": record["price_insights"],
        }
    except requests.RequestException as exc:
        logger.warning("Flight provider request failed (%s)", type(exc).__name__)
        return {"error": "Flight provider request failed; please retry shortly"}
    except (ValueError, TypeError, AttributeError, OSError) as exc:
        logger.warning("Flight search rejected or could not be saved: %s", exc)
        return {"error": str(exc)}


@mcp.tool()
def get_flight_details(search_id: str) -> str:
    """Return the saved flight search as JSON."""
    try:
        return json.dumps(_read_search(search_id), indent=2)
    except (ValueError, FileNotFoundError, json.JSONDecodeError, OSError) as exc:
        return f"Unable to read flight search: {exc}"


@mcp.tool()
def filter_flights_by_price(
    search_id: str,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
) -> str:
    """Filter saved flight options by inclusive price bounds."""
    try:
        for name, price in (("min_price", min_price), ("max_price", max_price)):
            if price is not None and (
                isinstance(price, bool)
                or not isinstance(price, (int, float))
                or not math.isfinite(price)
                or price < 0
            ):
                raise ValueError(f"{name} must be a finite non-negative number")
        if min_price is not None and max_price is not None and min_price > max_price:
            raise ValueError("min_price cannot exceed max_price")
        record = _read_search(search_id)

        def matches(flight: dict) -> bool:
            price = flight.get("price")
            if not isinstance(price, (int, float)):
                return False
            return (min_price is None or price >= min_price) and (
                max_price is None or price <= max_price
            )

        best = [flight for flight in record.get("best_flights", []) if matches(flight)]
        other = [flight for flight in record.get("other_flights", []) if matches(flight)]
        return json.dumps(
            {
                "search_id": search_id,
                "filters_applied": {"min_price": min_price, "max_price": max_price},
                "filtered_best_flights": best,
                "filtered_other_flights": other,
                "total_filtered": len(best) + len(other),
            },
            indent=2,
        )
    except (ValueError, FileNotFoundError, json.JSONDecodeError, OSError) as exc:
        return f"Unable to filter flight search: {exc}"


@mcp.resource("flights://searches")
def get_flight_searches() -> str:
    """List saved searches with route, dates, and available result counts."""
    if not os.path.isdir(FLIGHT_DIR):
        return "No flight searches found."
    searches = []
    for filename in sorted(os.listdir(FLIGHT_DIR)):
        if not filename.endswith(".json"):
            continue
        search_id = filename[:-5]
        try:
            record = _read_search(search_id)
        except (ValueError, FileNotFoundError, json.JSONDecodeError, OSError) as exc:
            logger.warning("Skipping unreadable flight search %s: %s", search_id, exc)
            continue
        data = record.get("search_data", {})
        searches.append(
            {
                "search_id": search_id,
                "route": f"{data.get('departure_id', '?')} -> {data.get('arrival_id', '?')}",
                "outbound_date": data.get("outbound_date"),
                "return_date": data.get("return_date"),
                "best_flights": len(record.get("best_flights", [])),
                "other_flights": len(record.get("other_flights", [])),
            }
        )
    return json.dumps(searches, indent=2)


@mcp.resource("flights://{search_id}")
def get_flight_search_details(search_id: str) -> str:
    """Read a saved flight search by ID."""
    return get_flight_details(search_id)


@mcp.prompt()
def travel_planning_prompt(
    departure: str,
    destination: str,
    departure_date: str,
    return_date: str = "",
    passengers: int = 1,
    budget: str = "",
    preferences: str = "",
) -> str:
    trip = f"from {departure} to {destination} on {departure_date}"
    if return_date:
        trip += f" and returning {return_date}"
    details = f" for {passengers} passenger(s)"
    if budget:
        details += f", with a budget of {budget}"
    if preferences:
        details += f"; preferences: {preferences}"
    return (
        f"Plan a trip {trip}{details}. Search flights first, compare available "
        "prices, stop counts, schedules, and price insights, then recommend "
        "suitable options. Clearly state when information is unavailable."
    )


@mcp.prompt()
def flight_comparison_promtp(search_id: str) -> str:
    return (
        f"Compare the saved flight search {search_id}. Use the flight details "
        "and price filter tools as appropriate. Summarize price, schedule, "
        "stops, and important trade-offs without inventing missing details."
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
