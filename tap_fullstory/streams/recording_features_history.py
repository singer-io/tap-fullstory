from tap_fullstory.streams.abstracts import IncrementalStream

class RecordingFeaturesHistory(IncrementalStream):
    tap_stream_id = "recording_features_history"
    key_properties = ["created", "createdBy", "lastUpdated"]
    replication_method = "INCREMENTAL"
    replication_keys = ["lastUpdated"]
    data_key = "versions"
    path = "/settings/recording/v1/features/history"

