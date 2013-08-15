#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
from urllib import urlencode

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request, FormRequest
from kaohsiung.items import KaohsiungItem

class KaohsiungSpider(CrawlSpider):
    name = 'kaohsiung'
    allowed_domains = ['pipegis.kcg.gov.tw']

    rules = [
            Rule(SgmlLinkExtractor(
                allow = ('default.aspx\?a=c.*')),
                follow = True,
                callback = 'parse_list'),
    ]

    county_name = u'高雄市'

    def __init__(self):
        self.start_urls = ['http://pipegis.kcg.gov.tw/default.aspx?a=c&id=-1&type=0&page=1']

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
            item = KaohsiungItem()
            item['county_name']  = self.county_name
            item['the_category'] = ''
            item['the_idx'] = fields[6]
            ts = re.findall('(\d+)', fields[7])
            item['start_timestamp'] = ts[0]
            item['end_timestamp']   = ts[1]
            item['the_data'] = ';'.join(fields)
            yield item

        # Traverse
        items = hxs.select("//div[@id='pagenate']/a/@href")
        for item in items:
            url = 'http://pipegis.kcg.gov.tw/' + re.findall("(default[^']+)", item.extract())[0]
            yield Request(url,
                    callback=self.parse_list,
                    errback=self.errback)

    def errback(self):
        self.log('Request failed')
