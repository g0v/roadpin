# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR
import random
import math
import base64
import time
import ujson as json

from app import cfg
from app import util

def p_geo_handler(params):
    the_timestamp = util.get_timestamp()
    user_id = params.get('user_id', '')
    lat = params.get('lat', 0)
    lon = params.get('lon', 0)
    yaw = params.get('yaw', 0)
    pitch = params.get('pitch', 0)
    roll = params.get('roll', 0)
    x = params.get('x', 0)
    y = params.get('y', 0)
    z = params.get('z', 0)

    key = {'user_id': user_id, 'the_timestamp': the_timestamp}
    val = {'lat': lat, 'lon': lon, 'yaw': yaw, 'pitch': pitch, 'roll': roll, 'x': x, 'y': y, 'z': z}

    util.db_update('reportDB', key, val)

    return {'success': True}
