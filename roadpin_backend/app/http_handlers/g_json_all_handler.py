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

def g_json_all_handler():
    db_results = util.db_find('roadDB', {})
    db_results.sort(key=lambda (r): str(r['start_timestamp']) + '_' + str(r['end_timestamp']))

    results = g_json_handler.parse_json_results(db_results)

    return results
