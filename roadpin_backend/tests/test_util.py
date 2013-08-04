# -*- coding: utf-8 -*-

from app.constants import S_OK

import logging
import unittest
from app import cfg
from app import util

class TestUtil(unittest.TestCase):
    '''unit tests for util'''

    def setUp(self):
        '''setup for all the tests'''
        logging.info('setup')
        self.____never_used_variable = 1

    def tearDown(self):
        '''teardown for all the tests'''
        logging.info("teardown")

    def test_util_true(self):
        '''True should not assert.'''
        assert True

    def test_bottle_tmp_never_used_variable_as_1(self):
        '''a == 1 should not assert.'''
        logging.info("test_bottle_tmp: test_bottle_tmp_true")
        assert self.____never_used_variable == 1

    def test_big5_to_utf8(self):
        result = util.big5_to_utf8('test')
        logging.debug('result: (%s, %s)', result, result.__class__.__name__)
        assert result == 'test'

        result_big5 = util.utf8_to_big5(u'我')
        logging.debug('result_big5: (%s, %s)', result_big5, result_big5.__class__.__name__)
        result = util.big5_to_utf8(result_big5)
        logging.debug('result: (%s, %s)', result, result.__class__.__name__)
        assert result == u'我'

    def test_tw_date_to_timestamp(self):
        result = util.tw_date_to_timestamp(1000131)
        logging.warning('test_tw_date_to_timestamp: result: %s', result)
        assert result == 1296403200

    def test_check_url(self):
        cfg.config['secret_key'] = 'test_secret'
        params = {'json': '{"test_json":"test_json2"}', 'sig': 'd7f5515058fcda6b06ddd56f929f0bc7'}
        (error_code, result) = util.check_url(params)
        assert error_code == S_OK
