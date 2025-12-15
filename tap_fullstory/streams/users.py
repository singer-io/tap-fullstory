from tap_fullstory.streams.abstracts import FullTableStream

class Users(FullTableStream):
    tap_stream_id = "users"
    key_properties = "id"
    replication_method = "FULL_TABLE"
    data_key = "results"
    path = "/v2/users"
    children = ["user"]

