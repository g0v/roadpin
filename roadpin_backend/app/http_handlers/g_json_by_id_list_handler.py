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

def g_json_by_id_list_handler(params):
    id_list = params.get('id_list').split(',')

    id_list = [each_id for each_id in id_list if each_id]
    if not id_list:
        return []

    db_results = util.db_find('roadDB', {'the_idx': {'$in': id_list}})

    results = g_json_handler.parse_json_results(db_results)

    return results
