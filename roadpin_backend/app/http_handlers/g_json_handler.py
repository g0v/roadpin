# -*- coding: utf-8 -*-

import random
import math
import base64
import time
import ujson as json

from app import cfg
from app import util

def g_json_handler(start_timestamp, end_timestamp):
    start_timestamp = int(start_timestamp)
    end_timestamp = int(end_timestamp)

    cfg.logger.debug('start_timestamp: %s end_timestamp: %s', start_timestamp, end_timestamp)

    result_all = util.db_find('roadDB')
    #cfg.logger.debug('result_all: %s', result_all)

    results = [result for result in result_all if _is_valid(result, start_timestamp, end_timestamp)]

    results.sort(key=lambda (r): str(r['start_timestamp']) + '_' + str(r['end_timestamp']), reverse=True)


    for result in results:
        del result['_id']
        result['beginDate'] = util.timestamp_to_date(result['start_timestamp'])
        result['endDate'] = util.timestamp_to_date(result['end_timestamp'])

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
        
    
    
def _result_to_dict(result):
    return {str(val['start_timestamp']) + '_' + str(val['end_timestamp']): val for val in result}
