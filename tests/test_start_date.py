from base import fullstoryBaseTest
from tap_tester.base_suite_tests.start_date_test import StartDateTest



class fullstoryStartDateTest(StartDateTest, fullstoryBaseTest):
    """Instantiate start date according to the desired data set and run the
    test."""

    @staticmethod
    def name():
        return "tap_tester_fullstory_start_date_test"

    def streams_to_test(self):
        streams_to_exclude = {
            # Unsupported Full-Table Streams
            'users',
            'user',
            'segments',
            # Less data only one record can not change the data due to permission
            'block_rules',
            'domain_settings',
            'geo_settings_history',
            'privacy_settings',
            'recording_features',
            'target_rule_history',
            'recording_features_history',
            'block_rules_history',
            'domain_settings_history',
        }
        return self.expected_stream_names().difference(streams_to_exclude)

    @property
    def start_date_1(self):
        return "2025-12-01T05:35:00.00Z"
    @property
    def start_date_2(self):
        return "2025-12-16T00:00:00.00Z"
