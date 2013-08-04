# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR
import random
import math
import base64
import time
import ujson as json

from app import cfg
from app import util

from app import cron_data

def post_add_handler(params):
    json_struct = util.json_loads(params.get('json', '{}'))
    (error_code, error_param) = util.check_valid_params(json_struct, ['county_name', 'the_category', 'the_idx', 'start_timestamp', 'end_timestamp', 'geo', 'the_data'])
    if error_code != S_OK:
        return (error_code, {"success": False, "error_msg": "no " + error_param})

    cron_data.process_data(json_struct['county_name'], json_struct['the_category'], json_struct['the_idx'], json_struct['start_timestamp'], json_struct['end_timestamp'], json_struct['geo'], json_struct['the_data'])

    return (S_OK, {"success": True})
