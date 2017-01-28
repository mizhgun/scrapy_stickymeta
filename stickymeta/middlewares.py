# -*- coding: utf-8 -*
from __future__ import absolute_import
from .decorators import sticky_passthrough

__author__ = 'mikhail.kolganov@gmail.com'


class StickyMetaMiddleware(object):
    def process_spider_output(self, response, result, spider):
        if getattr(spider, 'sticky_meta', None) is None:
            return result
        return sticky_passthrough(spider, response, lambda *args, **kwargs: result, (), None)
