Scrapy Sticky Meta
==================

Handy tools to maintain persistent meta values between requests in
Scrapy spiders. Available as spider middleware and spider callback
decorators.

Installation
------------

::

    pip install stickymeta

Usage
-----

As spider middleware
^^^^^^^^^^^^^^^^^^^^

Add middleware to ``settings.py``:

::

    SPIDER_MIDDLEWARES = {
        ...
        'stickymeta.StickyMetaMiddleware': 543,
        ...
    }

and ``sticky_meta`` attribute containing persistent ``meta`` keys to
spider:

::

    class TheSpider(scrapy.Spider):
        name = 'thespider'
        sticky_meta = ('cookiejar', 'foo', 'bar')

All values for the corresponding keys will be kept persistent between
all the requests and responses.

As decorators
^^^^^^^^^^^^^

@stick\_meta
''''''''''''

::

    from stickymeta import stick_meta

Keep persistent values for keys passed as decorator parameters:

::

    @stick_meta('a', 'b', 'c')
    def parse(self, response):
        ...
        yield scrapy.Request(url)
        

is equivalent to:

::

    def parse(self, response)
        ...
        meta = {
            'a': response.meta['a'],
            'b': response.meta['b'],
            'c': response.meta['c'],
        }
        yield scrapy.Request(url, meta=meta}
        

@stick\_cj
''''''''''

::

    from stickymeta import stick_cj

Shortcut for ``stick_meta`` handling ``cookiejar`` as default argument
value, so

::

    @stick_cj('a', 'b', 'c')
    def parse(self,response):
        ...
        

is equivalent to

::

    @stick_meta('cookiejar', 'a', 'b', 'c')
    def parse(self,response):
        ...
        

Spider attribute ``sticky_meta`` also affects to decorators, next two
pieces of code will handle ``meta`` in the same way:

::

    class TheSpider(scrapy.Spider):
        name = 'thespider'
        sticky_meta = ('a', 'b', 'c')
        
        @stick_meta()
        def parse(self, response):
            ...
            yield Request(url)
            

vs

::

    class TheSpider(scrapy.Spider):
        name = 'thespider'
        
        @stick_meta('a', 'b', 'c')
        def parse(self, response):
            ...
            yield Request(url)

