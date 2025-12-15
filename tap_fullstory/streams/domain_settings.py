from tap_fullstory.streams.abstracts import IncrementalStream

class DomainSettings(IncrementalStream):
    tap_stream_id = "domain_settings"
    key_properties = ["created", "createdBy", "lastUpdated"]
    replication_method = "INCREMENTAL"
    replication_keys = ["lastUpdated"]
    path = "/settings/recording/v1/domain"

