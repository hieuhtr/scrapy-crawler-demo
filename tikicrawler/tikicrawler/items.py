# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TikicrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    special_price = scrapy.Field()
    category = scrapy.Field()
    original_price = scrapy.Field()
    rating = scrapy.Field()
    comments_count = scrapy.Field()
    description = scrapy.Field()
