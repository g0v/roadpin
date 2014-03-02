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

def g_taipei_city_road_case_next_road_case_handler():
    db_results = util.db_find_it('roadDB', {'the_category': 'taipei_city_road_case'}, {'_id': False, 'the_idx': True})
    if not db_results:
        return START_TAIPEI_CITY_ROAD_CASE
    
    db_result = db_results.sort('the_idx', pymongo.DESCENDING).limit(1)

    if not db_result:
        return START_TAIPEI_CITY_ROAD_CASE

    result_list = list(db_result)

    if not result_list:
        return START_TAIPEI_CITY_ROAD_CASE

    result = result_list[0]

    the_idx = result.get('the_idx', START_TAIPEI_CITY_ROAD_CASE) #1000.0
    the_idx = util._int(util._float(the_idx) // 1)

    return util._int(the_idx)
