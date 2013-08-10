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
    the_timestamp = util.get_milli_timestamp()
    user_id = params.get('user_id', '')
    data = params.get('data', [])
    for each_data in data:
        _process_each_data(user_id, each_data, the_timestamp)


def _process_each_data(user_id, each_data, server_timestamp):
    offset_timestamp = util._int(each_data.get('offset_timestamp', 0))
    lat = each_data.get('lat', 0)
    lon = each_data.get('lon', 0)
    yaw = each_data.get('yaw', 0)
    pitch = each_data.get('pitch', 0)
    roll = each_data.get('roll', 0)
    x = each_data.get('x', 0)
    y = each_data.get('y', 0)
    z = each_data.get('z', 0)

    the_timestamp = server_timestamp + offset_timestamp

    key = {'user_id': user_id, 'the_timestamp': the_timestamp}
    val = {'lat': lat, 'lon': lon, 'yaw': yaw, 'pitch': pitch, 'roll': roll, 'x': x, 'y': y, 'z': z}


    cfg.logger.debug('to db_update reportDB: server_timestamp: %s offset_timestamp: %s the_timestamp: %s', server_timestamp, offset_timestamp, the_timestamp)

    util.db_update('reportDB', key, val)

    return {'success': True}
