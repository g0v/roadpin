# -*- coding: utf-8 -*-

import logging
import unittest
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
