#!/usr/bin/env python3

import os
import time
import re
import io

import json
import datetime
import gzip
import dateutil.parser
import requests
import pendulum
import backoff
import singer
import singer.metrics as metrics
from singer import utils


REQUIRED_CONFIG_KEYS = ["start_date", "api_key"]
PER_PAGE = 100
BASE_URL = "https://www.fullstory.com/api/v1/export/"

CONFIG = {}
STATE = {}

LOGGER = singer.get_logger()
SESSION = requests.session()


def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)

def load_schema(entity):
    return utils.load_json(get_abs_path("schemas/{}.json".format(entity)))

def transform_datetime(datetime_string):
    if datetime_string is None:
        return None

    return pendulum.parse(datetime_string).format(utils.DATETIME_FMT)


def transform_datetimes(item, datetime_fields):
    if not isinstance(datetime_fields, list):
        datetime_fields = [datetime_fields]

    for k in datetime_fields:
        if k in item:
            item[k] = transform_datetime(item[k])


def get_start(key):
    if key not in STATE:
        STATE[key] = CONFIG['start_date']

    return int(pendulum.parse(STATE[key]).timestamp())


def unzip_to_json(content):
    content_io = io.BytesIO(content)
    content_gz = gzip.GzipFile(fileobj=content_io, mode='rb')
    decoded = content_gz.read()
    return json.loads(decoded)


def giveup(exc):
    return exc.response is not None \
        and 400 <= exc.response.status_code < 500 \
        and exc.response.status_code != 429


def on_giveup(details):
    if len(details['args']) == 2:
        url, params = details['args']
    else:
        url = details['args']
        params = {}

    raise Exception("Giving up on request after {} tries with url {} and params {}" \
                    .format(details['tries'], url, params))

@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException,
                      max_tries=5,
                      giveup=giveup,
                      on_giveup=on_giveup,
                      factor=2)
@utils.ratelimit(9, 1)
def request(endpoint, params=None):
    url = BASE_URL + endpoint
    params = params or {}
    headers = {}
    if 'user_agent' in CONFIG:
        headers['User-Agent'] = CONFIG['user_agent']

    headers['Authorization'] = "Basic " + CONFIG['api_key']
    req = requests.Request("GET", url, params=params, headers=headers).prepare()
    LOGGER.info("GET {}".format(req.url))

    with metrics.http_request_timer(url) as timer:
        resp = SESSION.send(req)
        timer.tags[metrics.Tag.http_status_code] = resp.status_code

    if resp.headers.get('Content-Type') == "application/gzip":
        json_body = unzip_to_json(resp.content)
    else:
        json_body = resp.json()

    resp.raise_for_status()

    return json_body


def request_export_bundles():
    params = {}
    fs_max_results_per_page = 20
    while True:
        params["start"] = get_start("events")
        body = request("list", params)
        for row in body['exports']:
            yield row

        if len(body["exports"]) < fs_max_results_per_page:
            break


def transform_event(event):
    transform_datetimes(event, ["EventStart"])


def download_events(file_id):
    params = {"id": file_id}
    body = request("get", params)
    return body


def sync_events():
    schema = load_schema("events")
    singer.write_schema("events", schema, [])

    for export_bundle in request_export_bundles():
        with metrics.record_counter("events") as counter:
            for event in download_events(export_bundle['Id']):
                transform_event(event)
                counter.increment()
                singer.write_record("events", event)
            stop_timestamp = datetime.datetime.utcfromtimestamp(export_bundle['Stop'])
            utils.update_state(STATE, "events", stop_timestamp)
            singer.write_state(STATE)


def do_sync():
    LOGGER.info("Starting sync")
    sync_events()
    LOGGER.info("Completed sync")


def main():
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)
    CONFIG.update(args.config)
    STATE.update(args.state)
    do_sync()


if __name__ == "__main__":
    main()
