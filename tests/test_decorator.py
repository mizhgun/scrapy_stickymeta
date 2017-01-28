# -*- coding: utf-8 -*
from __future__ import absolute_import
import unittest
from scrapy.http import Request, Response
from stickymeta.decorators import stick_meta, stick_cj

__author__ = 'mikhail.kolganov@gmail.com'

URL = 'http://scrapytest.org/'


class DecoratorArgumentsTestCase(unittest.TestCase):
    class TestSpider(object):
        @stick_meta('cookiejar')
        def parse(self, response):
            return Request(URL)

        @stick_meta()
        def parse_empty(self, response):
            return Request(URL)

        @stick_meta('cookiejar')
        def parse_overwrite(self, response):
            return Request(URL, meta={'cookiejar': 2})

    def setUp(self):
        self.response = Response(URL, request=Request(URL, meta={'cookiejar': 1}))
        self.spider = self.TestSpider()

    def tearDown(self):
        del self.response
        del self.spider

    def test_basic(self):
        for r in self.spider.parse(self.response):
            self.assertEqual(r.meta.get('cookiejar', None), 1)

    def test_empty(self):
        for r in self.spider.parse_empty(self.response):
            self.assertEqual(r.meta, {})

    def test_overwrite(self):
        for r in self.spider.parse_overwrite(self.response):
            self.assertEqual(r.meta.get('cookiejar', None), 2)


class CookieDecoratorArgumentsTestCase(DecoratorArgumentsTestCase):
    class TestSpider(object):
        @stick_cj()
        def parse(self, response):
            return Request(URL)

        @stick_cj()
        def parse_overwrite(self, response):
            return Request(URL, meta={'cookiejar': 2})

    @unittest.skip
    def test_empty(self):
        pass


class DecoratorSpiderPropertyTestCase(unittest.TestCase):
    class TestSpider(object):
        sticky_meta = ('cookiejar',)

        @stick_meta()
        def parse(self, response):
            return Request(URL)

        @stick_meta()
        def parse_overwrite(self, response):
            return Request(URL, meta={'cookiejar': 2})

    def setUp(self):
        self.response = Response(URL, request=Request(URL, meta={'cookiejar': 1}))
        self.spider = self.TestSpider()

    def tearDown(self):
        del self.response
        del self.spider

    def test_basic(self):
        for r in self.spider.parse(self.response):
            self.assertEqual(r.meta.get('cookiejar', None), 1)

    def test_overwrite(self):
        for r in self.spider.parse_overwrite(self.response):
            self.assertEqual(r.meta.get('cookiejar', None), 2)


if __name__ == '__main__':
    unittest.main()
