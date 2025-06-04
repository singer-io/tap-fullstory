import os
import json
from singer import metadata
from tap_fullstory.streams import STREAMS

def get_abs_path(path):
    """Return absolute path for a file relative to this script."""
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


def get_schemas():
    """
    Load schema JSON files and build metadata for each stream.
    Returns:
      - schemas: dict of {stream_name: schema_json}
      - field_metadata: dict of {stream_name: metadata_list}
    """
    schemas = {}
    field_metadata = {}

    for stream_name, stream_metadata in STREAMS.items():
        schema_path = get_abs_path(f"schemas/{stream_name}.json")

        with open(schema_path, "r") as f:
            schema = json.load(f)

        schemas[stream_name] = schema

        # Create metadata object
        mdata = metadata.new()

        # Add standard metadata for replication, key properties, etc.
        mdata = metadata.get_standard_metadata(
            schema=schema,
            key_properties=getattr(stream_metadata, "key_properties", []),
            valid_replication_keys=getattr(stream_metadata, "replication_keys", []),
            replication_method=getattr(stream_metadata, "replication_method", None),
        )

        # Mark replication keys as "automatic" inclusion in metadata
        mdata_map = metadata.to_map(mdata)
        for field_name in schema.get("properties", {}).keys():
            if (
                    getattr(stream_metadata, "replication_keys", None)
                    and field_name in stream_metadata.replication_keys
            ):
                mdata_map = metadata.write(
                    mdata_map,
                    ("properties", field_name),
                    "inclusion",
                    "automatic",
                )

        # Convert back to list form for Singer
        mdata = metadata.to_list(mdata_map)

        field_metadata[stream_name] = mdata

    return schemas, field_metadata
