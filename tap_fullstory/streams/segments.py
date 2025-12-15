from tap_fullstory.streams.abstracts import IncrementalStream

class Segments(IncrementalStream):
    tap_stream_id = "segments"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["created"]
    data_key = "segments"
    path = "/segments/v1"

