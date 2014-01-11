# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR

import random
import math
import base64
import time
import ujson as json
from StringIO import StringIO

import sys
import argparse
from lxml import html

from app import cfg
from app import util

def cron_new_taipei_city():
    while True:
        error_code = _cron_new_taipei_city()
        _sleep()
    pass


def _cron_new_taipei_city():
    #params = _get_params()
    (error_code, results) = _crawl_data()
    return error_code


def _get_params():
    '''
    1. lookup the latest data in mongo.
    2. return the latest params of data.
    '''
    latest_dig = util.get_cache('cron_new_taipei_city_latest_dig')
    return {'latest_dig': latest_dig}


def _crawl_data():
    results = _crawl_dig()
    return (S_OK, results)


def _crawl_dig():
    the_url = 'http://61.60.124.185/tpctempdig/InfoAllList.asp'
    start_timestamp = 946684800
    end_timestamp = util.get_timestamp() + 86400 * 366

    start_datetime = util.timestamp_to_datetime(start_timestamp)
    end_datetime = util.timestamp_to_datetime(end_timestamp)

    params = {
        'sortflag': '',
        'sorttype': '',
        'TargetLB': '',
        'qry2': 1,
        'startyear': start_datetime.year,
        'startmonth': start_datetime.month,
        'startday': start_datetime.day,
        'endyear': end_datetime.year,
        'endmonth': end_datetime.month,
        'endday': end_datetime.day,
    }

    http_data = util.http_multipost({the_url: params})
    #cfg.logger.debug('http_data: %s', http_data)
    (latest_timestamp, dig_data) = _parse_dig(http_data[the_url])

    [_put_to_db(each_data) for each_data in dig_data]

    util.save_cache('cron_new_taipei_city_latest_dig', {'latest_timestamp': latest_timestamp})


def _parse_dig(http_data):
    #cfg.logger.debug('http_data_type: %s', http_data.__class__.__name__)
    http_data_ascii = http_data.encode('iso-8859-1')
    data_utf8 = util.big5_to_utf8(http_data_ascii)
    #cfg.logger.debug('data_utf8: %s', data_utf8)

    (latest_timestamp, data_list) = _parse_dig_data(data_utf8)
    return (latest_timestamp, data_list)


def _parse_dig_data(data):
    doc = html.parse(StringIO(data))
    #cfg.logger.debug('doc: %s', doc)

    results = [_parse_element(elem) for elem in doc.iter('tr')]
    results = [result for result in results if result]

    latest_timestamp = 0
    for result in results:
        start_timestamp = result.get('start_timestamp', 0)
        if start_timestamp > latest_timestamp:
            latest_timestamp = start_timestamp
    
    return (latest_timestamp, results)


def _parse_element(elem):
    text = elem.text_content()
    #cfg.logger.debug('text: %s', text)
    return _parse_text(text)

def _parse_text(text):
    _columns = [ '', 'OK_UNITpro', 'IDpro', 'APP_NAMEpro', 'LOCATIONpro', 'CB_DATEpro', 'APPROVE_DATEpro']

    f = StringIO(text)
    lines = f.readlines()
    n_lines = len(lines)
    if n_lines > 10 or n_lines < 7:
        cfg.logger.error('lines > 10: lines: %s', lines)
        return {}

    result = {column: lines[idx].strip() for (idx, column) in enumerate(_columns) if column}
    if not result.get('OK_UNITpro', ''):
        result = {}
    if not result.get('CB_DATEpro', ''):
        result = {}

    cfg.logger.debug('result: %s', result)
    (start_timestamp, end_timestamp) = _parse_timestamp(result)
    geo = _parse_geo(result)
    result['start_timestamp'] = start_timestamp
    result['end_timestamp'] = end_timestamp
    result['geo'] = geo

    return result


def _put_to_db(data):
    category = 'new_taipei_city_dig_point'
    the_idx = data['IDpro']
    start_timestamp = data.get('start_timestamp', 0)
    end_timestamp = data.get('end_timestamp', 0)
    geo = data.get('geo', {})

    process_data('新北市', category, the_idx, start_timestamp, end_timestamp, geo, data)


def _sleep():
    time_sleep = util._int(cfg.config.get('time_sleep', 86400))
    cfg.logger.debug('to sleep: time_sleep: %s', time_sleep)
    time.sleep(time_sleep)


def parse_args():
    ''' '''
    parser = argparse.ArgumentParser(description='roadpin_backend')
    parser.add_argument('-i', '--ini', type=str, required=True, help="ini filename")

    args = parser.parse_args()

    return (S_OK, args)


if __name__ == '__main__':
    (error_code, args) = parse_args()

    cfg.init({"ini_filename": args.ini})

    cron_new_taipei_city()

