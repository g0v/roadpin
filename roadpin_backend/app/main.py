#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app.constants import S_OK, S_ERR

import gevent.monkey; gevent.monkey.patch_all()
from bottle import Bottle, request, response, route, run, post, get, static_file, redirect, HTTPError, view, template

import random
import math
import base64
import time
import ujson as json
import sys
import argparse

from app import cfg
from app.gevent_server import GeventServer
from app.http_handlers.g_json_handler import g_json_handler
from app.http_handlers.p_json_handler import p_json_handler
from app.http_handlers.g_json_by_geo_handler import g_json_by_geo_handler
from app.http_handlers.post_add_handler import post_add_handler
from app.http_handlers.g_search_by_location_handler import g_search_by_location_handler
from app.http_handlers.p_geo_handler import p_geo_handler

from app import util

app = Bottle()


@app.get('/')
def g_index():
    return static_file('index.html', root='.')


@app.get('/get_json_today')
def g_json_by_today():
    today = util.date_today()
    tomorrow = util.date_tomorrow()
    cfg.logger.debug("today: %s tomorrow: %s", today, tomorrow)
    start_timestamp = util.date_to_timestamp(today)
    end_timestamp = util.date_to_timestamp(tomorrow)
    return _process_result(g_json_handler(start_timestamp, end_timestamp))


@app.get('/get_json_by_date')
def g_json_by_date():
    params = dict(request.params)
    start_timestamp = util.date_to_timestamp(params['begin_at'])
    end_timestamp = util.date_to_timestamp(params['end_at'])
    return _process_result(g_json_handler(start_timestamp, end_timestamp))


@app.get('/get_json_by_timestamp/<start_timestamp>/<end_timestamp>')
def g_json_by_timestamp(start_timestamp, end_timestamp):
    return _process_result(g_json_handler(start_timestamp, end_timestamp))


@app.get('/get_json_by_geo/<latitude>/<longtitude>')
def g_json_by_geo(latitude, longtitude):
    return _process_result(g_json_by_geo_handler(latitude, longtitude))


@app.post('/add')
def post_add():
    params = dict(request.params)
    (error_code, error_msg) = util.check_url(params)
    if error_code != S_OK: 
        return _process_result(error_msg)

    (error_code, result) = post_add_handler(params)

    return _process_result(result)


@app.post('/post_json/<src>')
def p_json(src):
    params = dict(request.params)
    return _process_result(p_json_handler(src, params))


@app.get('/post_geo')
def p_geo():
    params = dict(request.params)
    return _process_result(p_geo_handler(params))


@app.get('/search_by_location')
def g_search_by_location():
    params = dict(request.params)
    return _process_result(g_search_by_location_handler(params))


def _process_result(the_obj):
    response.set_header('Access-Control-Allow-Origin', '*')
    response.set_header('Access-Control-Allow-Methods', '*')
    return util.json_dumps(the_obj)


def parse_args():
    ''' '''
    parser = argparse.ArgumentParser(description='roadpin_backend')
    parser.add_argument('-i', '--ini', type=str, required=True, help="ini filename")
    parser.add_argument('-p', '--port', type=str, required=True, help="port")
    parser.add_argument('-u', '--username', type=str, required=False, help="username")
    parser.add_argument('--password', type=str, required=False, help="password")

    args = parser.parse_args()

    return (S_OK, args)


if __name__ == '__main__':
    (error_code, args) = parse_args()

    username = '' if not hasattr(args, 'username') else args.username
    password = '' if not hasattr(args, 'password') else args.password
    cfg.init({"port": args.port, "ini_filename": args.ini, 'username': '', 'password': ''})

    run(app, host='0.0.0.0', port=cfg.config.get('port'), server=GeventServer)
