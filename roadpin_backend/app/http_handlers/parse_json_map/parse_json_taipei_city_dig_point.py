# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR
import random
import math
import base64
import time
import ujson as json

from app import cfg
from app import util

def parse_json_taipei_city_dig_point(data):
    '''
    add 1 town name 2. location. 3. range. 4. work_institute. 5. work_institute2
    '''
    data['town_name'] = data.get('extension', {}).get('C_NAMEpro', '')
    data['town_name'] = '' if not data['town_name'] else data['town_name'] + u'區'
    data['location'] = data.get('extension', {}).get('LOCATIONpro', '')
    data['range'] = ''
    data['work_institute'] = data.get('extension', {}).get('TC_NApro', '')
    data['work_institute2'] = data.get('extension', {}).get('APP_NAMEpro', '')
    data['geo'] = _parse_geo_list(data.get('extension', {}).get('dtResultpro', []))


def _parse_geo_list(geo_list):
    return [_parse_geo(geo) for geo in geo_list]


def _parse_geo(geo):
    points = geo.get('POINTS', [])
    return {
        'type': 'Line',
        'data': [_parse_point(point) for point in points]
    }
    pass


def _parse_point(point):
    return {'lat': point.get('P2', 0.0), 'lon': point.get('P1', 0.0)}
