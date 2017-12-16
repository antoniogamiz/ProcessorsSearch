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
        self.db.addRegister(item['brand'][0],item['model'][0],item['frequency'][0],item['price'][0])
        return item
    
    def close_spider(self, spider):
        reg=self.db.getRegisters()
        for r in reg:
            print r