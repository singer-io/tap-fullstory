from tap_fullstory.streams.abstracts import IncrementalStream

class BlockRulesHistory(IncrementalStream):
    tap_stream_id = "block_rules_history"
    key_properties = ["created", "createdBy", "lastUpdated"]
    replication_method = "INCREMENTAL"
    replication_keys = ["lastUpdated"]
    data_key = "versions"
    path = "/settings/recording/v1/blocking/history"

