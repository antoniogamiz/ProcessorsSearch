# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader.processors import TakeFirst, Join, MapCompose

class ProcessorsItem(scrapy.Item):
    brand = scrapy.Field(
        input_processor=MapCompose(lambda s: re.search("(Intel|AMD)", s).group(0)),
        outpot_processor=Join(),
    )
    model = scrapy.Field(
        input_processor=MapCompose(lambda s: str(re.search("(Intel|AMD)(?P<model>.+)\d\.\dG[Hh][Zz]", s).group('model')).strip()),
        outpot_processor=Join(),
    )
    frequency=scrapy.Field(
        input_processor=MapCompose(lambda s: re.search("\d\.\dG[Hh][Zz]", s).group(0)),
        outpot_processor=Join(),
    )
    price=scrapy.Field()
