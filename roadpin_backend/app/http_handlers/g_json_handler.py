# -*- coding: utf-8 -*-

import random
import math
import base64
import time
import ujson as json

from app import cfg
from app import util

from app.http_handlers.parse_json_map import parse_json_taipei_city_road_case
from app.http_handlers.parse_json_map import parse_json_taipei_city_dig_point
from app.http_handlers.parse_json_map import parse_json_kaohsiung_dig_point

_parse_json_map = {
    'taipei_city_road_case': parse_json_taipei_city_road_case,
    'taipei_city_dig_point': parse_json_taipei_city_dig_point,
    'kaohsiung_dig_point': parse_json_kaohsiung_dig_point,
}

def g_json_handler(start_timestamp, end_timestamp):
    start_timestamp = int(start_timestamp)
    end_timestamp = int(end_timestamp)

    cfg.logger.debug('start_timestamp: %s end_timestamp: %s', start_timestamp, end_timestamp)

    result_all = util.db_find('roadDB', {'end_timestamp': {'$gte': start_timestamp}, 'start_timestamp': {'$lte': end_timestamp}})
    cfg.logger.debug('len(result_all): %s', len(result_all))

    results = [result for result in result_all if _is_valid(result, start_timestamp, end_timestamp)]
    cfg.logger.debug('len(result): %s', len(result))

    results.sort(key=lambda (r): str(r['start_timestamp']) + '_' + str(r['end_timestamp']))

    to_remove_ary = []
    for (idx, result) in enumerate(results):
        del result['_id']
        the_category = result['the_category']

        if the_category not in _parse_json_map:
            cfg.logger.error('the_category is not in _parse_json_map: the_category: %s', the_category)
            to_remove_ary.append(idx)
            continue
        
        _parse_json_map[the_category](result)

        result['beginDate'] = util.timestamp_to_date_str(result['start_timestamp'])
        result['endDate'] = util.timestamp_to_date_str(result['end_timestamp'])

    to_remove_ary.reverse()
    for idx in to_remove_ary:
        del results[idx]

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
