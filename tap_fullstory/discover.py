import singer
from tap_fullstory.streams import STREAMS
from tap_fullstory.schema import get_schemas

LOGGER = singer.get_logger()


def discover():
    """
    Run the discover mode, prepare the catalog file and return the catalog
    """

    schemas, field_metadata = get_schemas()
    streams = []

    for stream_name, schema_dict in schemas.items():
        mdata = field_metadata[stream_name]

        catalog_entry = {
            "stream": stream_name,
            "tap_stream_id": stream_name,
            "key_properties": STREAMS[stream_name].key_properties,
            "schema": singer.resolve_schema_references(schema_dict),
            "metadata": mdata,
        }

        streams.append(catalog_entry)

    return {"streams": streams}
