import pytz
import singer
from datetime import datetime, timedelta

TRAILING_DAYS = timedelta(days=30)
DEFAULT_TIMESTAMP = "1970-01-01T00:00:00Z"
LOGGER = singer.get_logger()


class Stream:
    name = None
    replication_method = None
    replication_keys = None
    key_properties = None
    parent_stream = None

    # To write schema in output
    def write_schema(self, schema, stream_name, sync_streams, selected_streams):
        """
        To write schema in output
        """
        try:
            # Write_schema for the stream if it is selected in catalog
            if stream_name in selected_streams and stream_name in sync_streams:
                singer.write_schema(stream_name, schema, self.key_properties)
        except OSError as err:
            LOGGER.error("OS Error writing schema for: {}".format(stream_name))
            raise err

    def to_utc(self, dt):
        """
        Set UTC offset for Python datetime object
        """
        return dt.replace(tzinfo=pytz.UTC)

    def write_bookmark(self, state, stream, value):
        """
        To write bookmark in sync mode
        """

        if "bookmarks" not in state:
            state["bookmarks"] = {}
        if stream not in state["bookmarks"]:
            state["bookmarks"][stream] = {}

        state["bookmarks"][stream] = value
        singer.write_state(state)

    def daterange(self, start_date, end_date):
        """
        Generator function that produces an iterable list of days between the two
        dates start_date and end_date as a tuple pair of datetimes.
        Note:
            All times are set to 0:00. Designed to be used in date query where query
            logic would be record_date >= 2019-01-01 0:00 and record_date < 2019-01-02 0:00
        Args:
            start_date (datetime): start of period
            end_date (datetime): end of period
        Yields:
            tuple: daily period
                * datetime: day within range
                * datetime: day within range + 1 day
        """

        # set to start of day
        start_date = self.to_utc(
            datetime.combine(
                start_date.date(),
                datetime.min.time(),  # set to the 0:00 on the day of the start date
            )
        )
        end_date = self.to_utc(end_date + timedelta(1))

        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n), start_date + timedelta(n + 1)


class Events(Stream):
    name = "events"
    key_properties = ["UserId"]

STREAMS = {"events":Events}
