#!/usr/bin/python

import os
import logging
from oslo_config import cfg
from paste.deploy import loadapp
from wsgiref.simple_server import make_server
from webob import Response

CONF = cfg.CONF

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(pathname)s - %(filename)s - %(funcName)s - %(lineno)d '
                              '- %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class ShowVersion(object):
    def __init__(self, version):
        self.version = version

    def __call__(self, environ, start_response):
        res = Response()
        res.status = '200 OK'
        res.content_type = "text/plain"
        content = []
        content.append("Version is %s\n" % self.version)
        res.body = '\n'.join(content)
        return res(environ, start_response)

    @classmethod
    def factory(cls, global_conf, **kwargs):
        return ShowVersion(kwargs['version'])


class LogFilter(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        logger.info('now in the LogFilter.  ')
        return self.app(environ, start_response)

    @classmethod
    def factory(cls, global_conf, **kwargs):
        return LogFilter


if __name__ == '__main__':
    config = "python_paste.ini"
    appname = "common"
    wsgi_app = loadapp("config:%s" % os.path.abspath(config), appname)
    server = make_server(CONF.bind_host, CONF.bind_port, wsgi_app)
    server.serve_forever()
