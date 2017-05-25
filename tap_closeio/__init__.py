#!/usr/bin/env python3

import os
import time
import re

import backoff
import pendulum
import requests
import dateutil.parser
import singer
import singer.stats
from singer import utils


REQUIRED_CONFIG_KEYS = ["start_date", "api_key"]
PER_PAGE = 100
BASE_URL = "https://app.close.io/api/v1/"

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

    return STATE[key]


def parse_source_from_url(url):
    match = re.match(r'^(\w+)\/', url)
    if match:
        return match.group(1)


def request(endpoint, params=None):
    url = BASE_URL + endpoint
    params = params or {}
    headers = {}
    if 'user_agent' in CONFIG:
        headers['User-Agent'] = CONFIG['user_agent']

    auth = (CONFIG['api_key'], "")
    req = requests.Request("GET", url, params=params, auth=auth, headers=headers).prepare()
    LOGGER.info("GET {}".format(req.url))

    with singer.stats.Timer(source=parse_source_from_url(endpoint)) as stats:
        resp = SESSION.send(req)
        stats.http_status_code = resp.status_code
        json = resp.json()
        if 'data' in json:
            stats.record_count = len(json['data'])

    # if we're hitting the rate limit cap, sleep until the limit resets
    if resp.headers.get('X-Rate-Limit-Remaining') == "0":
        time.sleep(int(resp.headers['X-Rate-Limit-Reset']))

    # if we're already over the limit, we'll get a 429
    # sleep for the rate_reset seconds and then retry
    if resp.status_code == 429:
        time.sleep(json["rate_reset"])
        return request(endpoint, params)

    resp.raise_for_status()

    return json


def gen_request(endpoint, params=None):
    params = params or {}
    params['_limit'] = PER_PAGE
    params['_skip'] = 0

    while True:
        body = request(endpoint, params)
        for row in body['data']:
            yield row

        if not body.get("has_more"):
            break

        params['_skip'] += PER_PAGE


def transform_activity(activity):
    transform_datetimes(activity, ["date_scheduled"])
    if "envelope" in activity:
        transform_datetimes(activity["envelope"], ["date"])

    if "send_attempts" in activity:
        for item in activity["send_attempts"]:
            transform_datetimes(item, ["date"])


def sync_activities():
    schema = load_schema("activities")
    singer.write_schema("activities", schema, ["id"])

    start = get_start("activities")
    params = {"date_created__gt": start}

    for row in gen_request("activity/", params):
        transform_activity(row)
        if row['date_created'] >= start:
            singer.write_record("activities", row)
            utils.update_state(STATE, "activities", dateutil.parser.parse(row['date_created']))

    singer.write_state(STATE)


def to_json_type(typ):
    if typ in ["datetime", "date"]:
        return {"type": ["null", "string"], "format": "date-time"}

    if typ == "number":
        return {"type": ["null", "number"]}

    return {"type": ["null", "string"]}


def get_custom_leads_schema():
    return {
        "type": "object",
        "properties": {row["name"]: to_json_type(row["type"])
                       for row in gen_request("custom_fields/lead/")},
    }


def transform_lead(lead, custom_schema):
    if "tasks" in lead:
        for item in lead["tasks"]:
            transform_datetimes(item, ["date", "due_date"])

    if "opportunities" in lead:
        for item in lead["opportunities"]:
            transform_datetimes(item, ["date_won"])

    if "custom" in lead:
        custom_datetimes = [k for k, v in custom_schema["properties"].items()
                            if v.get("format") == "date-time"]
        transform_datetimes(lead["custom"], custom_datetimes)


def sync_leads():
    schema = load_schema("leads")
    custom_schema = get_custom_leads_schema()
    schema["properties"]["custom"] = custom_schema
    singer.write_schema("leads", schema, ["id"])

    start = get_start("leads")
    formatted_start = dateutil.parser.parse(start).strftime("%Y-%m-%d %H:%M")
    params = {'query': 'date_updated>="{}" sort:date_updated'.format(formatted_start)}

    for i, row in enumerate(gen_request("lead/", params)):
        transform_lead(row, custom_schema)
        row['contacts'] = [request("contact/{}/".format(contact['id']))
                           for contact in row['contacts']]
        if row['date_updated'] >= start:
            singer.write_record("leads", row)
            utils.update_state(STATE, "leads", dateutil.parser.parse(row['date_updated']))

        if i % PER_PAGE == 0:
            singer.write_state(STATE)

    singer.write_state(STATE)


def do_sync():
    LOGGER.info("Starting sync")
    sync_activities()
    sync_leads()
    LOGGER.info("Completed sync")


def main():
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)
    CONFIG.update(args.config)
    STATE.update(args.state)
    do_sync()


if __name__ == "__main__":
    main()
