import math
import os
import re
from datetime import date, datetime
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def get_api_key() -> str:
    api_key = os.getenv("SERPAPI_KEY", "").strip()
    if not api_key or api_key.casefold() == "your_serpapi_key_here":
        raise ValueError("SERPAPI_KEY is not configured")
    return api_key


def get_request_timeout() -> float:
    raw_timeout = os.getenv("REQUEST_TIMEOUT_SECONDS", "15")
    try:
        timeout = float(raw_timeout)
    except ValueError as exc:
        raise ValueError("REQUEST_TIMEOUT_SECONDS must be a positive number") from exc
    if not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("REQUEST_TIMEOUT_SECONDS must be a positive number")
    return timeout


def create_http_session() -> requests.Session:
    retry = Retry(
        total=2,
        connect=2,
        read=2,
        status=2,
        backoff_factor=0.3,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET"}),
        respect_retry_after_header=True,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def require_text(value: object, name: str, max_length: int = 200) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{name} is required")
    value = value.strip()
    if not value:
        raise ValueError(f"{name} is required")
    if len(value) > max_length:
        raise ValueError(f"{name} must be {max_length} characters or fewer")
    return value


def parse_iso_date(value: object, name: str) -> date:
    value = require_text(value, name, max_length=10)
    try:
        parsed = datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError(f"{name} must use YYYY-MM-DD format") from exc
    if parsed.isoformat() != value:
        raise ValueError(f"{name} must use YYYY-MM-DD format")
    return parsed


def make_search_id(*parts: object) -> str:
    raw_id = "_".join(str(part) for part in parts if part is not None)
    slug = re.sub(r"[^A-Za-z0-9_-]+", "_", raw_id).strip("_")
    if not slug:
        raise ValueError("Unable to create a valid search ID")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return f"{slug[:150]}_{timestamp}"


def get_search_file(directory: str, search_id: str) -> Path:
    if not isinstance(search_id, str) or not re.fullmatch(
        r"[A-Za-z0-9][A-Za-z0-9_-]{0,179}", search_id
    ):
        raise ValueError("Invalid search ID")
    root = Path(directory).resolve()
    path = (root / f"{search_id}.json").resolve()
    if path.parent != root:
        raise ValueError("Invalid search ID")
    return path


def get_data_dir(service: str) -> str:
    if not re.fullmatch(r"[a-z][a-z0-9_-]{0,39}", service):
        raise ValueError("Invalid data service")
    project_root = Path(__file__).resolve().parent
    data_root = Path(os.getenv("TRAVEL_DATA_DIR", project_root / ".travel_data"))
    if not data_root.is_absolute():
        data_root = project_root / data_root
    return str(data_root / service)


def validate_date_range(start: date, end: date, start_name: str, end_name: str) -> None:
    if end <= start:
        raise ValueError(f"{end_name} must be after {start_name}")


HTTP_SESSION = create_http_session()
