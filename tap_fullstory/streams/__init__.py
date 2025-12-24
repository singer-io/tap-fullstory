from tap_fullstory.streams.users import Users
from tap_fullstory.streams.user import User
from tap_fullstory.streams.block_rules import BlockRules
from tap_fullstory.streams.block_rules_history import BlockRulesHistory
from tap_fullstory.streams.domain_settings_history import DomainSettingsHistory
from tap_fullstory.streams.domain_settings import DomainSettings
from tap_fullstory.streams.geo_settings_history import GeoSettingsHistory
from tap_fullstory.streams.privacy_settings import PrivacySettings
from tap_fullstory.streams.privacy_settings_history import PrivacySettingsHistory
from tap_fullstory.streams.recording_features import RecordingFeatures
from tap_fullstory.streams.recording_features_history import RecordingFeaturesHistory
from tap_fullstory.streams.target_rule_history import TargetRuleHistory
from tap_fullstory.streams.segments import Segments

STREAMS = {
    "users": Users,
    "user": User,
    "block_rules": BlockRules,
    "block_rules_history": BlockRulesHistory,
    "domain_settings_history": DomainSettingsHistory,
    "domain_settings": DomainSettings,
    "geo_settings_history": GeoSettingsHistory,
    "privacy_settings": PrivacySettings,
    "privacy_settings_history": PrivacySettingsHistory,
    "recording_features": RecordingFeatures,
    "recording_features_history": RecordingFeaturesHistory,
    "target_rule_history": TargetRuleHistory,
    "segments": Segments,
}

