import os
import unittest
from datetime import date, timedelta
from unittest.mock import patch

import requests

from demo_app import app


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


class WebAppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.key_patch = patch.dict(os.environ, {"SERPAPI_KEY": "test-key"})
        self.key_patch.start()

    def tearDown(self):
        self.key_patch.stop()

    def future_dates(self):
        start = date.today() + timedelta(days=10)
        end = start + timedelta(days=3)
        return start.isoformat(), end.isoformat()

    def test_health_and_home(self):
        self.assertEqual(self.client.get("/api/health").json["status"], "running")
        self.assertEqual(self.client.get("/").status_code, 200)

    def test_flight_search_formats_and_limits_provider_results(self):
        outbound, returned = self.future_dates()
        flights = [
            {
                "price": 120,
                "total_duration": 90,
                "flights": [
                    {
                        "airline": "Sample Air",
                        "departure_airport": {"time": "09:00"},
                        "arrival_airport": {"time": "10:30"},
                    }
                ],
            }
        ]
        with patch(
            "demo_app.HTTP_SESSION.get",
            return_value=FakeResponse({"best_flights": flights, "other_flights": []}),
        ) as request:
            response = self.client.post(
                "/api/flights",
                json={
                    "departure": "pnq",
                    "arrival": "jai",
                    "date": outbound,
                    "return_date": returned,
                    "adults": 1,
                    "children": 0,
                },
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["flights"][0]["airline"], "Sample Air")
        self.assertEqual(response.json["flights"][0]["stops"], 0)
        self.assertEqual(request.call_args.kwargs["params"]["departure_id"], "PNQ")

    def test_invalid_flight_dates_are_rejected_without_provider_call(self):
        with patch("demo_app.HTTP_SESSION.get") as request:
            response = self.client.post(
                "/api/flights",
                json={
                    "departure": "PNQ",
                    "arrival": "JAI",
                    "date": "not-a-date",
                },
            )
        self.assertEqual(response.status_code, 400)
        self.assertIn("YYYY-MM-DD", response.json["error"])
        request.assert_not_called()

    def test_hotel_search_formats_provider_results(self):
        check_in, check_out = self.future_dates()
        hotel = {
            "title": "Sample Hotel",
            "rate_per_night": {"lowest": "INR 5000"},
            "overall_rating": 4.6,
            "reviews": 125,
            "address": "Jaipur",
        }
        with patch(
            "demo_app.HTTP_SESSION.get",
            return_value=FakeResponse({"properties": [hotel]}),
        ):
            response = self.client.post(
                "/api/hotels",
                json={
                    "location": "Jaipur",
                    "check_in": check_in,
                    "check_out": check_out,
                    "guests": 2,
                },
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["hotels"][0]["name"], "Sample Hotel")

    def test_event_search_uses_provider_event_shape(self):
        with patch(
            "demo_app.HTTP_SESSION.get",
            return_value=FakeResponse(
                {
                    "events_results": [
                        {
                            "title": "Sample Concert",
                            "date": {"when": "Tomorrow"},
                            "venue": {"name": "Town Hall"},
                            "link": "https://example.com/event",
                        }
                    ]
                }
            ),
        ):
            response = self.client.post(
                "/api/events",
                json={"event_type": "Concerts", "location": "Jaipur"},
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["events"][0]["location"], "Town Hall")

    def test_provider_timeout_returns_gateway_error(self):
        with patch(
            "demo_app.HTTP_SESSION.get", side_effect=requests.Timeout()
        ):
            response = self.client.post(
                "/api/events",
                json={"event_type": "Concerts", "location": "Jaipur"},
            )
        self.assertEqual(response.status_code, 502)
        self.assertIn("retry", response.json["error"])

    def test_missing_serpapi_key_is_reported_as_configuration_error(self):
        with patch.dict(os.environ, {"SERPAPI_KEY": ""}):
            start, end = self.future_dates()
            response = self.client.post(
                "/api/hotels",
                json={
                    "location": "Jaipur",
                    "check_in": start,
                    "check_out": end,
                    "guests": 2,
                },
            )
        self.assertEqual(response.status_code, 503)
        self.assertIn("SERPAPI_KEY", response.json["error"])

    def test_weather_returns_five_day_data(self):
        geocoding = FakeResponse(
            {"results": [{"name": "Jaipur", "latitude": 26.9, "longitude": 75.8}]}
        )
        weather = FakeResponse(
            {
                "daily": {
                    "time": ["2026-10-11"],
                    "temperature_2m_max": [32],
                    "temperature_2m_min": [20],
                    "precipitation_sum": [0],
                    "weather_code": [0],
                }
            }
        )
        with patch("demo_app.HTTP_SESSION.get", side_effect=[geocoding, weather]):
            response = self.client.post("/api/weather", json={"location": "Jaipur"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["weather"][0]["temp_max"], 32)

    def test_invalid_json_body_is_rejected(self):
        response = self.client.post(
            "/api/events", data="[]", content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("JSON object", response.json["error"])


if __name__ == "__main__":
    unittest.main()
