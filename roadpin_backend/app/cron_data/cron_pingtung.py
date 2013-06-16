# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR

import random
import math
import base64
import time
import ujson as json

import sys
import argparse

from app import cfg
from app import util

def cron_pingtung():
    pass

def parse_args():
    ''' '''
    parser = argparse.ArgumentParser(description='roadpin_backend')
    parser.add_argument('-i', '--ini', type=str, required=True, help="ini filename")

    args = parser.parse_args()

    return (S_OK, args)


if __name__ == '__main__':
    (error_code, args) = parse_args()

    cfg.init({"ini_filename": args.ini})

    cron_pingtung()

