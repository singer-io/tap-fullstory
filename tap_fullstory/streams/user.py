from tap_fullstory.streams.abstracts import FullTableStream

class User(FullTableStream):
    tap_stream_id = "user"
    key_properties = "id"
    replication_method = "FULL_TABLE"
    path = "/v2/users/{id}"
    parent = "users"

