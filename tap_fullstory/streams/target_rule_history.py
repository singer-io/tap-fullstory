from tap_fullstory.streams.abstracts import IncrementalStream
from typing import Dict

class TargetRuleHistory(IncrementalStream):
    tap_stream_id = "target_rule_history"
    key_properties = ["created", "createdBy", "lastUpdated"]
    replication_method = "INCREMENTAL"
    replication_keys = ["lastUpdated"]
    data_key = "versions"
    path = "/settings/recording/v1/targeting/history"

    def modify_object(self, record: Dict, parent_record: Dict = None) -> Dict:
        """
        Modify the record before writing to the stream
        """
        if record:
            record["lastUpdated"] = record.get("metadata").get("lastUpdated")
            record["created"] = record.get("metadata").get("created")
            record["createdBy"] = record.get("metadata").get("createdBy")
        return record
