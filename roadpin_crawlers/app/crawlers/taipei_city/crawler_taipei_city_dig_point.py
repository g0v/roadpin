# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR
import random
import math
import base64
import time
import ujson as json
import re

import sys
import argparse

from app.constants import *

from app import cfg
from app import util
from app import crawlers
from app.crawlers import taipei_city


def do_crawler_taipei_city_dig_point(next_dig_point):
    results = crawler_taipei_city_dig_point({'next_dig_point': next_dig_point})
    util.to_json(results['data'], 'log.taipei_city_dig_point.json')


def crawler_taipei_city_dig_point(params):
    results = _crawl_data(params['next_dig_point'])

    return results


def _crawl_data(next_dig_point):
    (next_dig_point, data) = _crawl_dig_point(next_dig_point)
    crawlers.set_county_name(data, '臺北市')
    crawlers.set_category(data, 'taipei_city_dig_point')

    return {'next_dig_point': next_dig_point, 'data': data}


def _crawl_dig_point(next_dig_point):
    results = {}

    offset_dig_point = next_dig_point

    for idx in range(0, N_ITER_CRAWL_DIG_POINT):
        (error_code, next_dig_point, offset_dig_point, iter_results) = _iter_crawl_dig_point(next_dig_point, offset_dig_point)
        results.update(iter_results)

        sleep_time = cfg.config.get('time_sleep', 30)
        cfg.logger.debug('to sleep %s', sleep_time)
        time.sleep(sleep_time)

    results_list = results.values()

    return (next_dig_point, results_list)


def _iter_crawl_dig_point(next_dig_point, offset_dig_point):
    '''
    1. if success: continue do iteration.
    2. else: return results
    '''

    results = {}
    while True:
        (error_code, next_dig_point, offset_dig_point, iter_results) = _iter_crawl_dig_point_core(next_dig_point, offset_dig_point)
        if error_code != S_OK:
            break

        results.update(iter_results)

    error_code = S_OK if results else S_ERR
    return (error_code, next_dig_point, offset_dig_point, results)


def _iter_crawl_dig_point_core(next_dig_point, offset_dig_point):
    '''
    core to crawl_dig_point.
    1. get the range to of dig_points
    2. get http results by the range of road cases.
    3. parse the results
    '''
    start_dig_point = offset_dig_point
    end_dig_point = offset_dig_point + N_DIG_POINT
    offset_dig_point += N_DIG_POINT

    dig_points = range(start_dig_point, end_dig_point)

    (error_code, http_results) = _get_http_results(dig_points)
    cfg.logger.debug('error_code: %s http_results: %s', error_code, http_results)

    if error_code != S_OK:
        return (error_code, next_dig_point, offset_dig_point, {})
    
    (error_code, latest_dig_point, results) = _process_http_results(dig_points, http_results)
    cfg.logger.debug('error_code: %s next_dig_point: %s latest_dig_point: %s results: %s', error_code, next_dig_point, latest_dig_point, results)

    if error_code != S_OK:
        return (error_code, next_dig_point, offset_dig_point, {})

    return (S_OK, latest_dig_point + 1, offset_dig_point, results)


def _get_http_results(dig_points):
    the_urls = {dig_point: 'http://www.road.tcg.gov.tw/ROADRCIS/GetDigPoint.ashx?AP_NO=%d' % dig_point for dig_point in dig_points}

    http_results = util.http_multiget(the_urls.values())

    if not http_results:
        return (S_ERR, {})

    results = {dig_point: http_results.get(the_url, '') for (dig_point, the_url) in the_urls.iteritems()}

    return (S_OK, results)


def _process_http_results(dig_points, http_results):
    results = {}
    latest_dig_point = None
    for dig_point in dig_points:
        each_result = http_results.get(dig_point, '')
        parsed_result = _parse_http_result(dig_point, each_result)
        if not parsed_result:
            continue
        latest_dig_point = dig_point
        results.update(parsed_result)

    cfg.logger.debug('dig_points: %s latest_dig_point: %s results: %s', dig_points, latest_dig_point, results)

    if latest_dig_point is None:
        return (S_ERR, latest_dig_point, {})

    return (S_OK, latest_dig_point, results)


def _parse_http_result(dig_point, result):
    data = util.json_loads(result)
    cfg.logger.debug('after json_loads: result: %s data: %s', result, data)
    if taipei_city.validate_http_result_json(data) != S_OK:
        return {}

    return _process_data(dig_point, data)


def _process_data(dig_point, data):
    return {str(dig_point) + '.' + str(idx): _process_each_data(dig_point, idx, each_data) for (idx, each_data) in enumerate(data)}


def _process_each_data(dig_point, idx, data):
    cfg.logger.debug('dig_point: %s idx: %s data: %s', dig_point, idx, data)
    the_idx = str(dig_point) + '.' + str(idx)
    time_period = data.get('CB_DATEpro', '~')
    if not time_period: time_period = '~'
    (start_timestamp, end_timestamp) = taipei_city.parse_time_period(time_period)

    geo_data = data.get('dtResultpro', [])
    if not geo_data: geo_data = []
    geo = taipei_city.parse_geo(geo_data)

    town_name = data.get('C_NAMEpro', '')
    if not town_name: town_name = ''
    elif not re.search(ur'區$', town_name): town_name += u'區'

    location = data.get('LOCATIONpro', '')
    if not location: location = '' 

    the_range = ''

    work_institute = data.get('TC_NApro', '')
    if not work_institute: work_institute = ''

    work_institute2 = ''

    status = data.get('CASE_STATUSpro', 0)
    if not status: status = 0

    category_type = data.get('KIND_TYPEpro', 0)
    if not category_type: category_type = 0
    
    return {
        'the_idx': the_idx,
        'start_timestamp': start_timestamp,
        'end_timestamp': start_timestamp,
        'geo': geo,
        'town_name': town_name,
        'location': location,
        'range': the_range,
        'work_institute': work_institute,
        'work_institute2': work_institute2,
        'status': status,
        'category_type': category_type,
        'extension': data,
    }


def parse_args():
    ''' '''
    parser = argparse.ArgumentParser(description='roadpin_backend')
    parser.add_argument('-i', '--ini', type=str, required=True, help="ini filename")
    parser.add_argument('-n', '--next_dig_point', type=int, required=True, help="next dig point")

    args = parser.parse_args()

    return (S_OK, args)


if __name__ == '__main__':
    (error_code, args) = parse_args()

    cfg.init({"ini_filename": args.ini})

    do_crawler_taipei_city_dig_point(args.next_dig_point)
