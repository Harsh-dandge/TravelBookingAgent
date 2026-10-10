# Travel Booking Agent

A Python travel-planning project with a Flask web interface and four
Model Context Protocol (MCP) servers. Search flights, hotels, and events
through SerpAPI, or retrieve weather forecasts from Open-Meteo.

Search results are informational. The application does not book or purchase
travel products.

## Features

- Flight search with passenger, cabin, route, and date validation.
- Hotel search with price, rating, and amenity filters.
- Event discovery with date filtering.
- Weather lookup for forecasts up to 15 days ahead and historical dates.
- Web search forms backed by live provider APIs, with readable errors.
- MCP tools, resources, and planning prompts for compatible MCP clients.
- Bounded HTTP timeouts, retries for transient GET failures, and local result
  storage for subsequent filtering.

SerpAPI requires a user-provided key for flight, hotel, and event searches.
Open-Meteo weather and geocoding do not require an API key.

## Architecture

```text
Browser ──> Flask REST API ──> SerpAPI (flights, hotels, events)
                         └──> Open-Meteo (weather, geocoding)

MCP client ──> flight / hotel / event / weather servers (stdio)
```

The web app calls provider APIs directly. MCP servers are separate
stdio-based integrations; they do not listen on ports. Each server can be
configured as its own MCP client process.

## Tech stack

- Python 3.10+
- Flask
- MCP Python SDK (FastMCP)
- Requests and python-dotenv
- SerpAPI
- Open-Meteo
- HTML, CSS, and vanilla JavaScript

## Setup

1. Create and activate a virtual environment:

   **Windows PowerShell**

   ```powershell
   py -3 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **macOS / Linux**

   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```sh
   python -m pip install -r requirements.txt
   ```

3. Create a local environment file and add your SerpAPI key:

   ```powershell
   Copy-Item .env.example .env
   ```

   Edit `.env` and set `SERPAPI_KEY`. Do not commit this file.

4. Start the web interface:

   ```sh
   python demo_app.py
   ```

   Open <http://127.0.0.1:5000>. Weather search works without a SerpAPI key.
   Searches involving SerpAPI return a configuration error until a key is set.

## Usage

Use the browser forms to search. The REST API can also be called directly:

```sh
curl -X POST http://127.0.0.1:5000/api/flights \
  -H "Content-Type: application/json" \
  -d '{"departure":"PNQ","arrival":"JAI","date":"2026-11-01","return_date":"2026-11-05","adults":1,"children":0}'
```

```sh
curl -X POST http://127.0.0.1:5000/api/hotels \
  -H "Content-Type: application/json" \
  -d '{"location":"Jaipur","check_in":"2026-11-01","check_out":"2026-11-04","guests":2}'
```

```sh
curl -X POST http://127.0.0.1:5000/api/events \
  -H "Content-Type: application/json" \
  -d '{"event_type":"Concerts","location":"Jaipur"}'
```

```sh
curl -X POST http://127.0.0.1:5000/api/weather \
  -H "Content-Type: application/json" \
  -d '{"location":"Jaipur"}'
```

Dates must be in `YYYY-MM-DD` format. Flight routes use airport or supported
city codes. Search results can change and should be verified with the booking
provider before making travel decisions.

### MCP servers

Run a server as a stdio process from the repository root:

```sh
python servers/flight_server/flight_server.py
python servers/hotel_server/hotel_server.py
python servers/event_server/event_server.py
python servers/weather_server/weather_server.py
```

Configure one process per server in your MCP client. Provide `SERPAPI_KEY`
through that client's environment for the flight, hotel, and event servers.
The weather server uses Open-Meteo and needs no key. See the server source for
available MCP tools, resources, and prompts.

## Environment variables

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `SERPAPI_KEY` | For SerpAPI searches | — | SerpAPI account key; never commit it. |
| `REQUEST_TIMEOUT_SECONDS` | No | `15` | Positive HTTP timeout in seconds. |
| `TRAVEL_DATA_DIR` | No | `.travel_data` | Directory for saved MCP search results. |
| `FLASK_HOST` | No | `127.0.0.1` | Web server bind address. |
| `FLASK_PORT` | No | `5000` | Web server port. |
| `FLASK_DEBUG` | No | `false` | Enable Flask debug mode only for local development. |
| `LOG_LEVEL` | No | `INFO` | Python logging level. |

## Tests

The automated suite uses the standard library and mocked provider responses;
it does not make paid or external API requests.

```sh
python -m unittest discover -s tests -v
```

Live provider availability and credentials are not required to run the tests.

## Project structure

```text
.
├── database/                 # SQLite schema initialization
├── servers/
│   ├── event_server/         # Event MCP tools
│   ├── flight_server/        # Flight MCP tools
│   ├── hotel_server/         # Hotel MCP tools and filters
│   └── weather_server/       # Weather and geocoding MCP tools
├── static/                   # Web UI styles and JavaScript
├── templates/                # Flask HTML template
├── tests/                    # Offline unit and integration tests
├── demo_app.py               # Flask web application
├── utils.py                  # Shared validation, HTTP, and storage helpers
├── requirements.txt
└── .env.example
```

## Security and limitations

- Keep API keys in environment variables or a local `.env` file.
- Search inputs and saved-search IDs are validated; HTTP calls use timeouts
  and retry only transient GET failures.
- The development web app has no authentication or CSRF protection. Keep it
  bound to localhost; do not expose it directly to the public internet.
- Flight, hotel, event, and weather content comes from third parties and may
  be incomplete or stale. The thunderstorm estimate is a rough heuristic, not
  an official warning.

## License

This project is distributed under the MIT License. See [LICENSE](LICENSE).
