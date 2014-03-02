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
from app.crawlers.taipei_city import crawler_taipei_city_road_case

def cron_taipei_city_road_case():
    params = _get_params()

    cfg.logger.debug('params: %s', params)

    results = crawler_taipei_city_road_case.crawler_taipei_city_road_case(params)

    _process_results(results)


def _get_params():
    server = cfg.config.get('web_server', 'http://106.187.101.193:5346')
    the_url = server + '/get/taipei_city_road_case_next_road_case'
    http_result = util.http_multiget([the_url])
    next_road_case = util._int(util.json_loads(http_result.get(the_url, ''), ''), START_TAIPEI_CITY_ROAD_CASE)
    cfg.logger.debug('after http_multiget: http_result: %s next_road_case: %s', http_result, next_road_case)
    return {'next_road_case': next_road_case}


def _process_results(results):
    data = results.get('data', [])
    cron.to_http_post(data)

    util.to_json(util.json_dumps(data), 'log.taipei_city_road_case.json')

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
