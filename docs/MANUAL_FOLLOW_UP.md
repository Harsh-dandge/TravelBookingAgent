# Manual Follow-up Checklist

These items need your own account access or decisions. They are not required
to use the local demo.

## Do first: rotate the SerpAPI credential

A SerpAPI key was included in the repository's older Git history. Removing it
from the current files does not remove it from old commits.

1. Revoke the exposed key in your SerpAPI account.
2. Create a replacement key.
3. Put the new key in your local `.env` as `SERPAPI_KEY=...`.
4. Do not paste the key into GitHub, source files, screenshots, or chat.

## Update the GitHub repository profile

In the repository's GitHub **About** settings, update the description and
topics:

- **Suggested description:** Travel search agent with a Flask web UI and MCP
  tools for flights, hotels, events, and weather.
- **Suggested topics:** `travel`, `travel-planning`,
  `model-context-protocol`, `flask`, `python`, `serpapi`, `open-meteo`.

## Before sharing publicly or deploying

- Keep the local web app bound to localhost unless you add authentication,
  CSRF protection, and appropriate rate limits.
- Verify search results and booking details with the provider; this project
  searches but does not make reservations or take payments.
- If you deploy the app, use a production WSGI server and HTTPS, configure
  secrets through the hosting provider, and review data storage and logging.
