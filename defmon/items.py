# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class DefmonItem(scrapy.Item):
    link = scrapy.Field()
    message  = scrapy.Field()
    md5 = scrapy.Field()
    timestamp = scrapy.Field()
