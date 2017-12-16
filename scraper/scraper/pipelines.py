# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
import scraper.data_base.db as db


class ProcessorsPipeline(object):
    def open_spider(self, spider):
        self.db=db.DB_Handler()
        if self.db.openDB(host="localhost",user="antonio",passwd="antonio",db="proyecto"):
            sys.exit("Error al abrir la base de datos")
    def process_item(self, item, spider):
        return item
