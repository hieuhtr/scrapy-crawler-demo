# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TikibookItem(scrapy.Item):
    # define the fields for your item here like:
    product_id = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    category = scrapy.Field()
    
