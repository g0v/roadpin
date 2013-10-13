# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR
import random
import math
import base64
import time
import ujson as json

from app import cfg
from app import util

def parse_json_kaohsiung_dig_point(data):
    '''
    add 1 town name 2. location. 3. range. 4. work_institute. 5. work_institute2
    '''
    data['town_name'] = data.get('extension', {}).get('district', '')
    data['location'] = data.get('extension', {}).get('work_location', '')
    data['range'] = ''
    data['work_institute'] = data.get('extension', {}).get('apply_unit', '')
    data['work_institute2'] = ''
    data['geo'] = []

    if 'extension' in data:
        del data['extension']
