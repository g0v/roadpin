# -*- coding: utf-8 -*-

import random
import math
import base64
import time
import ujson as json

from app import cfg
from app import util

from app.http_handlers.parse_json_map.parse_json_default import parse_json_default
from app.http_handlers.parse_json_map.parse_json_taipei_city_road_case import parse_json_taipei_city_road_case
from app.http_handlers.parse_json_map.parse_json_taipei_city_dig_point import parse_json_taipei_city_dig_point
from app.http_handlers.parse_json_map.parse_json_kaohsiung_dig_point import parse_json_kaohsiung_dig_point

_parse_json_map = {
    'taipei_city_road_case': parse_json_taipei_city_road_case,
    'taipei_city_dig_point': parse_json_taipei_city_dig_point,
    'kaohsiung_dig_point': parse_json_kaohsiung_dig_point,
}

def g_json_handler(start_timestamp, end_timestamp):
    db_results = get_db_results_by_the_timestamp(start_timestamp, end_timestamp)

    db_results.sort(key=lambda (r): str(r['start_timestamp']) + '_' + str(r['end_timestamp']))

    results = parse_json_results(db_results)

    return results


def parse_json_results(db_results):
    for (idx, result) in enumerate(db_results):
        the_category = result['the_category']

        _parse_json_map.get(the_category, parse_json_default)(result)

        result['beginDate'] = util.timestamp_to_date_str(result['start_timestamp'])
        result['endDate'] = util.timestamp_to_date_str(result['end_timestamp'])

    return db_results


def get_db_results_by_the_timestamp(start_timestamp, end_timestamp):
    start_timestamp = util._int(start_timestamp)
    end_timestamp = util._int(end_timestamp)

    result_all = util.db_find('roadDB', {'end_timestamp': {'$gte': start_timestamp}, 'start_timestamp': {'$lte': end_timestamp}})
    results = [result for result in result_all if _is_valid(result, start_timestamp, end_timestamp)]
    return results


def _is_valid(result, start_timestamp, end_timestamp):

    if not result['start_timestamp']:
        return False

    if not result['end_timestamp']:
        return False

    if result['start_timestamp'] <= start_timestamp and result['end_timestamp'] >= start_timestamp:
        return True

    if result['start_timestamp'] <= end_timestamp and result['end_timestamp'] >= end_timestamp:
        return True

    if result['start_timestamp'] >= start_timestamp and result['end_timestamp'] <= end_timestamp:
        return True

    if result['start_timestamp'] < start_timestamp and result['end_timestamp'] > end_timestamp:
        return True

    return False
