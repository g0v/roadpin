# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR
import random
import math
import base64
import time
import ujson as json
import argparse

from app.constants import *
from app import cfg
from app import util

from app import cron
from app.crawlers.new_taipei_city import crawler_new_taipei_city_dig_point

def cron_new_taipei_city_dig_point():
    params = {}
    while True:
        (error_code, params) = _get_params(params)

        cfg.logger.debug('error_code: %s params: %s', error_code, params)

        if error_code != S_OK:
            break

        results = crawler_new_taipei_city_dig_point.crawler_new_taipei_city_dig_point(params)

        _process_results(results)


def _get_params(params):
    if not params:
        server = cfg.config.get('web_server', 'http://106.187.101.193:5346')
        the_url = server + '/get/new_taipei_city_dig_point_next_year'
        http_result = util.http_multiget([the_url])

        next_year = util._int(util.json_loads(http_result.get(the_url, ''), ''), START_NEW_TAIPEI_CITY_DIG_POINT_YEAR)
        this_year = _get_this_year()

        next_year = min(next_year, this_year)

        cfg.logger.debug('after http_multiget: http_result: %s next_year: %s', http_result, next_year)

        return (S_OK, {'next_year': next_year})

    next_year = params.get('next_year', START_NEW_TAIPEI_CITY_DIG_POINT_YEAR)
    stop_year = _get_stop_year()

    if next_year == stop_year:
        return (S_ERR, {'next_year': next_year})

    next_year += 1

    return (S_OK, {'next_year': next_year})


def _get_this_year():
    the_datetime = util.get_datetime()

    return the_datetime.year


def _get_stop_year():
    return _get_this_year() + 1


def _process_results(results):
    data = results.get('data', [])
    cron.to_http_post(data)

    util.to_json(data, 'log.new_taipei_city_dig_point.json')


def parse_args():
    ''' '''
    parser = argparse.ArgumentParser(description='roadpin_backend')
    parser.add_argument('-i', '--ini', type=str, required=True, help="ini filename")

    args = parser.parse_args()

    return (S_OK, args)


if __name__ == '__main__':
    (error_code, args) = parse_args()

    cfg.init({"ini_filename": args.ini})

    cron_new_taipei_city_dig_point()
