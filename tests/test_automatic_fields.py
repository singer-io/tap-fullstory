"""Test that with no fields selected for a stream automatic fields are still
replicated."""
from base import fullstoryBaseTest
from tap_tester.base_suite_tests.automatic_fields_test import MinimumSelectionTest


class fullstoryAutomaticFields(MinimumSelectionTest, fullstoryBaseTest):
    """Test that with no fields selected for a stream automatic fields are
    still replicated."""

    @staticmethod
    def name():
        return "tap_tester_fullstory_automatic_fields_test"

    def streams_to_test(self):
        streams_to_exclude = {}
        return self.expected_stream_names().difference(streams_to_exclude)
