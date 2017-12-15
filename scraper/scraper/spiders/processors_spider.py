# -*- coding: utf-8 -*-
import scrapy

class ProcessorsSpider(scrapy.Spider):
    name = "processors"
    start_urls = [
        "https://www.pccomponentes.com/procesadores/",
    ]

    def parse(self, response):
        for href in response.xpath("//a"):    # Analizamos cada post de una página.
            yield {
                "funciona" : "dddd",
            }
