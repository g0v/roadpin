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
from app.http_handlers import g_json_handler

def g_json_all_handler(params):
    next_id = params.get('next_id', '')
    sort_order = params.get('order', 'DESC')
    is_desc = True if sort_order in ['desc', 'DESC'] else False
    num_query = util._int(params.get('num_query', DEFAULT_NUM_QUERY))

    the_query = {}
    if next_id:
        query_key = '$lte' if is_desc else '$gte'
        the_query['json_id'] = {query_key: next_id}

    db_results = util.db_find_it('roadDB', the_query, {'_id': False, 'extension': False})

    sort_flag = pymongo.DESCENDING if is_desc else pymongo.ASCENDING
    db_results.sort([('json_id', sort_flag)]).limit(num_query)

    results = list(db_results)

    return results
