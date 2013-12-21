# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR
import random
import math
import base64
import time
import ujson as json
import traceback
import pytz
import hashlib
from pytz import timezone
from calendar import timegm
from datetime import datetime
from datetime import timedelta
import grequests

from app import cfg

def trace(params):
    traceback.print_stack()


def db_find(cf_name, key = None, fields={'_id': False}):
    result = []
    try:
        if key is None:
            result = cfg.config.get(cf_name).find(fields=fields)
        else:
            result = cfg.config.get(cf_name).find(key, fields=fields)
    except:
        cfg.logger.exception('unable to db_find: cf_name: %s key: %s', cf_name, key)
        result = None
        
    if result is None:
        result = []
    return list(result)


def db_find_one(cf_name, key, fields={'_id': False}):
    try:
        result = cfg.config.get(cf_name).find_one(key, fields=fields)
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


def date_today():
    today = datetime.today()
    return datetime_to_date(today)


def date_tomorrow():
    today = datetime.today()
    the_timedelta = timedelta(days=1)
    tomorrow = today + the_timedelta
    return datetime_to_date(tomorrow)


def datetime_to_date(the_datetime):
    result = the_datetime.strftime("%Y%m%d")
    return result


def datetime_to_date_str(the_datetime):
    result = the_datetime.strftime("%Y-%m-%d")
    return result


def date_to_timestamp(the_date):
    the_datetime = datetime.strptime(the_date, "%Y%m%d")
    the_datetime = the_datetime.replace(tzinfo = timezone('Asia/Taipei'))
    the_timestamp = _int(timegm(the_datetime.utctimetuple()))
    return the_timestamp


def timestamp_to_date(the_timestamp):
    the_datetime = datetime.fromtimestamp(_float(the_timestamp))
    return datetime_to_date(the_datetime)


def timestamp_to_date_str(the_timestamp):
    the_datetime = datetime.fromtimestamp(_float(the_timestamp))
    return datetime_to_date_str(the_datetime)


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


def http_multipost(the_url_data):
    the_urls = the_url_data.keys()
    rs = (grequests.post(the_url, data=the_url_data[the_url], timeout=5) for the_url in the_urls)
    result_map = grequests.map(rs)

    try:
        result_map_text = [_grequest_get_text(each_result_map) for each_result_map in result_map]
        result = {the_url: result_map_text[idx] for (idx, the_url) in enumerate(the_urls)}
    except:
        cfg.logger.exception('the_url_data: %s', the_url_data)
        result = {}
    return result


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


def big5_to_utf8(text_big5):
    str_utf8 = unicode(text_big5, 'big5')
    return str_utf8


def utf8_to_big5(text_utf8):
    str_big5 = text_utf8.encode('big5')
    return str_big5


def tw_date_to_timestamp(tw_date):
    tw_date = str(tw_date)
    tw_year = tw_date[0:-4]
    month = _int(tw_date[-4:-2])
    if month == 0:
        return 0

    day = _int(tw_date[-2:])
    if day == 0:
        return 0

    year = _int(tw_year)
    if year == 0:
        return 0
    year += 1911

    date_time = datetime(year, month, day, tzinfo=timezone('Asia/Taipei'))
    the_timestamp = _int(timegm(date_time.utctimetuple()))
    #cfg.logger.debug('tw_date: %s tw_year: %s year: %s month: %s day: %s date_time: %s the_timestamp: %s', tw_date, tw_year, year, month, day, date_time, the_timestamp)
    return the_timestamp


def check_url(params):
    the_str = params.get('json', '') + cfg.config.get('secret_key', '')
    md5_str = hashlib.md5(the_str).hexdigest()
    if md5_str != params.get('sig', ''):
        return (S_ERR, {"success": False, "error_msg": "invalid sig"})

    return (S_OK, {})


def check_valid_params(params, columns):
    for column in columns: 
        if column not in params:
            return (S_ERR, column)
    
    return (S_OK, '')


def get_timestamp():
    return int(time.time())


def get_milli_timestamp():
    return int(time.time() * 1000)
