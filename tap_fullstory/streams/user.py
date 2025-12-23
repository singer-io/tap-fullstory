from tap_fullstory.streams.abstracts import FullTableStream
from typing import Dict, Iterator

class User(FullTableStream):
    tap_stream_id = "user"
    key_properties = ["id"]
    replication_method = "FULL_TABLE"
    path = "/v2/users/{id}"
    parent = "users"
    data_key = ""

    def get_url_endpoint(self, parent_obj=None):
        """Prepare URL endpoint for child streams."""
        if not parent_obj or 'id' not in parent_obj:
            raise ValueError("parent_obj must be provided with an 'id' key.")
        return f"{self.client.base_url}/{self.path.format(id=parent_obj['id'])}"

    def get_records(self) -> Iterator[Dict]:

        data = self.client.make_request(self.http_method, self.url_endpoint, params={}, headers=self.headers)

        yield data
