
from base import fullstoryBaseTest
from tap_tester.base_suite_tests.interrupted_sync_test import InterruptedSyncTest


class fullstoryInterruptedSyncTest(InterruptedSyncTest, fullstoryBaseTest):
    """Test tap sets a bookmark and respects it for the next sync of a
    stream."""

    @staticmethod
    def name():
        return "tap_tester_fullstory_interrupted_sync_test"

    def streams_to_test(self):
        streams_to_exclude = {
            # Unsupported Full-Table Streams
            'segments',
            'users',
            'user'
        }
        return self.expected_stream_names().difference(streams_to_exclude)

    def manipulate_state(self):
        return {
            "currently_syncing": "block_rules",
            "bookmarks": {
                "block_rules": { "lastUpdated" : "2020-01-01T00:00:00Z"},
                "block_rules_history": { "lastUpdated" : "2020-01-01T00:00:00Z"},
                "domain_settings_history": { "lastUpdated" : "2020-01-01T00:00:00Z"},
                "domain_settings": { "lastUpdated" : "2020-01-01T00:00:00Z"},
                "geo_settings_history": { "lastUpdated" : "2020-01-01T00:00:00Z"},
                "privacy_settings": { "lastUpdated" : "2020-01-01T00:00:00Z"},
                "privacy_settings_history": { "lastUpdated" : "2020-01-01T00:00:00Z"},
                "recording_features": { "lastUpdated" : "2020-01-01T00:00:00Z"},
                "recording_features_history": { "lastUpdated" : "2020-01-01T00:00:00Z"},
                "target_rule_history": { "lastUpdated" : "2020-01-01T00:00:00Z"},
        }
    }
