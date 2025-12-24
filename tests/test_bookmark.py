from base import fullstoryBaseTest
from tap_tester.base_suite_tests.bookmark_test import BookmarkTest


class fullstoryBookMarkTest(BookmarkTest, fullstoryBaseTest):
    """Test tap sets a bookmark and respects it for the next sync of a
    stream."""
    bookmark_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    initial_bookmarks = {
        "bookmarks": {
            "block_rules_history": { "lastUpdated" : "2024-12-15T00:00:00Z"},
            "domain_settings_history": { "lastUpdated" : "2024-12-15T00:00:00Z"},
            "privacy_settings_history": { "lastUpdated" : "2024-12-15T00:00:00Z"},
            "recording_features_history": { "lastUpdated" : "2024-12-15T00:00:00Z"},
        }
    }
    @staticmethod
    def name():
        return "tap_tester_fullstory_bookmark_test"

    def streams_to_test(self):
        streams_to_exclude = {
            # Unsupported Full-Table Streams
            'users',
            'user',
            'segments',
            # Less data only one record
            'block_rules',
            'domain_settings',
            'geo_settings_history',
            'privacy_settings',
            'recording_features',
            'target_rule_history',
        }
        return self.expected_stream_names().difference(streams_to_exclude)
        
    def calculate_new_bookmarks(self):
        """Calculates new bookmarks by looking through sync 1 data to determine
        a bookmark that will sync 2 records in sync 2 (plus any necessary look
        back data)"""
        new_bookmarks = {
            "domain_settings_history": { "lastUpdated" : "2025-12-10T00:00:00Z"},
            "privacy_settings_history": { "lastUpdated" : "2025-12-16T00:00:00Z"},
            "recording_features_history": { "lastUpdated" : "2025-05-13T08:01:19.684286Z"},

        }

        return new_bookmarks
