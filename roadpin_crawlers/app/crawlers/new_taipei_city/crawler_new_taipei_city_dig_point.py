# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR
import random
import math
import base64
import time
import ujson as json
from StringIO import StringIO
from datetime import datetime
import re
import argparse

import sys
from lxml import html

from app import cfg
from app import util
from app import crawlers

def do_crawler_new_taipei_city_dig_point(next_year):
    next_year = util._int(next_year)
    results = crawler_new_taipei_city_dig_point({'next_year': next_year})
    util.to_json(results['data'], 'log.new_taipei_city_dig_point.json')


def crawler_new_taipei_city_dig_point(params):
    next_year = params['next_year']
    data = _crawl_data(next_year)

    crawlers.set_county_name(data, '新北市')
    crawlers.set_category(data, 'new_taipei_city_dig_point')


    return {"data": data}


def _crawl_data(the_year):
    '''
    return {data: list of data}

    data: {the_idx, start_timestamp, end_timestamp, geo, town_name, location, range, work_institute, work_institute2, status, category_type, extension}
    '''
    the_url = 'http://61.60.124.185/tpctempdig/InfoAllList.asp'

    params = {
        'sortflag': '',
        'sorttype': '',
        'TargetLB': '',
        'qry2': 1,
        'startyear': the_year,
        'startmonth': 1,
        'startday': 1,
        'endyear': the_year,
        'endmonth': 12,
        'endday': 31,
    }

    http_data = util.http_multipost({the_url: params})
    dig_data = _parse_dig(http_data[the_url])

    return dig_data


def _parse_dig(http_data):
    http_data_ascii = http_data.encode('iso-8859-1')
    data_utf8 = util.big5_to_utf8(http_data_ascii)

    #cfg.logger.debug('data_utf8: %s', data_utf8)

    data_list = _parse_dig_data(data_utf8)
    return data_list


def _parse_dig_data(data):
    doc = html.parse(StringIO(data))

    elements = doc.xpath("//tr[@class='g3']")

    results = [_parse_element(elem) for elem in elements]
    results = [result for result in results if result]

    return results


def _parse_element(elem):
    text = elem.text_content()
    return _parse_text(text)

def _parse_text(text):
    #cfg.logger.debug('text: %s', text)
    _columns = [ 'OK_UNITpro', 'IDpro', 'APP_NAMEpro', 'LOCATIONpro', 'CB_DATEpro', 'APPROVE_DATEpro']

    f = StringIO(text)
    lines = f.readlines()
    lines = [line for line in lines if line.strip()]
    n_lines = len(lines)
    if n_lines != 6:
        cfg.logger.error('lines != 6: lines: %s', lines)
        return {}

    cfg.logger.debug('lines: %s', lines)

    data = {column: lines[idx].strip() for (idx, column) in enumerate(_columns) if column}
    if not data.get('OK_UNITpro', ''):
        return {}

    return _parse_data(data)


def _parse_data(data):
    the_idx = data['IDpro']
    (start_timestamp, end_timestamp) = _parse_time_period(data)
    geo = _parse_geo(data)
    town_name = _parse_town_name(data)
    location = data['LOCATIONpro']
    work_institute = data['APP_NAMEpro']

    return {
        'the_idx': the_idx,
        'start_timestamp': start_timestamp,
        'end_timestamp': end_timestamp,
        'geo': geo,
        'town_name': town_name,
        'location': location,
        'range': '',
        'work_institute': work_institute,
        'work_institute2': '',
        'status': '',
        'category_type': '',
        'extension': data,
    }


def _parse_time_period(data):
    time_period = data.get('CB_DATEpro', '~')
    return _parse_time_period_core(time_period)


def _parse_time_period_core(time_period):
    time_period_split = time_period.split('~')
    if len(time_period_split) != 2:
        return (0, MAX_TIMESTAMP)

    start_date = time_period_split[0]
    end_date = time_period_split[1]

    start_timestamp = _parse_date(start_date)
    end_timestamp = _parse_date(end_date)

    if end_timestamp == 0:
        end_timestamp = MAX_TIMESTAMP
    
    return (start_timestamp, end_timestamp)


def _parse_date(the_date):
    the_date_list = the_date.split('/')
    if len(the_date_list) != 3:
        return 0

    the_year = util._int(the_date_list[0])
    the_month = util._int(the_date_list[1])
    the_day = util._int(the_date_list[2])

    cfg.logger.debug('the_date: %s the_year: %s the_month: %s the_day: %s', the_date, the_year, the_month, the_day)

    the_datetime = datetime(the_year, the_month, the_day)
    the_timestamp = util.datetime_to_timestamp(the_datetime)

    return the_timestamp


def _parse_geo(data):
    return []


def _parse_town_name(data):
    return re.sub(u'區.*', u'區', data['LOCATIONpro'])


def parse_args():
    ''' '''
    parser = argparse.ArgumentParser(description='roadpin_backend')
    parser.add_argument('-i', '--ini', type=str, required=True, help="ini filename")
    parser.add_argument('-n', '--next_year', type=str, required=True, help="next_year")

    args = parser.parse_args()

    return (S_OK, args)


if __name__ == '__main__':
    (error_code, args) = parse_args()

    cfg.init({"ini_filename": args.ini})

    do_crawler_new_taipei_city_dig_point(args.next_year)
