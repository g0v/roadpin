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
import grequests

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


def db_find_one(cf_name, key):
    try:
        result = cfg.config.get(cf_name).find_one(key)
    except:
        cfg.logger.exception('unable to db_find_one: cf_name: %s key: %s', cf_name, key)
        result = None

    if result is None:
        result = {}

    return dict(result)


def db_update(cf_name, key, val):
    if not key or not val:
        cfg.logger.exception('not key or val: key: %s val: %s', key, val)
        return

    cfg.logger.debug('cf_name: %s key: %s val: %s', cf_name, key, val)
    result = cfg.config.get(cf_name).update(key, {'$set':val}, upsert=True, w=1)
    #cfg.logger.debug('after update: result: %s', result)
    return result


def json_dumps(json_struct, default_val=''):
    result = default_val
    try:
        result = json.dumps(json_struct)
    except:
        cfg.logger.exception('unable to json_dumps: json_struct: %s', json_struct)

    return result


def json_loads(json_str, default_val={}):
    result = default_val
    try:
        result = json.loads(json_str)
    except:
        cfg.logger.exception('unable to json_loads: json_str: %s', json_str)
        result = default_val

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


def _int(the_val, default_val=0):
    result = default_val
    try:
        result = int(the_val)
    except:
        cfg.logger.exception('unable to _int: the_val: %s default_val: %s', the_val, default_val)
        
    return result


def init_cache(cache, cache_name):
    if cache_name not in cache:
        cache[cache_name] = get_cache(cache_name)


def save_cache(key, cache):
    db_update('cacheDB', {'cache_key':key}, {'cache_val':json_dumps(cache)})


def get_cache(key):
    result_db = db_find_one('cacheDB', {'cache_key':key})
    result_db = {} if not result_db else result_db
    return json_loads(result_db.get('cache_val', '{}'), result_db.get('cache_val', {}))


def http_multiget(the_urls):
    rs = (grequests.get(u, timeout=5) for u in the_urls)
    result_map = grequests.map(rs)
    try:
        result_map_text = [_grequest_get_text(each_result_map) for each_result_map in result_map]
        result = {the_url: result_map_text[idx] for (idx, the_url) in enumerate(the_urls)}
    except:
        cfg.logger.exception('the_urls: %s', the_urls)
        result = {}

    return result


def _grequest_get_text(result):
    if result is None:
        return ''
    if not hasattr(result, 'text'):
        return ''
    return result.text
