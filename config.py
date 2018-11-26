#!/usr/bin/python

from oslo_config import cfg


opts = [
    cfg.StrOpt('bind_host', default='0.0.0.0'),
    cfg.IntOpt('bind_port', default=8000),
]


CONF = cfg.CONF
CONF.register_opts(opts)

if __name__ == '__main__':
    print CONF.bind_host
    print CONF.bind_port

