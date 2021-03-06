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
        if self.db.openDB(host="localhost",user="antonio",passwd="antonio",db="processors"):
            sys.exit("Error al abrir la base de datos")
    
    def process_item(self, item, spider):
        if item['availability'][0]:     # No todos tienen este campo, así que hay que comprobarlo.
            availability=item['availability'][0]
        else:
            availability="No disponible"
        self.db.addRegister(item['brand'][0],item['model'][0],item['frequency'][0],item['price'][0], availability)
        return item
    
    def close_spider(self, spider):
        pass