# -*- coding: utf-8 -*-

import sys
import os

os.chdir('./scraper')
os.system('scrapy crawl processors')
os.chdir('..')