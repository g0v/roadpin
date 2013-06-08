# -*- coding: utf-8 -*-

import random
import math
import base64
import time
import ujson as json
import traceback
from datetime import datetime

from app import cfg

def trace(params):
    traceback.print_stack()


def db_find(cf_name, key = None):
    result = []
    try:
        if key is None:
            result = cfg.config.get(cf_name).find()
        else:
            result = cfg.config.get(cf_name).find(key)
    except:
        cfg.logger.exception('unable to db_find: cf_name: %s key: %s', cf_name, key)
        result = None
        
    if result is None:
        result = []
    return list(result)


def json_dumps(json_struct):
    result = json_struct
    try:
        result = json.dumps(json_struct)
    except:
        cfg.logger.exception('unable to json_dumps: json_struct: %s', json_struct)
        result = ''

    return result


def date_to_timestamp(the_date):
    cfg.logger.debug('the_date: %s', the_date)
    month = int(str(the_date)[0:2])
    day = int(str(the_date)[3:5])
    year = int(str(the_date)[6:10])
    cfg.logger.debug('year: %s month: %s day: %s', year, month, day)
    the_date_datetime = datetime(year=year, month=month, day=day)
    the_timestamp = int(time.mktime(the_date_datetime.timetuple()))
    cfg.logger.debug('the_timestamp: %s', the_timestamp)
    return the_timestamp
