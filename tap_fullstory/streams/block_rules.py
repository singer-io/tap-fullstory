from tap_fullstory.streams.abstracts import IncrementalStream

class BlockRules(IncrementalStream):
    tap_stream_id = "block_rules"
    key_properties = ["created", "createdBy", "lastUpdated"]
    replication_method = "INCREMENTAL"
    replication_keys = ["lastUpdated"]
    path = "/settings/recording/v1/blocking"

