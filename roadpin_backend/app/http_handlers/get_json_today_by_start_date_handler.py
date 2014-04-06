# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR
import random
import math
import base64
import time
import ujson as json
import pymongo

from app.constants import *
from app import cfg
from app import util

def get_json_today_by_start_date_handler(start_date, params):
    start_timestamp = util.date_to_timestamp(start_date)
    next_id = params.get('next_id', '')
    num_query = util._int(params.get('num_query', DEFAULT_NUM_QUERY))

    tomorrow = util.date_tomorrow()
    tomorrow_timestamp = util.date_to_timestamp(tomorrow)

    cfg.logger.debug('start_timestamp: %s tomorrow_timestamp: %s', start_timestamp, tomorrow_timestamp)

    the_query = {'start_timestamp': {'$lte': start_timestamp}, 'end_timestamp': {'$gte': tomorrow_timestamp}}
    if next_id:
        the_query['json_id'] = {"$lte": next_id}

    db_results = util.db_find_it('roadDB', the_query, {'_id': False, 'extension': False})

    db_results.sort([('json_id', pymongo.DESCENDING)]).limit(num_query)

    results = list(db_results)

    cfg.logger.debug('start_date: %s next_id: %s num_query: %s', start_date, next_id, num_query)
    for (idx, result) in enumerate(results):
        cfg.logger.debug('idx: %s result: %s', idx, result)

    return results
