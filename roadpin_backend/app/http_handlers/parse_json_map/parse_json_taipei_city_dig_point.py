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
