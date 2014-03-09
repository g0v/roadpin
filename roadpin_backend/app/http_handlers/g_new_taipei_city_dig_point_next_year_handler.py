# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR
import random
import math
import base64
import time
import ujson as json
import pymongo

from app.constants import *

from app import cfg
from app import util

def g_new_taipei_city_dig_point_next_year_handler():
    db_results = util.db_find_it('roadDB', {'the_category': 'new_taipei_city_dig_point'}, {'_id': False, 'end_timestamp': True})
    if not db_results:
        return START_NEW_TAIPEI_CITY_DIG_POINT_YEAR

    db_result = db_results.sort('end_timestamp', pymongo.DESCENDING).limit(1)

    if not db_result:
        return START_NEW_TAIPEI_CITY_DIG_POINT_YEAR


    result_list = list(db_result)

    if not result_list:
        return START_NEW_TAIPEI_CITY_DIG_POINT_YEAR

    result = result_list[0]

    end_timestamp = result.get('end_timestamp', MAX_TIMESTAMP) #1000.0
    end_datetime = util.timestamp_to_datetime(end_timestamp)
    the_year = end_datetime.year

    return the_year
