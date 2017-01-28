# -*- coding: utf-8 -*
from __future__ import absolute_import
import unittest
import scrapy
from scrapy.http import Response
from stickymeta.middlewares import StickyMetaMiddleware

__author__ = 'mikhail.kolganov@gmail.com'

URL = 'http://scrapytest.org/'


class MiddlewareTestCase(unittest.TestCase):
    class TestSpider(scrapy.Spider):
        sticky_meta = ('cookiejar',)

    def setUp(self):
        self.mw = StickyMetaMiddleware()
        self.spider = self.TestSpider('sticky')
        self.response = Response(URL, request=scrapy.Request(URL, meta={'cookiejar': 1}))

    def tearDown(self):
        del self.mw
        del self.spider

    def test_basic_output(self):
        out = list(self.mw.process_spider_output(self.response, [scrapy.Request(URL)], self.spider))
        self.assertEqual(out[0].meta['cookiejar'], 1)

    def test_no_sticky_output(self):
        out = list(self.mw.process_spider_output(self.response, [scrapy.Request(URL)], scrapy.Spider('foo')))
        self.assertEqual(out[0].meta.get('cookiejar', None), None)

    def test_overwrite_output(self):
        out = list(self.mw.process_spider_output(self.response, [scrapy.Request(URL, meta={'cookiejar': 2})], self.spider))
        self.assertEqual(out[0].meta['cookiejar'], 2)
