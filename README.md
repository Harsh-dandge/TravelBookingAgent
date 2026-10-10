<div align="center">

# Travel Booking Agent

**One place to explore flights, stays, events, and weather for a trip.**

Built with Flask, Python, and the Model Context Protocol (MCP).

[Features](#what-you-can-do) · [Quick start](#quick-start) ·
[API](#web-api) · [MCP tools](#mcp-servers) ·
[Configuration](#configuration) · [Tests](#tests)

</div>

> **What this project does:** It searches and compares travel information.
> It does not make bookings, take payments, or guarantee third-party results.

## What you can do

| Search | Information |
| --- | --- |
| Flights | Search routes and dates, compare prices, schedules, and stops. |
| Hotels | Find stays and narrow results by price, rating, and amenities. |
| Events | Discover events by interest and location, then filter by date. |
| Weather | Check a five-day web forecast or use the MCP tool for a specific date. |

The browser app provides a simple search interface. The MCP servers expose
tools, resources, and prompts for MCP-compatible AI clients. The application
does **not** include an LLM or autonomous booking agent: the connected client
decides when to call MCP tools and how to present their results.

## How it works

```text
Browser
   │
   ▼
Flask web app ──────► SerpAPI ──► Flights, hotels, and events
       │
       └────────────► Open-Meteo ──► Geocoding and weather

MCP-compatible client ──stdio──► Flight / hotel / event / weather servers
                                      │
                                      └──► The same provider APIs
```

The Flask app makes provider requests directly. Each MCP server is a separate
stdio process; the MCP servers do not run on HTTP ports. MCP search results
are saved locally so tools can retrieve or filter them later.

## Quick start

### 1. Install

You need Python 3.10 or newer and pip.

**Windows PowerShell**

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

**macOS / Linux**

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

### 2. Add your SerpAPI key

Open `.env` and replace the placeholder value:

```dotenv
SERPAPI_KEY=your_serpapi_key_here
```

SerpAPI is needed for flight, hotel, and event searches. Weather uses
Open-Meteo and works without a key. Keep `.env` private; it is ignored by Git.

### 3. Run the app

```sh
python demo_app.py
```

Visit <http://127.0.0.1:5000>. The development server binds to localhost by
default. Use the form tabs to search, and check provider availability before
relying on any result.

## Web API

The web interface calls these JSON endpoints:

| Method and path | Required JSON fields | Purpose |
| --- | --- | --- |
| `POST /api/flights` | `departure`, `arrival`, `date`; optional `return_date`, `adults`, `children` | Search flight options. |
| `POST /api/hotels` | `location`, `check_in`, `check_out`; optional `guests` | Search hotel options. |
| `POST /api/events` | `event_type`, `location` | Find local events. |
| `POST /api/weather` | `location` | Get a five-day forecast. |
| `GET /api/health` | — | Check whether the web app is running. |

Dates use `YYYY-MM-DD`. For example, search flights with:

```sh
curl -X POST http://127.0.0.1:5000/api/flights \
  -H "Content-Type: application/json" \
  -d '{"departure":"PNQ","arrival":"JAI","date":"2030-11-01","return_date":"2030-11-05","adults":1,"children":0}'
```

Successful searches return JSON with `success: true` and a result list.
Validation failures return a clear message; provider failures return an
error response rather than fabricated example results.

## MCP servers

From the repository root, launch the server you want to connect:

```sh
python servers/flight_server/flight_server.py
python servers/hotel_server/hotel_server.py
python servers/event_server/event_server.py
python servers/weather_server/weather_server.py
```

Configure each command as a separate stdio server in your MCP client. The
flight, hotel, and event servers need `SERPAPI_KEY` in the process environment.
The weather server does not. Available tools include flight search and price
filtering, hotel search and filters, event search and date filtering, and
weather lookup. The servers also expose saved-search resources and planning
prompts.

## Configuration

Set variables in `.env` for the Flask app, or in the process environment when
launching an MCP server.

| Variable | Default | What it controls |
| --- | --- | --- |
| `SERPAPI_KEY` | — | SerpAPI authentication for flights, hotels, and events. |
| `REQUEST_TIMEOUT_SECONDS` | `15` | HTTP request timeout; must be positive. |
| `TRAVEL_DATA_DIR` | `.travel_data` | Root folder for saved MCP search results. |
| `FLASK_HOST` | `127.0.0.1` | Address the web app listens on. |
| `FLASK_PORT` | `5000` | Web app port. |
| `FLASK_DEBUG` | `false` | Flask debug mode; keep off outside local development. |
| `LOG_LEVEL` | `INFO` | Application log level. |

## Tests

The automated tests use mocked provider responses, so they do not need an API
key, internet access, paid requests, or a separate test framework.

```sh
python -m unittest discover -s tests -v
```

The suite covers API routes, validation, MCP search/filter flows, safe search
IDs, utility functions, and SQLite schema initialization.

## Project layout

```text
.
├── database/                 # SQLite schema initialization helper
├── docs/                     # Project and interview documentation
├── servers/
│   ├── event_server/         # Event search MCP server
│   ├── flight_server/        # Flight search MCP server
│   ├── hotel_server/         # Hotel search and filtering MCP server
│   └── weather_server/       # Weather and geocoding MCP server
├── static/                   # Browser JavaScript and styles
├── templates/                # Flask page template
├── tests/                    # Offline automated tests
├── demo_app.py               # Flask app and web API
├── utils.py                  # Shared configuration, HTTP, and validation
├── requirements.txt          # Python dependencies
└── .env.example              # Safe environment-variable template
```

## Important limitations

- This is a travel **search** demo, not a booking or payment system.
- Search results are supplied by third parties, can be incomplete or stale,
  and should be checked with the provider.
- The web app has no login, CSRF protection, or production deployment setup.
  Keep it on localhost unless you add and review those protections.
- The weather MCP tool's thunderstorm likelihood is a simple heuristic, not
  an official forecast or safety warning.

## License

MIT. See [LICENSE](LICENSE).

## Interview preparation

Preparing for an interview about this project? Start with
[Interview Prep](docs/INTERVIEW_PREP.md) for a short project pitch, architecture
walkthrough, likely questions, and honest limitations.

Manual account and deployment tasks are listed in
[Manual Follow-up](docs/MANUAL_FOLLOW_UP.md).
