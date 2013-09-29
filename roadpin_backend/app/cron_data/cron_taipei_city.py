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

from app.constants import N_ROAD_CASE, N_COUNT_FAIL_ROAD_CASE, N_DIG_POINT, N_COUNT_FAIL_DIG_POINT, MAX_TIMESTAMP

from app import cfg
from app import util
from app.cron_data import process_data

def cron_taipei_city():
    while True:
        error_code = _cron_taipei_city()
        sleep()


def _cron_taipei_city():
    params = _get_params()
    (error_code, results) = _crawl_data(params)
    return error_code


def _get_params():
    '''
    1. lookup the latest data in mongo.
    2. return the latest number of data.
    '''
    latest_road_case = util.get_cache('cron_taipei_city_latest_road_case')
    if not latest_road_case: 
        latest_road_case = cfg.config.get('first_road_case', 0)

    latest_dig_point = util.get_cache('cron_taipei_city_latest_dig_point')
    if not latest_dig_point:
        latest_dig_point = cfg.config.get('first_dig_point', 10000000)

    return {'latest_road_case': latest_road_case, 'latest_dig_point': latest_dig_point}


def _crawl_data(params):
    latest_road_case = _crawl_road_case(params['latest_road_case'])
    latest_dig_point = _crawl_dig_point(params['latest_dig_point'])

    return (S_ERR, {'latest_road_case': latest_road_case, 'latest_dig_point': latest_dig_point})


def _crawl_road_case(first_road_case):
    count_fail = 0
    latest_road_case = first_road_case
    offset_road_case = first_road_case
    while True:
        end_road_case = offset_road_case + N_ROAD_CASE
        road_cases = range(offset_road_case, end_road_case)
        offset_road_case += N_ROAD_CASE

        (the_urls, results) = _get_http_results(road_cases, 'http://www.road.tcg.gov.tw/ROADRCIS/GetCaseGeo.ashx?CASE_ID=%04d')

        (error_code, latest_road_case) = _process_http_results(the_urls, results, latest_road_case, 'taipei_city_road_case', 'WORK_DATEpro')

        cfg.logger.debug('road_cases: %s error_code: %s latest_road_case: %s', road_cases, error_code, latest_road_case)

        if error_code != S_OK:
            count_fail += 1

        if count_fail >= N_COUNT_FAIL_ROAD_CASE:
            break

        util.save_cache('cron_taipei_city_latest_road_case',  latest_road_case)

        cfg.logger.debug('to sleep 30')
        time.sleep(30)

    return latest_road_case


def _crawl_dig_point(first_dig_point):
    count_fail = 0
    latest_dig_point = first_dig_point
    offset_dig_point = first_dig_point
    while True:
        end_dig_point = offset_dig_point + N_DIG_POINT
        dig_points = range(offset_dig_point, end_dig_point)
        offset_dig_point += N_DIG_POINT

        (the_urls, results) = _get_http_results(dig_points, 'http://www.road.tcg.gov.tw/ROADRCIS/GetDigPoint.ashx?AP_NO=%08d')

        (error_code, latest_dig_point) = _process_http_results(the_urls, results, latest_dig_point, 'taipei_city_dig_point', 'CB_DATEpro')
        cfg.logger.debug('dig_points: %s error_code: %s latest_dig_point: %s', dig_points, error_code, latest_dig_point)

        if error_code != S_OK:
            count_fail += 1

        if count_fail >= N_COUNT_FAIL_DIG_POINT:
            break

        util.save_cache('cron_taipei_city_latest_dig_point',  latest_dig_point)

        cfg.logger.debug('to sleep 30')
        time.sleep(30)

    return latest_dig_point


def _get_http_results(idx_list, url_tmpl):
    the_urls = {idx: url_tmpl % (idx) for idx in idx_list}
    results = util.http_multiget(the_urls.values())
    return (the_urls, results)


def _process_http_results(the_urls, results, latest_idx, the_category, time_period_idx):
    if not results:
        return (S_ERR, latest_idx)

    cfg.logger.debug('results: %s', results)

    error_code = S_ERR
    for (idx, the_url) in the_urls.iteritems():
        the_data_text = results.get(the_url, '')
        if _validate_http_result(the_data_text) != S_OK:
            continue

        error_code = S_OK
        latest_idx = max(latest_idx, idx)

        _process_data_text(the_category, idx, the_data_text, time_period_idx)

    return (error_code, latest_idx)


def _validate_http_result(result):
    if not result:
        return S_ERR

    result_json = util.json_loads(result)
    if not result_json:
        return S_ERR

    if result == '-1':
        return S_ERR

    if result == u'-1':
        return S_ERR

    if result == -1:
        return S_ERR

    return S_OK


def _process_data_text(the_category, the_idx, the_data_text, time_period_idx):
    the_data = util.json_loads(the_data_text)
    data_list = the_data if the_data.__class__.__name__ == 'list' else [the_data]
    len_data_list = len(data_list)

    if len_data_list == 1:
        _process_each_data(the_category, the_idx, data_list[0], time_period_idx)
    else:
        [_process_each_data(the_category, the_idx + '.' + data_idx, each_data, time_period_idx) for (data_idx, each_data) in enumerate(data_list)]


def _process_each_data(the_category, the_idx, the_data, time_period_idx):
    if the_data.__class__.__name__ != 'dict':
        cfg.logger.error('the_data is not dict: the_category: %s the_idx: %s the_data: %s time_period_idx: %s', the_category, the_idx, the_data, time_period_idx)
        return

    (start_timestamp, end_timestamp) = _parse_time_period(the_data, time_period_idx)
    geo = _parse_geo(the_data)
    process_data('臺北市', the_category, the_idx, start_timestamp, end_timestamp, geo, the_data)


def _parse_time_period(the_data, time_period_idx):
    time_period = the_data.get(time_period_idx, '~')
    return _parse_time_period_core(time_period)


def _parse_time_period_core(time_period):
    try:
        time_period = re.sub(ur'/', '', time_period)
    except:
        cfg.logger.error('unable to re.sub time_period: time_period: (%s, %s)', time_period, time_period.__class__.__name__)
        time_period = '~'
        
    (start_tw_date, end_tw_date) = time_period.split('~')
    start_timestamp = util.tw_date_to_timestamp(start_tw_date)
    end_timestamp = util.tw_date_to_timestamp(end_tw_date)
    if end_timestamp == 0:
        end_timestamp = MAX_TIMESTAMP
    return (start_timestamp, end_timestamp)


def _parse_geo(the_data):
    geo_list = the_data.get('dtResultpro', [])
    the_geo = []
    for each_geo in geo_list:
        geo_type = 'LineString'

        points = each_geo.get('POINTS')

        coordinates = [_point_to_coordinate(point) for point in points]
        the_geo.append({'type': geo_type, 'coordinates': coordinates})
    return the_geo


def _point_to_coordinate(point):
    lat = point.get('P2', 0)
    lon = point.get('P1', 0)
    return [lon, lat]


def sleep():
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

    cron_taipei_city()

