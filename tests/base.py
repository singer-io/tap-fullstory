import copy
import os
import unittest
from datetime import datetime as dt
from datetime import timedelta

import dateutil.parser
import pytz
from tap_tester import connections, menagerie, runner
from tap_tester.logger import LOGGER
from tap_tester.base_suite_tests.base_case import BaseCase


class fullstoryBaseTest(BaseCase):
    """Setup expectations for test sub classes.

    Metadata describing streams. A bunch of shared methods that are used
    in tap-tester tests. Shared tap-specific methods (as needed).
    """
    start_date = "2019-01-01T00:00:00Z"
    PARENT_TAP_STREAM_ID = "parent-tap-stream-id"

    @staticmethod
    def tap_name():
        """The name of the tap."""
        return "tap-fullstory"

    @staticmethod
    def get_type():
        """The name of the tap."""
        return "platform.fullstory"

    @classmethod
    def expected_metadata(cls):
        """The expected streams and metadata about the streams."""
        return {
            "users": {
                cls.PRIMARY_KEYS: { "id" },
                cls.REPLICATION_METHOD: cls.FULL_TABLE,
                cls.REPLICATION_KEYS: set(),
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100,
            },
            "user": {
                cls.PRIMARY_KEYS: { "id" },
                cls.REPLICATION_METHOD: cls.FULL_TABLE,
                cls.REPLICATION_KEYS: set(),
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100,
                cls.PARENT_TAP_STREAM_ID: "users"
            },
            "block_rules": {
                cls.PRIMARY_KEYS: { "created", "createdBy", "lastUpdated" },
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: { "lastUpdated" },
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100,
            },
            "block_rules_history": {
                cls.PRIMARY_KEYS: { "created", "createdBy", "lastUpdated" },
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: { "lastUpdated" },
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100,
            },
            "domain_settings_history": {
                cls.PRIMARY_KEYS: { "created", "createdBy", "lastUpdated" },
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: { "lastUpdated" },
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100,
            },
            "domain_settings": {
                cls.PRIMARY_KEYS: { "created", "createdBy", "lastUpdated" },
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: { "lastUpdated" },
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100,
            },
            "geo_settings_history": {
                cls.PRIMARY_KEYS: { "created", "createdBy", "lastUpdated" },
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: { "lastUpdated" },
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100,
            },
            "privacy_settings": {
                cls.PRIMARY_KEYS: { "created", "createdBy", "lastUpdated" },
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: { "lastUpdated" },
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100,
            },
            "privacy_settings_history": {
                cls.PRIMARY_KEYS: { "created", "createdBy", "lastUpdated" },
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: { "lastUpdated" },
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100,
            },
            "recording_features": {
                cls.PRIMARY_KEYS: { "created", "createdBy", "lastUpdated" },
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: { "lastUpdated" },
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100,
            },
            "recording_features_history": {
                cls.PRIMARY_KEYS: { "created", "createdBy", "lastUpdated" },
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: { "lastUpdated" },
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100,
            },
            "target_rule_history": {
                cls.PRIMARY_KEYS: { "created", "createdBy", "lastUpdated" },
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: { "lastUpdated" },
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100,
            },
            "segments": {
                cls.PRIMARY_KEYS: { "id" },
                cls.REPLICATION_METHOD: cls.FULL_TABLE,
                cls.REPLICATION_KEYS: set(),
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100,
            }
        }

    @staticmethod
    def get_credentials():
        """Authentication information for the test account."""
        credentials_dict = {}
        creds = {'api_key': 'TAP_FULLSTORY_API_KEY'}

        for cred in creds:
            credentials_dict[cred] = os.getenv(creds[cred])

        return credentials_dict
    
    def get_properties(self, original: bool = True):
        """Configuration of properties required for the tap."""
        return {
            "start_date": self.start_date
        }

    def expected_parent_tap_stream(self, stream=None):
        """return a dictionary with key of table name and value of parent stream"""
        parent_stream = {
            table: properties.get(self.PARENT_TAP_STREAM_ID, None)
            for table, properties in self.expected_metadata().items()}
        if not stream:
            return parent_stream
        return parent_stream[stream]
