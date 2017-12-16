# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProcessorsItem(scrapy.Item):
    brand = scrapy.Field()
    model = scrapy.Field()
    frequency=scrapy.Field()
    price=scrapy.Field()
