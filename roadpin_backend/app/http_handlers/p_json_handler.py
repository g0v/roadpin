# -*- coding: utf-8 -*-

import random
import math
import base64
import time
import ujson as json

from app.constants import *
from app import cfg
from app import util

def p_json_handler(data):
    error_code = S_OK
    error_msg = ''

    save_timestamp = util.get_timestamp()

    for each_data in data:
        _infer_columns(each_data, save_timestamp)
        the_id = each_data['the_id']

        db_result = util.db_find_one('roadDB', {'the_id': the_id})
        if db_result:
            if not _is_same(db_result, each_data):
                error_code = S_ERR
                cfg.logger.error('data different: the_id: %s db_result: %s each_data: %s', the_id, db_result, each_data)
                error_msg += 'data different: the_id: %s db_result: %s each_data: %s\n' % (the_id, db_result, each_data)
            continue

        util.db_insert_if_not_exist('roadDB', {'the_id': the_id}, each_data)

    return {"success": True if error_code == S_OK else False, "error_msg": error_msg}


def _infer_columns(data, save_timestamp):
    data['the_id'] = data.get('the_category', '') + '_' + data.get('the_idx', '')

    start_timestamp = util._int(data.get('start_timestamp', 0))
    data['beginDate'] = '' if not start_timestamp else util.timestamp_to_date_str(start_timestamp, 'Asia/Taipei')

    end_timestamp = util._int(data.get('end_timestamp', 0))
    data['endDate'] = '' if not end_timestamp or end_timestamp >= MAX_TIMESTAMP else util.timestamp_to_date_str(end_timestamp, 'Asia/Taipei')


def _is_same(db_result, data):
    if data.__class__.__name__ == 'dict':
        if db_result.__class__.__name__ != 'dict':
            return False

        for (key, val) in data.iteritems():
            if key not in db_result:
                return False

            if not _is_same(db_result[key], val):
                return False

        return True
    elif data.__class__.__name__ == 'list':
        if db_result.__class__.__name__ != 'list':
            return False

        for (idx, val) in enumerate(data):
            if len(db_result) <= idx:
                return False

            if not _is_same(db_result[idx], val):
                return False

        return True
    else:
        return db_result == data

    return True
