# -*- coding: utf-8 -*-

from app import util
from app.value_map import COUNTY_MAP

def set_county_name(results, county_name):
    county_id = COUNTY_MAP.get(county_name, '')
    for result in results:
        result['county_name'] = county_name
        result['county_id'] = county_id


def set_category(results, the_category):
    for result in results:
        result['the_category'] = the_category
