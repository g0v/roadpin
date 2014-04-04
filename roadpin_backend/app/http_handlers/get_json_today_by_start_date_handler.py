# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR
import random
import math
import base64
import time
import ujson as json

from app import cfg
from app import util

def get_json_today_by_start_date_handler(start_date, params):
    start_timestamp = util.date_to_timestamp(start_date)
    next_idx = params.get('next_idx', '')
    num_query = util._int(params.get('num_query', 0))

    the_query = {'start_timestamp': {'$lte': start_timestamp}, 'end_timestamp': {'$gte': tomorrow_timestamp}}
    if next_idx:
        the_query['the_idx']
    pass
