# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR

import random
import math
import base64
import time
import ujson as json

import sys
import argparse

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

    cron_new_taipei_city()

