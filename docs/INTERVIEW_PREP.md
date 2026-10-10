# Travel Booking Agent — Interview Prep

A plain-language guide to understanding and explaining this project.
Read it once, then practice answering the questions in your own words.

## The project in one sentence

This is a Python travel-search application with a Flask web interface and
separate MCP servers for flight, hotel, event, and weather tools.

## A short interview introduction

> “I built a travel search application that brings flight, hotel, event, and
> weather searches into one small project. It has a Flask web interface for
> people and separate Model Context Protocol servers that an MCP-compatible AI
> client can call. SerpAPI provides the flight, hotel, and event search data,
> while Open-Meteo provides geocoding and weather. I focused on validating
> inputs, handling external service failures clearly, keeping secrets in
> environment variables, and testing the main flows without making live API
> calls.”

Only claim work you personally understand and can explain. This project
searches and displays information; it does not book travel or include an LLM.

## What happens during a search?

### From the website

1. A traveler submits a form in the browser.
2. JavaScript sends a JSON request to a Flask route in `demo_app.py`.
3. Flask checks the input: required fields, dates, passenger counts, and JSON
   shape.
4. The route calls SerpAPI or Open-Meteo using the shared HTTP session in
   `utils.py`. The session has a timeout and retries temporary GET failures.
5. Flask turns the provider response into a smaller result shape for the page.
6. JavaScript displays the results, escaping provider text before placing it
   in the page.

### From an MCP client

1. The MCP client launches the requested Python server as a separate process.
2. The client calls one of that server's tools using MCP over standard input
   and output (stdio).
3. The tool validates inputs and requests data from the external provider.
4. Search tools save results under the configured local data directory.
5. Other tools can read those results, filter them, or return them as an MCP
   resource.

The Flask web routes and MCP servers are two separate ways to access provider
searches. The Flask app makes provider requests directly; it does not call the
MCP servers.

## Main technologies

- **Python:** Server and validation logic.
- **Flask:** Web page and JSON API.
- **MCP / FastMCP:** Makes travel search functions available as tools and
  resources to compatible clients.
- **Requests:** Calls third-party HTTP APIs.
- **python-dotenv:** Loads local `.env` configuration for the web application.
- **SerpAPI:** Search results for flights, hotels, and events.
- **Open-Meteo:** Weather and location geocoding.
- **HTML, CSS, JavaScript:** Browser interface; no frontend framework.
- **SQLite:** A helper initializes a flight-search schema. The live search
  tools currently save their results as JSON files instead.

## Likely interview questions

### 1. What problem does this project solve?

It gives a traveler one interface to explore several trip-planning
information types. It also makes the same search capabilities available to
MCP-compatible clients.

### 2. What does “agent” mean here? Does the project use AI?

The project provides travel search tools that an AI client can use through
MCP. It does not contain its own language model or autonomous agent loop. An
MCP client decides whether to call a tool; the tool performs a specific
search and returns results.

### 3. What is MCP?

The Model Context Protocol is a standard way for an AI application to
discover and call tools provided by another program. Here, FastMCP exposes
Python functions as tools and saved-search data as resources. The servers
use stdio, so each MCP client launches its own server process; they are not
HTTP services listening on ports.

### 4. Why have both Flask and MCP?

They serve different users. Flask gives people a conventional browser
interface. MCP gives compatible AI clients a standard way to call the same
types of search operations. The implementations are separate, so they can be
used independently.

### 5. Why use external search providers?

The project does not own airline, hotel, event, or weather datasets.
SerpAPI and Open-Meteo provide that data through HTTP APIs. The trade-off is
that the application depends on provider availability, credentials where
required, rate limits, and provider response formats.

### 6. How are secrets managed?

The app reads `SERPAPI_KEY` from the environment. Developers can use a local
`.env` file, which is excluded from Git, while `.env.example` documents
variable names without containing real secrets. Keys should never be placed
in source code, test fixtures, or documentation.

> **Credential warning:** A key was present in the repository's earlier Git
> history. Removing it from the current files does not erase old commits.
> Previously exposed keys must be revoked and rotated.

### 7. How do you validate user input?

The API checks that request bodies are JSON objects, required strings are
present, dates follow `YYYY-MM-DD`, return/check-out dates follow the start
date, and passenger, rating, and price values are within supported ranges.
MCP search IDs are restricted to a safe filename pattern before opening a
saved result.

### 8. How do you handle failures?

Input errors are returned as clear client errors. Provider timeouts or HTTP
failures produce explicit failure responses instead of pretending a search
succeeded. The shared HTTP client has a bounded timeout and retries selected
temporary failures for GET requests. Logs record failure types without
printing API keys.

### 9. What do the tests cover?

The `unittest` suite uses mock provider responses. It checks Flask routes,
input validation, provider errors, MCP save-and-filter workflows, safe search
IDs, utility behavior, and SQLite schema creation. This lets the core flows
run without internet, credentials, or paid API calls. A live provider smoke
test is separate from the automated suite.

Run the suite with:

```sh
python -m unittest discover -s tests -v
```

### 10. Why mock provider APIs instead of calling the real APIs in tests?

Mocks make tests repeatable and fast. They also avoid consuming API quota,
needing secrets in CI, and failing because of an unrelated provider outage.
Live smoke tests are useful separately to confirm credentials and external
connectivity.

### 11. Why use JSON files for saved searches?

They keep the demo's save-and-filter MCP workflows simple, with no database
service to install. This is a conscious trade-off: JSON files are suitable
for a small local demo, but they do not provide concurrent-write guarantees,
efficient querying, or robust production data management.

### 12. Why is there SQLite code if searches use JSON?

The repository includes a helper that initializes a proposed SQLite schema.
The current search tools do not use it; they persist MCP search results as
JSON. A future cleanup could either connect the tools to SQLite or remove
the unused database helper to keep the architecture consistent.

### 13. What is a limitation you would improve next?

The app is intended for local demonstration. Before public deployment, I
would add authentication, CSRF protections, production server configuration,
stronger rate limiting, and a deliberate persistence strategy. I would also
keep provider credentials server-side and add provider contract tests.

### 14. Does this application book a flight or hotel?

No. It displays search information and may show provider links, but it does
not reserve inventory, collect payment, or guarantee the quoted price.

### 15. How would you add a new travel search provider?

I would define the expected input and output shape, validate the inputs,
implement a small provider client with timeouts and safe error handling,
normalize the response for the existing UI or MCP tool, then add mocked tests
for success, invalid data, and provider failure. I would keep credentials in
environment variables.

### 16. What would you change for production?

I would first choose a supported persistence layer and schema, add
authentication and CSRF/rate-limit controls for the web app, configure a
production WSGI server and HTTPS, centralize logs and secrets, and monitor
provider errors and quotas. I would also review data retention and privacy.

## Honest limitations to remember

- Results depend on third-party APIs and may be incomplete, stale, or
  unavailable.
- No actual reservations, checkout, payments, or user accounts are
  implemented.
- Flask has no authentication or CSRF protection and should stay on localhost
  unless those protections are added.
- MCP results use local JSON files; SQLite is initialized by a helper but is
  not currently the active search store.
- The weather server's thunderstorm likelihood is a rough heuristic, not an
  official alert.
- SerpAPI calls need a valid key; the automated tests deliberately mock those
  requests.

## Before an interview

1. Run the tests and be ready to explain what a mocked API response does.
2. Draw the web path and MCP path separately; explain that Flask does not
   call MCP.
3. Be clear about what MCP provides and what it does not provide.
4. Do not claim the app makes bookings, includes an LLM, or uses SQLite for
   current search persistence.
5. Practice the introduction above, then answer questions naturally rather
   than memorizing every sentence.
