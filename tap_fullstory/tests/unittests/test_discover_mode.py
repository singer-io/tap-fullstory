import unittest
from unittest import mock
from tap_fullstory.discover import discover

class TestDiscoverMode(unittest.TestCase):

    @mock.patch("tap_fullstory.schema.get_schemas")
    def test_discover_output_structure(self, mock_get_schemas):
        # Mock schema and metadata
        mock_get_schemas.return_value = (
            {
                "events": {
                    "type": "object",
                    "properties": {
                        "EventStart": {"type": "string"},
                        "UserId": {"type": "string"}
                    }
                }
            },
            {
                "events": [
                    {
                        "metadata": {},
                        "breadcrumb": [],
                        "inclusion": "available"
                    }
                ]
            }
        )

        catalog = discover()

        self.assertIn("streams", catalog)
        self.assertEqual(len(catalog["streams"]), 1)

        stream = catalog["streams"][0]
        self.assertEqual(stream["stream"], "events")
        self.assertIn("schema", stream)
        self.assertIn("metadata", stream)
        self.assertEqual(stream["tap_stream_id"], "events")
        self.assertEqual(stream["key_properties"], ["UserId"])

if __name__ == '__main__':
    unittest.main()
