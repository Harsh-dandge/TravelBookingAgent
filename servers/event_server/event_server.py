import json
import logging
import os
from datetime import date
from typing import Optional

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
    require_text,
)

load_dotenv()
logger = logging.getLogger(__name__)
mcp = FastMCP("event-server")
EVENT_DIR = get_data_dir("events")
DATE_FILTERS = {"today", "tomorrow", "week", "weekend", "next_week", "month", "next_month"}


def _read_search(search_id: str) -> dict:
    path = get_search_file(EVENT_DIR, search_id)
    with path.open(encoding="utf-8") as file:
        return json.load(file)


@mcp.tool()
def search_events(
    query: str,
    location: Optional[str] = None,
    date_filter: Optional[str] = None,
    language: str = "en",
    country: str = "us",
    max_results: int = 20,
) -> dict:
    """Search and save events matching a query and optional date filter."""
    try:
        query = require_text(query, "query")
        if location is not None:
            location = require_text(location, "location")
        if date_filter is not None and date_filter not in DATE_FILTERS:
            raise ValueError(f"date_filter must be one of: {', '.join(sorted(DATE_FILTERS))}")
        if isinstance(max_results, bool) or not isinstance(max_results, int) or not 1 <= max_results <= 100:
            raise ValueError("max_results must be between 1 and 100")
        if not language.isalpha() or not 2 <= len(language) <= 3:
            raise ValueError("language must be a 2- or 3-letter language code")
        if not country.isalpha() or len(country) != 2:
            raise ValueError("country must be a 2-letter country code")
        if not country.isascii():
            raise ValueError("country must use ASCII letters")
        if not language.isascii():
            raise ValueError("language must use ASCII letters")

        params = {
            "engine": "google_events",
            "api_key": get_api_key(),
            "q": f"{query} in {location}" if location else query,
            "hl": language.lower(),
            "gl": country.lower(),
        }
        if date_filter:
            params["htichips"] = f"date:{date_filter}"
        response = HTTP_SESSION.get(
            "https://serpapi.com/search", params=params, timeout=get_request_timeout()
        )
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, dict):
            raise ValueError("Event provider returned an invalid response")
        if data.get("error"):
            raise ValueError(f"Event provider error: {data['error']}")

        events = data.get("events_results") or []
        if not isinstance(events, list) or any(
            not isinstance(event, dict) for event in events
        ):
            raise ValueError("Event provider returned an invalid results list")
        search_id = make_search_id(
            query, location or "global", date.today().isoformat()
        )
        record = {
            "search_metadata": {
                "search_id": search_id,
                "query": query,
                "location": location,
                "date_filter": date_filter,
                "language": language.lower(),
                "country": country.lower(),
                "total_results": len(events[:max_results]),
            },
            "search_parameters": data.get("search_parameters") or {},
            "search_information": data.get("search_information") or {},
            "events_results": events[:max_results],
        }
        os.makedirs(EVENT_DIR, exist_ok=True)
        with get_search_file(EVENT_DIR, search_id).open("w", encoding="utf-8") as file:
            json.dump(record, file, indent=2)

        return {
            "search_id": search_id,
            "total_events": len(record["events_results"]),
            "query": query,
            "location": location,
            "filters_applied": {"date_filter": date_filter},
            "sample_events": [
                {
                    "title": event.get("title", "N/A"),
                    "date": (event.get("date") or {}).get("when", "N/A")
                    if isinstance(event.get("date"), dict)
                    else event.get("date", "N/A"),
                    "venue": (event.get("venue") or {}).get("name", "N/A")
                    if isinstance(event.get("venue"), dict)
                    else "N/A",
                }
                for event in record["events_results"][:3]
            ],
        }
    except requests.RequestException as exc:
        logger.warning("Event provider request failed (%s)", type(exc).__name__)
        return {"error": "Event provider request failed; please retry shortly"}
    except (ValueError, TypeError, AttributeError, OSError) as exc:
        logger.warning("Event search rejected or could not be saved: %s", exc)
        return {"error": str(exc)}


@mcp.tool()
def get_event_details(search_id: str) -> str:
    """Return a saved event search as JSON."""
    try:
        return json.dumps(_read_search(search_id), indent=2)
    except (ValueError, FileNotFoundError, json.JSONDecodeError, OSError) as exc:
        return f"Unable to read event search: {exc}"


@mcp.tool()
def filter_events_by_date(
    search_id: str,
    date_range: Optional[str] = None,
    specific_date: Optional[str] = None,
) -> str:
    """Filter saved events by a provider date phrase or exact ISO date."""
    if date_range and date_range not in DATE_FILTERS:
        return f"date_range must be one of: {', '.join(sorted(DATE_FILTERS))}"
    if specific_date:
        try:
            parse_iso_date(specific_date, "specific_date")
        except ValueError as exc:
            return str(exc)
    if date_range and specific_date:
        return "Use date_range or specific_date, not both"
    try:
        record = _read_search(search_id)
        filtered = []
        for event in record.get("events_results", []):
            date_info = event.get("date") or {}
            event_date = " ".join(
                str(value)
                for value in date_info.values()
                if isinstance(value, (str, int, float))
            ) if isinstance(date_info, dict) else str(date_info)
            if date_range and date_range.casefold() in event_date.casefold():
                filtered.append(event)
            elif specific_date and specific_date in event_date:
                filtered.append(event)
            elif not date_range and not specific_date:
                filtered.append(event)
        return json.dumps(
            {
                "search_id": search_id,
                "filters_applied": {
                    "date_range": date_range,
                    "specific_date": specific_date,
                },
                "filtered_events": filtered,
                "total_filtered": len(filtered),
            },
            indent=2,
        )
    except (ValueError, FileNotFoundError, json.JSONDecodeError, OSError) as exc:
        return f"Unable to filter event search: {exc}"


@mcp.resource("events://searches")
def list_event_searches() -> str:
    """List saved event searches."""
    if not os.path.isdir(EVENT_DIR):
        return "No event searches found."
    searches = []
    for filename in sorted(os.listdir(EVENT_DIR)):
        if not filename.endswith(".json"):
            continue
        try:
            searches.append(_read_search(filename[:-5]).get("search_metadata", {}))
        except (ValueError, FileNotFoundError, json.JSONDecodeError, OSError) as exc:
            logger.warning("Skipping unreadable event search %s: %s", filename, exc)
    return json.dumps(searches, indent=2)


@mcp.resource("events://{search_id}")
def get_event_search_details(search_id: str) -> str:
    """Read a saved event search resource."""
    return get_event_details(search_id)


@mcp.prompt()
def event_discovery_prompt(
    location: str,
    interests: str = "",
    date_preference: str = "",
    event_type: str = "",
    budget: str = "",
) -> str:
    return (
        f"Find {event_type or 'events'} in {location}. "
        f"Interests: {interests or 'any'}. "
        f"Date preference: {date_preference or 'any'}. "
        f"Budget: {budget or 'not specified'}. "
        "Search first, then summarize dates, venues, ticket information, "
        "and practical travel considerations. Do not invent missing details."
    )


@mcp.prompt()
def event_comparison_prompt(search_id: str) -> str:
    return (
        f"Compare the events in saved search {search_id}. Retrieve the saved "
        "search and summarize dates, venues, ticket information, and any "
        "missing details that a traveler should verify."
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
