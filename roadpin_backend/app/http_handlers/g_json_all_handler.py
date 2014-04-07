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
    num_query = util._int(params.get('num_query', DEFAULT_NUM_QUERY))

    the_query = {}
    if next_id:
        the_query['json_id'] = {'$lte': next_id}

    db_results = util.db_find_it('roadDB', the_query, {'_id': False, 'extension': False})

    db_results.sort([('json_id', pymongo.DESCENDING)]).limit(num_query)

    results = list(db_results)

    return results
