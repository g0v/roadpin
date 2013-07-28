# -*- coding: utf-8 -*-

import logging
import unittest
from app.cron_data import cron_taipei_city

class TestCronTaipeiCity(unittest.TestCase):
    '''unit tests for cron_taipei_city'''

    def setUp(self):
        '''setup for all the tests'''
        logging.info('setup')
        self.____never_used_variable = 1

    def tearDown(self):
        '''teardown for all the tests'''
        logging.info("teardown")

    def test_cron_taipei_city_true(self):
        '''True should not assert.'''
        assert True

    def test_bottle_tmp_never_used_variable_as_1(self):
        '''a == 1 should not assert.'''
        logging.info("test_bottle_tmp: test_bottle_tmp_true")
        assert self.____never_used_variable == 1

    def test__parse_geo(self):
        the_data = {
            'dtResultpro': [
                {'GEO_TYPE': None,
                 'POINTS': [
                     {'P1': 121.53275726071669,
                      'P2': 25.101171798153032},
                     {'P1': 121.5329732086012,
                      'P2': 25.1011710222917}]},
                {'GEO_TYPE': 'Polygon',
                 'POINTS': [
                     {'P1': 121.52826916840115,
                      'P2': 25.018342943987733},
                     {'P1': 121.52885968944659,
                      'P2': 25.018868265169033}]}]}
        
        result = cron_taipei_city._parse_geo(the_data)
        logging.debug('result: %s', result)
        assert len(result) == 2
        assert result[0]['type'] == 'LineString'
        assert len(result[0]['coordinates']) == 2
        assert result[0]['coordinates'][0][0] == 121.53275726071669
        assert result[0]['coordinates'][0][1] == 25.101171798153032
        assert result[0]['coordinates'][1][0] == 121.5329732086012
        assert result[0]['coordinates'][1][1] == 25.1011710222917

        assert result[1]['type'] == 'LineString'
        assert len(result[1]['coordinates']) == 2
        assert result[1]['coordinates'][0][0] == 121.52826916840115
        assert result[1]['coordinates'][0][1] == 25.018342943987733
        assert result[1]['coordinates'][1][0] == 121.52885968944659
        assert result[1]['coordinates'][1][1] == 25.018868265169033
