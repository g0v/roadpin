# -*- coding: utf-8 -*-
import re

from app.constants import *
import random
import math
import base64
import time
import ujson as json

from app import cfg
from app import util

def validate_http_result_json(result):
    if not result:
        return S_ERR

    if result.__class__.__name__ != 'dict' and result.__class__.__name__ != 'list':
        return S_ERR

    if result == '-1':
        return S_ERR

    if result == '-2':
        return S_ERR

    return S_OK


def parse_time_period(time_period):
    try:
        time_period = re.sub(ur'/', '', time_period)
    except:
        cfg.logger.error('unable to re.sub time_period: time_period: (%s, %s)', time_period, time_period.__class__.__name__)
        time_period = '~'

    time_period_split = time_period.split('~')
    if len(time_period_split) != 2:
        return (0, MAX_TIMESTAMP)

    start_tw_date = time_period_split[0]
    end_tw_date = time_period_split[1]
    (start_tw_date, end_tw_date) = time_period.split('~')
    start_timestamp = util.tw_date_to_timestamp(start_tw_date)
    end_timestamp = util.tw_date_to_timestamp(end_tw_date)
    if not end_timestamp:
        end_timestamp = MAX_TIMESTAMP
    return (start_timestamp, end_timestamp)


def parse_geo(geo_list):
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
