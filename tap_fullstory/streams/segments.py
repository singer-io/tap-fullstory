from tap_fullstory.streams.abstracts import FullTableStream

class Segments(FullTableStream):
    tap_stream_id = "segments"
    key_properties = ["id"]
    replication_method = "FULL_TABLE"
    data_key = "segments"
    path = "/segments/v1"
