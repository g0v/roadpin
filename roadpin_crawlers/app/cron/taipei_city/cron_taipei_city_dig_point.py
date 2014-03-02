# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR
import random
import math
import base64
import time
import ujson as json

import sys
import argparse

from app.constants import *
from app import cfg
from app import util
from app import cron
from app.crawlers.taipei_city import crawler_taipei_city_dig_point

def cron_taipei_city_dig_point():
    params = _get_params()

    cfg.logger.debug('params: %s', params)

    results = crawler_taipei_city_dig_point.crawler_taipei_city_dig_point(params)

    _process_results(results)


def _get_params():
    server = cfg.config.get('web_server', 'http://106.187.101.193:5346')
    the_url = server + '/get/taipei_city_road_case_next_dig_point'
    http_result = util.http_multiget([the_url])
    next_dig_point = util._int(util.json_loads(http_result.get(the_url, ''), ''), START_TAIPEI_CITY_ROAD_CASE)
    cfg.logger.debug('after http_multiget: http_result: %s next_dig_point: %s', http_result, next_dig_point)
    return {'next_dig_point': next_dig_point}


def _process_results(results):
    data = util.json_dumps(results.get('data', []))
    util.to_json(data, 'log.taipei_city_dig_point.json')

    cron.to_http_post(data)


def parse_args():
    ''' '''
    parser = argparse.ArgumentParser(description='roadpin_backend')
    parser.add_argument('-i', '--ini', type=str, required=True, help="ini filename")

    args = parser.parse_args()

    return (S_OK, args)


if __name__ == '__main__':
    (error_code, args) = parse_args()

    cfg.init({"ini_filename": args.ini})

    cron_taipei_city_road_case()
