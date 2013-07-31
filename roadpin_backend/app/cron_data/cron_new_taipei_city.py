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
    params = _get_params()
    (error_code, results) = _crawl_data(params)
    return error_code


def _get_params():
    '''
    1. lookup the latest data in mongo.
    2. return the latest params of data.
    '''
    latest_dig = util.get_cache('cron_new_taipei_city_latest_dig')
    return {'latest_dig': latest_dig}


def _crawl_data(params):
    results = _crawl_dig(params['latest_dig'])
    return (S_OK, results)


def _crawl_dig(last_dig):
    the_url = 'http://61.60.124.185/tpctempdig/InfoAllList.asp'
    params = {
        'sortflag': '',
        'sorttype': '',
        'TargetLB': '',
        'startyear': last_dig.get('start_year', 2000),
        'startmonth': last_dig.get('start_month', 1),
        'endyear': last_dig.get('end_year', 2014),
        'endmonth': last_dig.get('end_month', 12),
        'endday': last_dig.get('endday', 31)
    }

    http_data = util.http_multipost({the_url: params})
    #cfg.logger.debug('http_data: %s', http_data)
    dig_data = _parse_dig(http_data[the_url])

    [_put_to_db(each_data) for each_data in dig_data]


def _parse_dig(http_data):
    #cfg.logger.debug('http_data_type: %s', http_data.__class__.__name__)
    http_data_ascii = http_data.encode('iso-8859-1')
    data_utf8 = util.big5_to_utf8(http_data_ascii)
    #cfg.logger.debug('data_utf8: %s', data_utf8)

    data_list = _parse_dig_data(data_utf8)
    return data_list


def _parse_dig_data(data):
    doc = html.parse(StringIO(data))
    #cfg.logger.debug('doc: %s', doc)

    results = [_parse_element(elem) for elem in doc.iter('tr')]
    results = [result for result in results if result]
    
    return results


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
        
    return result


def _put_to_db(data):
    category = 'new_taipei_city_dig_point'
    the_idx = data['IDpro']
    the_id = category + '_' + the_idx
    the_key = {'the_category': category, 'the_id': the_id, 'the_idx': the_idx}
    util.db_update('roadDB', the_key, data)


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

