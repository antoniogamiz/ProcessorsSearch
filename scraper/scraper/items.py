# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader.processors import TakeFirst, MapCompose
import unicodedata

class ProcessorsItem(scrapy.Item):
    brand = scrapy.Field(
        input_processor=MapCompose(lambda s: re.search("(Intel|AMD)", s).group(0)),
        outpot_processor=TakeFirst(),
    )
    model = scrapy.Field(
        input_processor=MapCompose(lambda s: str(re.search("(Intel|AMD)(?P<model>.+)\d\.\dG[Hh][Zz]", s).group('model')).strip()),
        outpot_processor=TakeFirst(),
    )
    frequency=scrapy.Field(
        input_processor=MapCompose(lambda s: re.search("\d\.\dG[Hh][Zz]", s).group(0)),
        outpot_processor=TakeFirst(),
    )
    price=scrapy.Field()
    availability=scrapy.Field(
        input_processor=MapCompose(lambda s: str(re.search("(entre el |el )(?P<model>.+)", s.encode('ascii','ignore')).group('model')).strip()),
        outpot_processor=TakeFirst(),
    )
