from tap_fullstory.streams.abstracts import IncrementalStream

class RecordingFeatures(IncrementalStream):
    tap_stream_id = "recording_features"
    key_properties = ["created", "createdBy", "lastUpdated"]
    replication_method = "INCREMENTAL"
    replication_keys = ["lastUpdated"]
    path = "/settings/recording/v1/features"

