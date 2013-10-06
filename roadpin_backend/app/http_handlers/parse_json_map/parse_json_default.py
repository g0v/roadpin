# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR
import random
import math
import base64
import time
import ujson as json

from app import cfg
from app import util

def parse_json_default(data):
    data['town_name'] = ''
    data['location'] = ''
    data['work_institute'] = ''
    data['work_institute2'] = ''
