# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR
import random
import math
import base64
import time
import ujson as json

from app.constants import EARTH_EQUATOIAL_CIRCUMFERENCE, EARTH_MERIDIONAL_CIRCUMFERENCE

from app import cfg
from app import util

def g_search_by_location_handler(params):
    lat = util._float(params.get('lat', 25))
    lon = util._float(params.get('lng', 121))

    dist = util._float(params.get('distance', 10))
    dist = max(dist, 10.0)

    dist_x = 360.0 * dist / EARTH_EQUATOIAL_CIRCUMFERENCE
    dist_y = 360.0 * dist / EARTH_MERIDIONAL_CIRCUMFERENCE

    min_x = lon - dist_x
    max_x = lon + dist_x
    min_y = lat - dist_y
    max_y = lat + dist_y

    query = {'geo': {'$geoIntersects': {'$geometry': {'type': 'Polygon', 'coordinates': [[[min_x, min_y], [min_x, max_y], [max_x, max_y], [max_x, min_y], [min_x, min_y]]]}}}}

    cfg.logger.debug('dist: %s dist_x: %s dist_y: %s to db_find: query: %s', dist, dist_x, dist_y, query)

    results = util.db_find('roadDB', query)
    for result in results:
        del result['_id']
    cfg.logger.debug('results: % len: %s', results, len(results))
    return results
