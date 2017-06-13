#!/usr/bin/env python3

import os
import time
import re

import json
import backoff
import pendulum
import requests
import datetime
import dateutil.parser
import tempfile
import gzip
import singer
import singer.stats
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

def transform_datetime(datetime):
    if datetime is None:
        return None

    return pendulum.parse(datetime).format(utils.DATETIME_FMT)


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


def parse_source_from_url(url):
    match = re.match(r'^(\w+)\/', url)
    if match:
        return match.group(1)


def unzip_to_json(content):
    with tempfile.TemporaryFile() as temp_file:
        temp_file.write(content)
        temp_file.seek(0)
        with gzip.open(temp_file) as unzipped_file:
            body = unzipped_file.read().decode()
            return json.loads(body)

def request(endpoint, params=None):
    url = BASE_URL + endpoint
    params = params or {}
    headers = {}
    if 'user_agent' in CONFIG:
        headers['User-Agent'] = CONFIG['user_agent']

    headers['Authorization'] = "Basic " + CONFIG['api_key']
    req = requests.Request("GET", url, params=params, headers=headers).prepare()
    LOGGER.info("GET {}".format(req.url))

    with singer.stats.Timer(source=parse_source_from_url(endpoint)) as stats:
        resp = SESSION.send(req)
        stats.http_status_code = resp.status_code
        if resp.headers.get('Content-Type') == "application/gzip":
            json_body = unzip_to_json(resp.content)
            stats.record_count = len(json_body)
        else:
            json_body = resp.json()
            if 'data' in json_body:
                stats.record_count = len(json_body['data'])

    # if we're hitting the rate limit cap, sleep until the limit resets
    if resp.headers.get('X-Rate-Limit-Remaining') == "0":
        time.sleep(int(resp.headers['X-Rate-Limit-Reset']))

    # if we're already over the limit, we'll get a 429
    # sleep for the rate_reset seconds and then retry
    if resp.status_code == 429:
        time.sleep(resp.json()["rate_reset"])
        return request(endpoint, params)

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
    singer.write_schema("events", schema, ["IndvId"])

    start = get_start("events")
    list_params = {"start": start}

    for export_bundle in request_export_bundles():
        for event in download_events(export_bundle['Id']):
            transform_event(event)
            singer.write_record("events", event)
        utils.update_state(STATE, "events", datetime.datetime.utcfromtimestamp(export_bundle['Stop']))
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
