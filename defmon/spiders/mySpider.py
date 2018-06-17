# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from defmon.items import DefmonItem
from hashlib import md5
import datetime

class mySpider(CrawlSpider):
    name = 'mySpider'
    rules = (
            Rule(LinkExtractor(), callback='parse_start_url', follow=True),
            )

    def __init__(self, *a, **kw):
        super(mySpider, self).__init__(*a, **kw)
        self.allowed_domains = [kw.get('domain')]
        self.start_urls = [kw.get('start_url')]

    def parse_start_url(self, response):
        item = DefmonItem()
        item['link'] = response.request.url
        item['message'] = response.body
        item['md5'] = self.make_md5(response.body)
        item['timestamp'] = datetime.datetime.now()

        yield item

    def make_md5(self, s, encoding='utf-8'):
         return md5(s).hexdigest()
