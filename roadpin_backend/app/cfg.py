# -*- coding: utf-8 -*-

import ConfigParser
import logging
import logging.config
import random
import math
import base64
import time
from pymongo import MongoClient
import ujson as json

_LOGGER_NAME = "app"
logger = None
config = {}
_EXPECTED_CONFIG_COLUMNS = []

_mongo_map = {
    'roadDB': 'roadCases'
}

def init(params):
    init_cfg(params)

def init_cfg(params):
    '''params: parameters from main.py, currently including port and ini_filename'''
    _init_logger(params['ini_filename'])
    _init_ini_file(params['ini_filename'])
    _post_init_config(params)
    _post_check_config()
    _init_mongo()
    logger.info('config: %s', config)


def _init_mongo():
    global config
    global logger

    logger.warning('init_mongo: start')

    #config['MONGO_SERVER_URL'] = "mongodb://" + config.get('username') + ':' + config.get('password') + '@' + config.get('mongo_server_hostname') + "/" + config.get('mongo_server')
    config['MONGO_SERVER_URL'] = "mongodb://" + config.get('mongo_server_hostname') + "/" + config.get('mongo_server')
    try:
        config['mongoServer'] = MongoClient(config.get('MONGO_SERVER_URL'))[config.get('mongo_server')]
        for (key, val) in _mongo_map.iteritems():
            logger.warning('mongo: %s => %s', key, val)
            config[key] = config.get('mongoServer')[val]
    except:
        logger.exception('')

        for (key, val) in _mongo_map.iteritems():
            config[key] = None


def _init_logger(ini_file):
    '''logger'''
    global logger
    logger = logging.getLogger(_LOGGER_NAME)
    logging.config.fileConfig(ini_file, disable_existing_loggers=False)


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

    
def _post_check_config():
    '''ensure _EXPECTED_CONFIG_COLUMNS is set. raise error if some is not set'''
    for k in _EXPECTED_CONFIG_COLUMNS:
        config[k]
    
