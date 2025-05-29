import json
import unittest
import importlib.metadata
from pathlib import Path
from unittest.mock import patch, MagicMock
import tap_fullstory


class TestTapFullstorySchema(unittest.TestCase):
    def test_schema_file_structure(self):
        schema_path = Path(__file__).resolve().parent.parent.parent / "schemas" / "events.json"
        self.assertTrue(schema_path.exists(), "Schema file does not exist")

        with schema_path.open("r") as f:
            schema = json.load(f)

        self.assertIsInstance(schema, dict)
        self.assertIn("properties", schema)


class TestLibraryVersions(unittest.TestCase):
    def test_installed_versions(self):
        self.assertTrue(importlib.metadata.version("singer-python").startswith("6.1"))
        self.assertTrue(importlib.metadata.version("requests").startswith("2.32"))
        self.assertTrue(importlib.metadata.version("backoff").startswith("2.1"))
        self.assertTrue(importlib.metadata.version("pendulum").startswith("3.1"))
        self.assertTrue(importlib.metadata.version("ijson").startswith("3.4"))


class TestTapFullstoryMain(unittest.TestCase):
    @patch("singer.utils.parse_args", return_value=MagicMock(config={"api_key": "fake", "start_date": "2024-01-01"}, state={}))
    @patch("tap_fullstory.requests.get")
    @patch("tap_fullstory.singer.write_record")
    @patch("tap_fullstory.singer.write_schema")
    def test_main_with_schema(self, mock_write_schema, mock_write_record, mock_requests_get, mock_parse_args):
        schema_path = Path(__file__).parent.parent.parent / 'schemas' / 'events.json'

        with schema_path.open("r") as f:
            schema = json.load(f)

        mock_data = {
            "events": [
                {
                    "IndvId": 101,
                    "UserId": 202,
                    "SessionId": 303,
                    "PageId": 404,
                    "EventStart": "2024-05-20T10:00:00Z",
                    "EventType": "click",
                    "EventTargetText": "Submit",
                    "EventTargetSelectorTok": "#submit-btn",
                    "PageDuration": 5000,
                    "PageActiveDuration": 4800,
                    "PageUrl": "https://example.com",
                    "PageRefererUrl": "https://google.com",
                    "PageIp": "192.168.0.1",
                    "PageLatLong": "37.7749,-122.4194",
                    "PageAgent": "Mozilla/5.0",
                    "PageBrowser": "Chrome",
                    "PageDevice": "Desktop"
                }
            ]
        }

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_data
        mock_requests_get.return_value = mock_response

        tap_fullstory.main()

        mock_write_schema.assert_called_once()
        called_schema = mock_write_schema.call_args[0][1]
        self.assertEqual(set(called_schema["properties"].keys()), set(schema["properties"].keys()))
