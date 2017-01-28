# -*- coding: utf-8 -*
from __future__ import absolute_import
from scrapy import Request
from scrapy.utils.misc import arg_to_iter

__author__ = 'mikhail.kolganov@gmail.com'


def sticky_passthrough(spider, response, func, sticky_args, *args, **kwargs):
    meta_keys = set(list(sticky_args) + list(getattr(spider, 'sticky_meta', [])))
    sticky = {k: v for k, v in response.meta.items() if k in meta_keys}
    f = func(spider, response, *args, **kwargs)
    for r in arg_to_iter(f):
        if sticky and isinstance(r, Request):
            r.meta.update({k: v for k, v in sticky.items() if k not in r.meta.keys()})
        yield r


def stick_meta(*meta_keys):
    def dec(func):

        def wrapper(spider, response, *args, **kwargs):
            return sticky_passthrough(spider, response, func, meta_keys, *args, **kwargs)

        return wrapper

    return dec


def stick_cj(*extra_meta_keys):
    return stick_meta('cookiejar', *extra_meta_keys)
