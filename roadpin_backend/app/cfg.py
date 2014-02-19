# -*- coding: utf-8 -*-

import ConfigParser
import logging
import logging.config
import random
import math
import base64
import time
import pymongo
from pymongo import MongoClient
import ujson as json

_LOGGER_NAME = "app"
logger = None
config = {}
_EXPECTED_CONFIG_COLUMNS = []

_mongo_map = {
    'roadDB': 'roadCases',
    'cacheDB': 'cache',
    'reportDB': 'geo_report',
}

_ensure_index = {
    'roadDB': [('county_id', pymongo.ASCENDING), ('county_name', pymongo.ASCENDING), ('start_timestamp', pymongo.DESCENDING)]
}

def init(params):
    init_cfg(params)

def init_cfg(params):
    '''params: parameters from main.py, currently including port and ini_filename'''
    _init_logger(params['log_filename'])
    _init_ini_file(params['ini_filename'])
    _post_init_config(params)
    _post_json_config(config)
    _init_mongo()
    logger.info('config: %s', config)


def _init_mongo():
    global config
    global logger

    logger.warning('init_mongo: start')

    #config['MONGO_SERVER_URL'] = "mongodb://" + config.get('username') + ':' + config.get('password') + '@' + config.get('mongo_server_hostname') + "/" + config.get('mongo_server')
    config['MONGO_SERVER_URL'] = "mongodb://" + config.get('mongo_server_hostname') + "/" + config.get('mongo_server')
    try:
        config['mongoServer'] = MongoClient(config.get('MONGO_SERVER_URL'), use_greenlets=True)[config.get('mongo_server')]
        for (key, val) in _mongo_map.iteritems():
            logger.debug('mongo: %s => %s', key, val)
            config[key] = config.get('mongoServer')[val]
    except:
        logger.exception('')

        for (key, val) in _mongo_map.iteritems():
            config[key] = None

    for (key, val) in _ensure_index.iteritems():
        config[key].ensure_index(val)


def _init_logger(log_filename):
    '''logger'''
    global logger
    logger = logging.getLogger(_LOGGER_NAME)
    handler = logging.handlers.RotatingFileHandler(log_filename, maxBytes=100000000, backupCount=2)
    formatter = logging.Formatter('%(asctime)s [%(levelname)-5.5s] %(module)s#%(funcName)s@%(lineno)d: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)


def _init_ini_file(ini_file):
    '''...'''
    global config
    section = 'app:main'

    config_parser = ConfigParser.SafeConfigParser()
    config_parser.read(ini_file)
    options = config_parser.options(section)
    config = {option: __init_ini_file_parse_option(option, section, config_parser) for option in options}

def __init_ini_file_parse_option(option, section, config_parser):
    try:
        val = config_parser.get(section, option)
    except Exception as e:
        logger.warning(str(e))
        val = ''
    return val


def _post_init_config(params):
    '''...'''
    global config
    for k in params.keys():
        v = params[k]
        if k in config:
            logger.warning('params will be overwrite: key: %s origin: %s new: %s', k, config[k], v)
        config[k] = v

    
def _post_json_config(config):
    logger.debug('start: config: %s', config)
    for k, v in config.iteritems():
        if v.__class__.__name__ != 'str':
            continue

        orig_v = v
        try:
            config[k] = json.loads(v)
        except:
            config[k] = orig_v

    logger.debug('end: config: %s', config)
