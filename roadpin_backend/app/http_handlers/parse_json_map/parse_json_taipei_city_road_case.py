# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR
import random
import math
import base64
import time
import ujson as json

from app import cfg
from app import util

def parse_json_taipei_city_road_case(data):
    '''
    add 1 town name 2. location. 3. range. 4. work_institute. 5. work_institute2
    '''
    data['town_name'] = data.get('extension', {}).get('REG_NAMEpro', '')
    data['location'] = data.get('extension', {}).get('CASE_LOCATIONpro', '')
    data['range'] = data.get('extension', {}).get('CASE_RANGEpro', '')
    data['work_institute'] = data.get('extension', {}).get('CTR_WNAMEpro', '')
    data['work_institute2'] = data.get('extension', {}).get('CTR_ONAMEpro', '')
