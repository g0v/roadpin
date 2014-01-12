# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR
import random
import math
import base64
import time
import ujson as json
import re

from app import cfg
from app import util

def parse_json_new_taipei_city_dig_point(data):
    data['town_name'] = re.sub(u'區.*', u'區', data.get('extension', {}).get('LOCATIONpro', ''))
    data['location'] = data.get('extension', {}).get('LOCATIONpro', '')
    data['range'] = ''
    data['work_institute'] = data.get('extension', {}).get('APP_NAMEpro', '')
    data['work_institute2'] = ''
    data['geo'] = []
    if 'extension' in data:
        del data['extension']
