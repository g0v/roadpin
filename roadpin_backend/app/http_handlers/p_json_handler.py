# -*- coding: utf-8 -*-

import random
import math
import base64
import time
import ujson as json

_parse_json_map = {
}


def p_json_handler(src, params):
    if src not in _parse_json_map:
        return {"result":False}
    
    _parse_json_map[src](src, params)
    
    return {"result":True}
