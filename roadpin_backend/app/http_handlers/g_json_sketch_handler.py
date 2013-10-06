# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR
import random
import math
import base64
import time
import ujson as json

from app import cfg
from app import util

from app.http_handlers import g_json_handler

def g_json_sketch_handler(start_timestamp, end_timestamp, params):

    db_results = g_json_handler.get_db_results_by_the_timestamp(start_timestamp, end_timestamp)

    results = [result.get('the_id', '') for result in db_results]

    return results
