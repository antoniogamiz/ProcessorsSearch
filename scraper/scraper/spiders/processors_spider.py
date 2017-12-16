# -*- coding: utf-8 -*-
import scrapy
from scraper.items import ProcessorsItem
from scrapy.loader import ItemLoader

class ProcessorsSpider(scrapy.Spider):
    name = "processors"
    start_urls = [
        "https://www.pccomponentes.com/procesadores/",
    ]
    def parse(self, response):
        for href in response.xpath("/html/body/div[1]/div[2]/div/div/div[2]/div/div[4]/div/div/article/div[1]/a"):
            yield response.follow(href, self.parse_processors)

    def parse_processors(self, response):
            loader = ItemLoader(ProcessorsItem(), selector=response)
            loader.add_xpath('brand', '/html/body/div[1]/div[2]/div[1]/div[2]/div/div/div[1]/h1/strong/text()')
            loader.add_xpath('model', '/html/body/div[1]/div[2]/div[1]/div[2]/div/div/div[1]/h1/strong/text()')
            loader.add_xpath('frequency', '/html/body/div[1]/div[2]/div[1]/div[2]/div/div/div[1]/h1/strong/text()')
            loader.add_xpath('price', '/html/body/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[1]/span[1]/text()')
            loader.add_xpath('availability', '//*[@id="GTM-desplegableFicha-disponibilidad"]/text()')
            return loader.load_item()