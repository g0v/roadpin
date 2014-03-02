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


def do_crawler_taipei_city_road_case(next_road_case):
    results = crawler_taipei_city_road_case({'next_road_case': next_road_case})
    util.to_json(results['data'], 'log.taipei_city_road_case.json')


def crawler_taipei_city_road_case(params):
    results = _crawl_data(params['next_road_case'])

    return results


def _crawl_data(next_road_case):
    (next_road_case, data) = _crawl_road_case(next_road_case)
    crawlers.set_county_name(data, '臺北市')
    crawlers.set_category(data, 'taipei_city_road_case')

    return {'next_road_case': next_road_case, 'data': data}


def _crawl_road_case(next_road_case):
    '''
    1. start from the next_road_case. 
    2. n iterations of crawls
    input: next_road_case: next possible road case to retrieve.
    return: results_list: the list of available results.
            next_road_case: next possible road case to retrieve (max id in results_list + 1)
    '''
    results = {}

    # start from next_road_case
    offset_road_case = next_road_case 

    # iter
    for idx in range(0, N_ITER_CRAWL_ROAD_CASE):
        cfg.logger.debug('idx: %s to _iter_crawl_road_case: next_road_case: %s offset_road_case: %s', idx, next_road_case, offset_road_case)
        (error_code, next_road_case, offset_road_case, iter_results) = _iter_crawl_road_case(next_road_case, offset_road_case)

        results.update(iter_results)

        cfg.logger.debug('to sleep 30')
        time.sleep(30)

    results_list = results.values()

    return (next_road_case, results_list)


def _iter_crawl_road_case(next_road_case, offset_road_case):
    '''
    1. if success: continue do iteration.
    2. else: return results
    '''

    results = {}
    while True:
        (error_code, next_road_case, offset_road_case, iter_results) = _iter_crawl_road_case_core(next_road_case, offset_road_case)
        if error_code != S_OK:
            break

        results.update(iter_results)

    error_code = S_OK if results else S_ERR
    return (error_code, next_road_case, offset_road_case, results)


def _iter_crawl_road_case_core(next_road_case, offset_road_case):
    '''
    core to crawl_road_case.
    1. get the range to of road_caseas
    2. get http results by the range of road cases.
    3. parse the results
    '''
    start_road_case = offset_road_case
    end_road_case = offset_road_case + N_ROAD_CASE
    offset_road_case += N_ROAD_CASE

    road_cases = range(start_road_case, end_road_case)

    (error_code, http_results) = _get_http_results(road_cases)
    cfg.logger.debug('error_code: %s http_results: %s', error_code, http_results)

    if error_code != S_OK:
        return (error_code, next_road_case, offset_road_case, {})
    
    (error_code, latest_road_case, results) = _process_http_results(road_cases, http_results)
    cfg.logger.debug('error_code: %s next_road_case: %s latest_road_case: %s results: %s', error_code, next_road_case, latest_road_case, results)

    if error_code != S_OK:
        return (error_code, next_road_case, offset_road_case, {})

    return (S_OK, latest_road_case + 1, offset_road_case, results)


def _get_http_results(road_cases):
    the_urls = {road_case: 'http://www.road.tcg.gov.tw/ROADRCIS/GetCaseGeo.ashx?CASE_ID=%04d' % road_case for road_case in road_cases}

    http_results = util.http_multiget(the_urls.values())

    if not http_results:
        return (S_ERR, {})

    results = {road_case: http_results.get(the_url, '') for (road_case, the_url) in the_urls.iteritems()}

    return (S_OK, results)


def _process_http_results(road_cases, http_results):
    results = {}
    latest_road_case = None
    for road_case in road_cases:
        each_result = http_results.get(road_case, '')
        parsed_result = _parse_http_result(road_case, each_result)
        if not parsed_result:
            continue
        latest_road_case = road_case
        results.update(parsed_result)

    cfg.logger.debug('road_cases: %s latest_road_case: %s results: %s', road_cases, latest_road_case, results)

    if latest_road_case is None:
        return (S_ERR, latest_road_case, {})

    return (S_OK, latest_road_case, results)


def _parse_http_result(road_case, result):
    data = util.json_loads(result)
    cfg.logger.debug('result: %s data: %s', result, data)
    if taipei_city.validate_http_result_json(data) != S_OK:
        return {}

    return _process_data(road_case, data)


def _process_data(road_case, data):
    return {str(road_case) + '.' + str(idx): _process_each_data(road_case, idx, each_data) for (idx, each_data) in enumerate(data)}


def _process_each_data(road_case, idx, data):
    cfg.logger.debug('road_case: %s idx: %s data: %s', road_case, idx, data)
    the_idx = str(road_case) + '.' + str(idx)

    time_period = data.get('WORK_DATEpro', '~')
    if not time_period: time_period = '~'

    (start_timestamp, end_timestamp) = taipei_city.parse_time_period(time_period)

    geo_data = data.get('dtResultpro', [])
    if not geo_data: geo_data = []
    geo = taipei_city.parse_geo(geo_data)

    town_name = data.get('REG_NAMEpro', '')
    if not town_name: town_name = ''
    elif not re.search(ur'區$', town_name): town_name += u'區'

    location = data.get('CASE_LOCATIONpro', '')
    if not location: location = '' 

    the_range = data.get('CASE_RANGEpro', '')
    if not the_range: the_range = ''

    work_institute = data.get('CTR_WNAMEpro', '')
    if not work_institute: work_institute = ''

    work_institute2 = data.get('CTR_ONAMEpro', '')
    if not work_institute2: work_institute2 = ''

    status = data.get('CASE_STATUSpro', 0)
    if not status: status = 0

    category_type = data.get('CASE_TYPEpro', 0)
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
    parser.add_argument('-n', '--next_road_case', type=int, required=True, help="next road case")

    args = parser.parse_args()

    return (S_OK, args)


if __name__ == '__main__':
    (error_code, args) = parse_args()

    cfg.init({"ini_filename": args.ini})

    do_crawler_taipei_city_road_case(args.next_road_case)
