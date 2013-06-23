# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR

import random
import math
import base64
import time
import ujson as json

import sys
import argparse

from app.constants import N_ROAD_CASE, N_COUNT_FAIL_ROAD_CASE, N_DIG_POINT, N_COUNT_FAIL_DIG_POINT

from app import cfg
from app import util

def cron_taipei_city():
    while True:
        error_code = _cron_taipei_city()
        _sleep()
    pass


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
        cfg.logger.debug('offset_road_case: %s end_road_case: %s', offset_road_case, end_road_case)
        road_cases = range(offset_road_case, end_road_case)
        offset_road_case += N_ROAD_CASE

        the_urls = {idx: 'http://www.road.tcg.gov.tw/ROADRCIS/GetCaseGeo.ashx?CASE_ID=%04d' % (idx) for idx in road_cases}
        results = util.http_multiget(the_urls.values())
        cfg.logger.debug('road_case: after http_multiget: results: %s', results)
        if not results:
            results = {}

        is_success = False
        for idx in road_cases:
            the_url = the_urls[idx]
            the_val = results[the_url]

            if not the_val:
                continue

            if the_val == '-1':
                continue

            if the_val == u'-1':
                continue

            is_success = True

            the_val = util.json_loads(the_val)
            cfg.logger.debug('with_data: the_url: %s the_val: %s', the_url, the_val)
            latest_road_case = idx
            _process_data(the_val, 'taipei_city_road_case', idx)

        if not is_success:
            count_fail += 1

        if count_fail >= N_COUNT_FAIL_ROAD_CASE:
            break

        util.save_cache('cron_taipei_city_latest_road_case',  latest_road_case)

    return latest_road_case


def _crawl_dig_point(first_dig_point):
    count_fail = 0
    latest_dig_point = first_dig_point
    offset_dig_point = first_dig_point
    while True:
        end_dig_point = offset_dig_point + N_DIG_POINT
        cfg.logger.debug('offset_dig_point: %s end_dig_point: %s', offset_dig_point, end_dig_point)
        dig_points = range(offset_dig_point, end_dig_point)
        offset_dig_point += N_DIG_POINT

        the_urls = {idx: 'http://www.road.tcg.gov.tw/ROADRCIS/GetDigPoint.ashx?AP_NO=%08d' % (idx) for idx in dig_points}
        results = util.http_multiget(the_urls.values())
        cfg.logger.debug('dig_point: after http_multiget: results: %s', results)
        if not results:
            results = {}

        is_success = False
        for idx in dig_points:
            the_url = the_urls[idx]
            the_val = results[the_url]
            if not the_val:
                continue

            if the_val == '-1':
                continue

            if the_val == u'-1':
                continue

            is_success = True

            the_val = util.json_loads(the_val)
            cfg.logger.debug('with_data: the_url: %s the_val: %s', the_url, the_val)
            latest_dig_point = idx
            _process_data(the_val, 'taipei_city_road_case', idx)

        if not is_success:
            count_fail += 1

        if count_fail >= N_COUNT_FAIL_DIG_POINT:
            break

        util.save_cache('cron_taipei_city_latest_dig_point',  latest_dig_point)

    return latest_dig_point


def _process_data(the_data, id_prefix, the_idx):
    if the_data.__class__.__name__ == 'dict':
        _process_data_core(the_data, id_prefix + '_' + str(the_idx))
    elif the_data.__class__.__name__ == 'list':
        for (each_idx, each_data) in enumerate(the_data):
            _process_data_core(each_data, id_prefix + '_' + str(the_idx) + '_' + str(each_idx))


def _process_data_core(data, the_id):
    data['the_id'] = the_id
    _put_to_db(data)


def _put_to_db(the_val):
    the_key = {'the_id': the_val['the_id']}
    util.db_update('roadDB', the_key, the_val)


def _sleep():
    time_sleep = util._int(cfg.config.get('time_sleep', 3600))
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

