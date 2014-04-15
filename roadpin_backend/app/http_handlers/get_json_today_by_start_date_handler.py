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
    sort_order = params.get('order', 'DESC')
    num_query = util._int(params.get('num_query', DEFAULT_NUM_QUERY))

    today = util.date_today()
    today_timestamp = util.date_to_timestamp(today)

    cfg.logger.debug('start_timestamp: %s today_timestamp: %s', start_timestamp, today_timestamp)

    the_query = {'start_timestamp': {'$lte': start_timestamp}, 'end_timestamp': {'$gte': today_timestamp}}
    if next_id:
        query_key = '$lte' if sort_order in ['desc', 'DESC'] else '$gte'
        the_query['json_id'] = {query_key: next_id}

    db_results = util.db_find_it('roadDB', the_query, {'_id': False, 'extension': False})

    sort_flag = pymongo.DESCENDING if is_desc else pymongo.ASCENDING
    db_results.sort([('json_id', sort_flag)]).limit(num_query)

    results = list(db_results)

    cfg.logger.debug('start_date: %s next_id: %s num_query: %s', start_date, next_id, num_query)
    for (idx, result) in enumerate(results):
        cfg.logger.debug('idx: %s result: %s', idx, result)

    return results
