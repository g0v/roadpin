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
from app import util

app = Bottle()

@app.get('/get_json_by_date')
def g_json_by_date():
    params = dict(request.params)
    start_timestamp = util.date_to_timestamp(params['begin_at'])
    end_timestamp = util.date_to_timestamp(params['end_at'])
    return util.json_dumps(g_json_handler(start_timestamp, end_timestamp))

@app.get('/get_json_by_timestamp/<start_timestamp>/<end_timestamp>')
def g_json_by_timestamp(start_timestamp, end_timestamp):
    return util.json_dumps(g_json_handler(start_timestamp, end_timestamp))

@app.get('/get_json_by_geo/<latitude>/<longtitude>')
def g_json_by_geo(latitude, longtitude):
    return util.json_dumps(g_json_by_geo_handler(latitude, longtitude))

@app.post('/post_json/<src>')
def p_json(src):
    params = dict(request.params)
    return util.json_dumps(p_json_handler(src, params))


def parse_args():
    ''' '''
    parser = argparse.ArgumentParser(description='rtbbidder-frontend-aggregator')
    parser.add_argument('-i', '--ini', type=str, required=True, help="ini filename")
    parser.add_argument('-p', '--port', type=str, required=True, help="port")
    parser.add_argument('-u', '--username', type=str, required=True, help="username")
    parser.add_argument('--password', type=str, required=True, help="password")

    args = parser.parse_args()

    return (S_OK, args)



if __name__ == '__main__':
    (error_code, args) = parse_args()

    cfg.init({"port": args.port, "ini_filename": args.ini, 'username': args.username, 'password': args.password})

    run(app, host='0.0.0.0', port=cfg.config.get('port'), server=GeventServer)
