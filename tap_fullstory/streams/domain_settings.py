from tap_fullstory.streams.abstracts import IncrementalStream
from typing import Dict, Iterator

class DomainSettings(IncrementalStream):
    tap_stream_id = "domain_settings"
    key_properties = ["created", "createdBy", "lastUpdated"]
    replication_method = "INCREMENTAL"
    replication_keys = ["lastUpdated"]
    path = "/settings/recording/v1/domain"

    def modify_object(self, record: Dict, parent_record: Dict = None) -> Dict:
        """
        Modify the record before writing to the stream
        """
        if record:
            record["lastUpdated"] = record.get("metadata").get("lastUpdated")
            record["created"] = record.get("metadata").get("created")
            record["createdBy"] = record.get("metadata").get("createdBy")
        return record

    def get_records(self) -> Iterator[Dict]:

        data = self.client.make_request(self.http_method, self.url_endpoint, params={}, headers=self.headers)

        yield data
