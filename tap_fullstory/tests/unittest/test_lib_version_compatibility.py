import json
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
import datetime
import tap_fullstory


class FakeDateTime(datetime.datetime):
    @classmethod
    def utcfromtimestamp(cls, ts):
        return datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc)


class TestTapFullstoryMain(unittest.TestCase):
    @patch("singer.utils.parse_args", return_value=MagicMock(config={"api_key": "fake", "start_date": "2024-01-01"}, state={}))
    @patch("tap_fullstory.request")  # patch request() in __init__.py
    @patch("tap_fullstory.singer.write_record")
    @patch("tap_fullstory.singer.write_schema")
    @patch("tap_fullstory.datetime", wraps=datetime)
    def test_main_with_schema(self, mock_datetime_module, mock_write_schema, mock_write_record, mock_request, mock_parse_args):
        mock_datetime_module.datetime = FakeDateTime

        # Load expected schema
        schema_path = Path(__file__).parent.parent.parent / 'schemas' / 'events.json'
        with schema_path.open("r") as f:
            schema = json.load(f)

        # Setup mocked API responses
        mock_request.side_effect = [
            {
                "exports": [
                    {"Id": "mock_file_id", "Stop": 1716163200}
                ]
            },
            [
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
        ]

        # Run the tap
        tap_fullstory.main()

        # Assert schema was written
        mock_write_schema.assert_called_once()
        written_schema = mock_write_schema.call_args[0][1]
        self.assertEqual(set(written_schema["properties"].keys()), set(schema["properties"].keys()))

        # Assert record was written
        mock_write_record.assert_called()



