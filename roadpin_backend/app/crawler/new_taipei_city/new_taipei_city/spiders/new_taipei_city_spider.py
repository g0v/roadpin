# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR
import random
import math
import base64
import time
import ujson as json
import re
from urllib import urlencode

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request, FormRequest
from app.crawler.new_taipei_city.new_taipei_city.items import NewTaipeiCityItem

from app import cfg
from app import util

class NewTaipeiCitySpider(CrawlSpider):
    name = 'new_taipei_city'
    allowed_domains = ['61.60.124.185']

    rules = [
            Rule(SgmlLinkExtractor(
                allow = ('InfoAllList.asp\?a=c.*')),
                follow = True,
                callback = 'parse_list'),
    ]

    county_name = u'新北市'

    def __init__(self):
        self.start_urls = ['http://61.60.124.185/tpctempdig/InfoAllList.asp']

        super(CrawlSpider, self).__init__()
        self._compile_rules()

    def parse_list(self, response):
        self.log('crawl: %s' % response.url)
        hxs = HtmlXPathSelector(response)

        # Get data
        records = hxs.select("//div[@class='tabs_content']//tr")
        for r in records:
            fields = r.select('.//td/text()').extract()
            if not fields:
                continue

            cfg.logger.debug('fields: %s', fields)
            data_dict = self._process_data_dict(fields, _columns)
            item = NewTaipeiCityItem()
            item['county_name']  = self.county_name
            item['the_category'] = 'kaohsiung_dig_point'
            item['the_idx'] = fields[6]
            ts = re.findall('(\d+)', fields[7])
            item['start_timestamp'] = ts[0]
            item['end_timestamp']   = ts[1]
            item['the_data'] = data_dict
            
            item['start_timestamp'] = util.tw_date_to_timestamp(item['start_timestamp'])
            item['end_timestamp'] = util.tw_date_to_timestamp(item['end_timestamp'])

            process_data(item['county_name'], item['the_category'], item['the_idx'], item['start_timestamp'], item['end_timestamp'], {}, item['the_data'])

            yield item

        # Traverse
        items = hxs.select("//div[@id='pagenate']/a/@href")
        for item in items:
            url = 'http://pipegis.kcg.gov.tw/' + re.findall("(default[^']+)", item.extract())[0]
            yield Request(url,
                          callback=self.parse_list,
                          method='POST',
                          errback=self.errback)

    def errback(self):
        self.log('Request failed')

    def _process_data_dict(self, fields, columns):
        result = {column: '' if idx >= len(fields) else fields[idx] for (idx, column) in enumerate(columns)}
        return result
