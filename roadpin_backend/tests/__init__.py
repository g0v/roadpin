import logging

from app import cfg

def setup():
    cfg.logger = logging
    cfg.config = {}
    pass

def teardown():
    pass
