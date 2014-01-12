# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR
import random
import math
import base64
import time
import ujson as json

from app import cfg
from app import util

from scrapy.item import Item, Field

class NewTaipeiCityItem(Item):
    # define the fields for your item here like:
    # name = Field()
    county_name  = Field()
    the_category = Field()
    the_idx      = Field()
    the_data     = Field()
    geo          = Field()
    start_timestamp = Field()
    end_timestamp   = Field()
