# -*- coding: utf-8 -*-

import random
import math
import base64
import time
import ujson as json
import sys
from bottle import ServerAdapter
from gevent import Greenlet
from gevent import wsgi, pywsgi, local

from app import cfg

class GeventServer(ServerAdapter):
    """ Untested. Options:
        * `fast` (default: False) uses libevent's http server, but has some
          issues: No streaming, no pipelining, no SSL.
        * See gevent.wsgi.WSGIServer() documentation for more options.
    """
    def run(self, handler):
        if not self.options.pop('fast', None): wsgi = pywsgi
        self.options['log'] = sys.stdout if cfg.config.get('dologstdout', None) else None

        address = (self.host, self.port)
        wsgi.WSGIServer(address, handler, **self.options).serve_forever()
