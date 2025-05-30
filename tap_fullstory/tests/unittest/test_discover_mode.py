import unittest
from unittest.mock import patch, MagicMock
import tap_fullstory

class TestDiscoverMode(unittest.TestCase):

    @patch("tap_fullstory.singer.write_schema")
    @patch("tap_fullstory.load_schema")
    @patch("tap_fullstory.LOGGER")
    def test_do_discover(self, mock_logger, mock_load_schema, mock_write_schema):
        # Arrange
        mock_schema = {"type": "object", "properties": {"id": {"type": "string"}}}
        mock_load_schema.return_value = mock_schema
        tap_fullstory.do_discover()

        mock_logger.info.assert_called_once_with("Running in discovery mode")
        mock_load_schema.assert_called_once_with("events")
        mock_write_schema.assert_called_once_with("events", mock_schema, [])



