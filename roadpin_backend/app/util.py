# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR
import random
import math
import base64
import time
import ujson as json
import traceback
from datetime import datetime
from datetime import timedelta

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


def date_today():
    today = datetime.today()
    return datetime_to_date(today)


def date_tomorrow():
    today = datetime.today()
    the_timedelta = timedelta(days=1)
    tomorrow = today + the_timedelta
    return datetime_to_date(tomorrow)


def datetime_to_date(the_datetime):
    year = '%04d' % the_datetime.year
    month = '%02d' % the_datetime.month
    day = '%02d' % the_datetime.day
    result = month + '/' + day + '/' + year
    cfg.logger.debug('result: %s', result)
    return result


def timestamp_to_date(the_timestamp):
    the_datetime = datetime.fromtimestamp(_float(the_timestamp))
    return datetime_to_date(the_datetime)


def _float(the_val, default_val=0):
    result = default_val
    try:
        result = float(the_val)
    except:
        cfg.logger.exception('unable to _float: the_val: %s default_val: %s', the_val, default_val)
        
    return result


def sleep_by_error_code(error_code):
    if error_code == S_OK:
        time.sleep(cfg.config.get('cron_success_sleep_time', 5))
    else:
        time.sleep(cfg.config.get('cron_fail_sleep_time', 3600))
