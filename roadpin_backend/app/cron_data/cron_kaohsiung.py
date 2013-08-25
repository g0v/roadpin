# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR

import random
import math
import base64
import time
import ujson as json

import sys
import argparse

from twisted.internet import reactor

from scrapy import log, signals
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy.xlib.pydispatch import dispatcher

from app import cfg
from app import util
from app.crawler.kaohsiung.kaohsiung.spiders.kaohsiung_spider import KaohsiungSpider
from app.cron_data import cron_taipei_city

def stop_reactor():
    reactor.stop()


def cron_kaohsiung():
    while True:
        _cron_kaohsiung()
        cron_taipei_city.sleep()


def _cron_kaohsiung():
    dispatcher.connect(stop_reactor, signal=signals.spider_closed)
    spider = KaohsiungSpider()
    crawler = Crawler(Settings())
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    log.start()
    log.msg('Running reactor...')
    reactor.run()  # the script will block here until the spider is closed
    log.msg('Reactor stopped.')


def parse_args():
    ''' '''
    parser = argparse.ArgumentParser(description='roadpin_backend')
    parser.add_argument('-i', '--ini', type=str, required=True, help="ini filename")

    args = parser.parse_args()

    return (S_OK, args)


if __name__ == '__main__':
    (error_code, args) = parse_args()

    cfg.init({"ini_filename": args.ini})

    cron_kaohsiung()
