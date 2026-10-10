import json
import logging
import math
import os
from datetime import date
from typing import List, Optional

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
    validate_date_range,
)

load_dotenv()
logger = logging.getLogger(__name__)
mcp = FastMCP("hotel-server")
HOTEL_DIR = get_data_dir("hotels")


def _read_search(search_id: str) -> dict:
    path = get_search_file(HOTEL_DIR, search_id)
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def _filter_properties(search_id: str, predicate, filters: dict) -> str:
    try:
        properties = _read_search(search_id).get("properties", [])
        filtered = [hotel for hotel in properties if predicate(hotel)]
        return json.dumps(
            {
                "search_id": search_id,
                "filters_applied": filters,
                "filtered_properties": filtered,
                "total_filtered": len(filtered),
            },
            indent=2,
        )
    except (ValueError, FileNotFoundError, json.JSONDecodeError, OSError) as exc:
        return f"Unable to filter hotel search: {exc}"


@mcp.tool()
def search_hotel(
    query: str,
    check_in_date: str,
    check_out_date: str,
    engine: str = "google_hotels",
    currency: str = "INR",
    language: str = "en",
    adults: int = 2,
    sort_by: int = 8,
    hotel_class: int = 2,
    max_results: int = 20,
) -> dict:
    """Search hotels and save options for filtering and property lookups."""
    try:
        if not isinstance(query, str) or not query.strip() or len(query.strip()) > 200:
            raise ValueError("query is required and must be 200 characters or fewer")
        check_in = parse_iso_date(check_in_date, "check_in_date")
        check_out = parse_iso_date(check_out_date, "check_out_date")
        validate_date_range(check_in, check_out, "check_in_date", "check_out_date")
        if check_in < date.today():
            raise ValueError("check_in_date cannot be in the past")
        if isinstance(adults, bool) or not isinstance(adults, int) or not 1 <= adults <= 30:
            raise ValueError("adults must be between 1 and 30")
        if sort_by not in (3, 8, 13):
            raise ValueError("sort_by must be 3 (price), 8 (rating), or 13 (views)")
        if hotel_class not in (2, 3, 4, 5):
            raise ValueError("hotel_class must be between 2 and 5")
        if isinstance(max_results, bool) or not isinstance(max_results, int) or not 1 <= max_results <= 100:
            raise ValueError("max_results must be between 1 and 100")
        if not isinstance(currency, str) or not currency.isascii() or not currency.isalpha() or len(currency) != 3:
            raise ValueError("currency must be a 3-letter currency code")
        if not isinstance(language, str) or not language.isascii() or not language.isalpha() or not 2 <= len(language) <= 3:
            raise ValueError("language must be a 2- or 3-letter language code")
        if engine != "google_hotels":
            raise ValueError("engine must be google_hotels")

        params = {
            "engine": engine,
            "q": query.strip(),
            "check_in_date": check_in.isoformat(),
            "check_out_date": check_out.isoformat(),
            "currency": currency.upper(),
            "hl": language.lower(),
            "adults": adults,
            "sort_by": sort_by,
            "hotel_class": hotel_class,
            "api_key": get_api_key(),
        }
        response = HTTP_SESSION.get(
            "https://serpapi.com/search", params=params, timeout=get_request_timeout()
        )
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, dict):
            raise ValueError("Hotel provider returned an invalid response")
        if data.get("error"):
            raise ValueError(f"Hotel provider error: {data['error']}")

        properties = data.get("properties") or []
        if not isinstance(properties, list) or any(
            not isinstance(hotel, dict) for hotel in properties
        ):
            raise ValueError("Hotel provider returned an invalid properties list")
        search_id = make_search_id(
            check_in.isoformat(),
            check_out.isoformat(),
            query,
            date.today().isoformat(),
        )
        record = {
            "search_id": search_id,
            "search_metadata": {
                "search_id": search_id,
                "query": query.strip(),
                "check_in_date": check_in.isoformat(),
                "check_out_date": check_out.isoformat(),
                "adults": adults,
                "hotel_class": hotel_class,
                "currency": currency.upper(),
            },
            "search_parameters": {
                "q": query.strip(),
                "check_in_date": check_in.isoformat(),
                "check_out_date": check_out.isoformat(),
                "adults": adults,
            },
            "search_information": data.get("search_information") or {},
            "properties": properties[:max_results],
        }
        os.makedirs(HOTEL_DIR, exist_ok=True)
        with get_search_file(HOTEL_DIR, search_id).open("w", encoding="utf-8") as file:
            json.dump(record, file, indent=2)

        return {
            "search_id": search_id,
            "query": query.strip(),
            "check_in_date": check_in.isoformat(),
            "check_out_date": check_out.isoformat(),
            "total_results": len(properties),
            "properties": record["properties"],
        }
    except requests.RequestException as exc:
        logger.warning("Hotel provider request failed (%s)", type(exc).__name__)
        return {"error": "Hotel provider request failed; please retry shortly"}
    except (ValueError, TypeError, AttributeError, OSError) as exc:
        logger.warning("Hotel search rejected or could not be saved: %s", exc)
        return {"error": str(exc)}


@mcp.tool()
def filter_hotel_by_price(
    search_id: str,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
) -> str:
    """Filter hotels by inclusive nightly price bounds."""
    for name, price in (("min_price", min_price), ("max_price", max_price)):
        if price is not None and (
            isinstance(price, bool)
            or not isinstance(price, (int, float))
            or not math.isfinite(price)
            or price < 0
        ):
            return f"{name} must be a finite non-negative number"
    if min_price is not None and max_price is not None and min_price > max_price:
        return "min_price cannot exceed max_price"

    def matches(hotel: dict) -> bool:
        rate = hotel.get("rate_per_night") or {}
        price = rate.get("extracted_lowest")
        if not isinstance(price, (int, float)):
            return False
        return (min_price is None or price >= min_price) and (
            max_price is None or price <= max_price
        )

    return _filter_properties(
        search_id, matches, {"min_price": min_price, "max_price": max_price}
    )


@mcp.tool()
def filter_hotels_by_rating(search_id: str, min_rating: float = 3.0) -> str:
    """Filter hotels by minimum overall guest rating."""
    if (
        isinstance(min_rating, bool)
        or not isinstance(min_rating, (int, float))
        or not 0 <= min_rating <= 5
    ):
        return "min_rating must be between 0 and 5"
    return _filter_properties(
        search_id,
        lambda hotel: isinstance(hotel.get("overall_rating"), (int, float))
        and hotel["overall_rating"] >= min_rating,
        {"min_rating": min_rating},
    )


@mcp.tool()
def filter_hotels_by_amenities(search_id: str, required_amenities: List[str]) -> str:
    """Filter hotels containing every requested amenity (case-insensitive)."""
    if not isinstance(required_amenities, list) or any(
        not isinstance(amenity, str) or not amenity.strip()
        for amenity in required_amenities
    ):
        return "required_amenities must be a list of non-empty strings"
    required = {amenity.strip().casefold() for amenity in required_amenities}

    def matches(hotel: dict) -> bool:
        amenities = hotel.get("amenities") or []
        return required.issubset(
            {amenity.casefold() for amenity in amenities if isinstance(amenity, str)}
        )

    return _filter_properties(
        search_id, matches, {"required_amenities": sorted(required)}
    )


@mcp.tool()
def get_property_details(
    property_token: str,
    search_id: str,
    currency: str = "INR",
    country: str = "in",
    language: str = "en",
) -> str:
    """Fetch detailed information for a property from a saved hotel search."""
    try:
        if not isinstance(property_token, str) or not property_token or len(property_token) > 500:
            raise ValueError("A valid property_token is required")
        if not isinstance(currency, str) or not currency.isascii() or not currency.isalpha() or len(currency) != 3:
            raise ValueError("currency must be a 3-letter currency code")
        if not isinstance(country, str) or not country.isascii() or not country.isalpha() or len(country) != 2:
            raise ValueError("country must be a 2-letter country code")
        if not isinstance(language, str) or not language.isascii() or not language.isalpha() or not 2 <= len(language) <= 3:
            raise ValueError("language must be a 2- or 3-letter language code")
        record = _read_search(search_id)
        if not any(
            hotel.get("property_token") == property_token
            for hotel in record.get("properties", [])
        ):
            raise ValueError("property_token was not found in this hotel search")
        params = {
            "engine": "google_hotels",
            "api_key": get_api_key(),
            "property_token": property_token,
            **record.get("search_parameters", {}),
            "currency": currency.upper(),
            "gl": country.lower(),
            "hl": language.lower(),
        }
        response = HTTP_SESSION.get(
            "https://serpapi.com/search", params=params, timeout=get_request_timeout()
        )
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)
    except requests.RequestException as exc:
        logger.warning("Hotel property request failed (%s)", type(exc).__name__)
        return "Hotel property request failed; please retry shortly"
    except (ValueError, TypeError, FileNotFoundError, json.JSONDecodeError, OSError) as exc:
        return f"Unable to read hotel property details: {exc}"


@mcp.resource("hotel://searches")
def list_hotel_searches() -> str:
    """List saved hotel searches."""
    if not os.path.isdir(HOTEL_DIR):
        return "No hotel searches found."
    records = []
    for filename in sorted(os.listdir(HOTEL_DIR)):
        if not filename.endswith(".json"):
            continue
        search_id = filename[:-5]
        try:
            record = _read_search(search_id)
        except (ValueError, FileNotFoundError, json.JSONDecodeError, OSError) as exc:
            logger.warning("Skipping unreadable hotel search %s: %s", search_id, exc)
            continue
        records.append(record.get("search_metadata", {}))
    return json.dumps(records, indent=2)


@mcp.resource("hotel://{search_id}")
def get_hotel_search_details(search_id: str) -> str:
    """Read the saved hotel search JSON."""
    try:
        return json.dumps(_read_search(search_id), indent=2)
    except (ValueError, FileNotFoundError, json.JSONDecodeError, OSError) as exc:
        return f"Unable to read hotel search: {exc}"


@mcp.prompt()
def hotel_planning_prompt(
    destination: str,
    check_in_date: str,
    check_out_date: str,
    guests: int = 2,
    budget: str = "",
    preferences: str = "",
    hotel_type: str = "hotels",
) -> str:
    details = f"Plan {hotel_type} in {destination} for {guests} guest(s), "
    details += f"from {check_in_date} to {check_out_date}."
    if budget:
        details += f" Budget: {budget}."
    if preferences:
        details += f" Preferences: {preferences}."
    return (
        details
        + " Search, compare nightly price, ratings, amenities, and cancellation "
        "details when available. Clearly identify missing information."
    )


@mcp.prompt()
def hotel_comparison_prompt(search_id: str) -> str:
    return (
        f"Compare the hotels in saved search {search_id}. Use the available "
        "price, rating, amenity, and property-detail tools. Distinguish known "
        "facts from unavailable booking details."
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
