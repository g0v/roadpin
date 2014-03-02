# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR
import random
import math
import base64
import time
import ujson as json

from app.constants import *
from app import cfg
from app import util

def to_http_post(data):
    path = '/post_json'

    len_data = len(data)
    for idx in range(0, len_data, N_DATA_TO_SERVER):
        end_idx = min(idx + N_DATA_TO_SERVER, len_data)
        each_data = data[idx:end_idx]

        _http_post(each_data, path, idx)


def _http_post(data, path, idx):
    server = cfg.config.get('web_server', 'http://106.187.101.193:5346')
    the_url = server + path

    data_json = util.json_dumps(data)

    cfg.logger.debug('to http_multipost: idx: %s the_url: %s data_json: %s', idx, the_url, data_json)

    http_result = util.http_multipost({the_url: data_json}, timeout=None)
    cfg.logger.debug('http_result: %s', http_result)
