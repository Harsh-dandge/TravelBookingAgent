import json
import os
import tempfile
import unittest
from datetime import date, timedelta
from unittest.mock import patch

from servers.event_server import event_server
from servers.flight_server import flight_server
from servers.hotel_server import hotel_server
from servers.weather_server import weather_server


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


class McpServerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.key_patch = patch.dict(os.environ, {"SERPAPI_KEY": "test-key"})
        self.key_patch.start()

    def tearDown(self):
        self.key_patch.stop()
        self.temp_dir.cleanup()

    def future_stay(self):
        start = date.today() + timedelta(days=10)
        end = start + timedelta(days=2)
        return start.isoformat(), end.isoformat()

    def test_flight_search_saves_and_filters_best_and_other_flights(self):
        record = {
            "best_flights": [{"price": 100}, {"price": 250}],
            "other_flights": [{"price": 180}],
            "price_insights": {"lowest_price": 100},
        }
        outbound, returned = self.future_stay()
        with patch.object(flight_server, "FLIGHT_DIR", self.temp_dir.name), patch(
            "servers.flight_server.flight_server.HTTP_SESSION.get",
            return_value=FakeResponse(record),
        ):
            search = flight_server.search_flight(
                "PNQ", "JAI", outbound, return_date=returned
            )
            filtered = json.loads(
                flight_server.filter_flights_by_price(search["search_id"], 150, 250)
            )
        self.assertEqual(search["best_flights_found"], 2)
        self.assertEqual(len(filtered["filtered_best_flights"]), 1)
        self.assertEqual(len(filtered["filtered_other_flights"]), 1)

    def test_flight_rejects_invalid_round_trip_before_request(self):
        with patch("servers.flight_server.flight_server.HTTP_SESSION.get") as request:
            result = flight_server.search_flight("PNQ", "JAI", "2030-01-01")
        self.assertIn("return_date is required", result["error"])
        request.assert_not_called()

    def test_hotel_search_and_price_rating_amenity_filters(self):
        check_in, check_out = self.future_stay()
        properties = [
            {
                "name": "Value Stay",
                "rate_per_night": {"extracted_lowest": 100},
                "overall_rating": 4.5,
                "amenities": ["Pool", "Free Wi-Fi"],
            },
            {
                "name": "Luxury Stay",
                "rate_per_night": {"extracted_lowest": 300},
                "overall_rating": 4.9,
                "amenities": ["Spa"],
            },
        ]
        with patch.object(hotel_server, "HOTEL_DIR", self.temp_dir.name), patch(
            "servers.hotel_server.hotel_server.HTTP_SESSION.get",
            return_value=FakeResponse({"properties": properties}),
        ):
            result = hotel_server.search_hotel("Hotels in Jaipur", check_in, check_out)
            cheap = json.loads(
                hotel_server.filter_hotel_by_price(result["search_id"], max_price=150)
            )
            amenities = json.loads(
                hotel_server.filter_hotels_by_amenities(
                    result["search_id"], ["pool", "Free Wi-Fi"]
                )
            )
            rated = json.loads(
                hotel_server.filter_hotels_by_rating(result["search_id"], 4.8)
            )
        self.assertEqual(cheap["total_filtered"], 1)
        self.assertEqual(amenities["total_filtered"], 1)
        self.assertEqual(rated["total_filtered"], 1)

    def test_search_id_path_traversal_is_rejected(self):
        with patch.object(hotel_server, "HOTEL_DIR", self.temp_dir.name):
            result = hotel_server.filter_hotel_by_price("..\\..\\secrets", 0, 10)
        self.assertIn("Invalid search ID", result)

    def test_event_search_saves_and_filters_by_date(self):
        check_in, _ = self.future_stay()
        event_data = {
            "events_results": [
                {"title": "Travel fair", "date": {"when": f"Oct {check_in}"}},
                {"title": "Music night", "date": {"when": "Next month"}},
            ]
        }
        with patch.object(event_server, "EVENT_DIR", self.temp_dir.name), patch(
            "servers.event_server.event_server.HTTP_SESSION.get",
            return_value=FakeResponse(event_data),
        ):
            result = event_server.search_events("events", "Jaipur")
            filtered = json.loads(
                event_server.filter_events_by_date(
                    result["search_id"], specific_date=check_in
                )
            )
        self.assertEqual(result["total_events"], 2)
        self.assertEqual(filtered["total_filtered"], 1)

    def test_weather_uses_forecast_for_today_and_saves_result(self):
        payloads = [
            FakeResponse(
                {
                    "results": [
                        {
                            "name": "Jaipur",
                            "latitude": 26.9,
                            "longitude": 75.8,
                            "country": "India",
                        }
                    ]
                }
            ),
            FakeResponse(
                {
                    "hourly": {
                        "rain": [0, 1],
                        "cloudcover": [50, 60],
                        "relativehumidity_2m": [40, 60],
                        "windspeed_10m": [10, 15],
                    }
                }
            ),
        ]
        with patch.object(weather_server, "WEATHER_DIR", self.temp_dir.name), patch(
            "servers.weather_server.weather_server.HTTP_SESSION.get",
            side_effect=payloads,
        ) as request:
            result = weather_server.get_weather("Jaipur", date.today().isoformat())
        self.assertEqual(result["rain_probability_percent"], 50.0)
        self.assertEqual(len(request.call_args_list), 2)
        self.assertIn("/v1/forecast", request.call_args_list[1].args[0])


if __name__ == "__main__":
    unittest.main()
