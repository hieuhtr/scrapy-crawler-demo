# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log

class TikicrawlerPipeline(object):
    def __init__(self):
    	connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]
        self.file = codecs.open('itemsnew.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        #write to json file
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        
        #write to mongodb
        for data in item:
            if not data:
                raise DropItem("Missing data!")
        self.collection.update({'title': item['title'], 'special_price' : item['special_price'], 'category' : item['category'], 'original_price' : item['original_price'], 'description' : item['description'], 'rating' : item['rating'], 'comments_count' : item['comments_count']}, dict(item), upsert=True)
        log.msg("Product added to MongoDB database!",
                level=log.DEBUG, spider=spider)
        return item

    def spider_closed(self, spider):
        self.file.close()    