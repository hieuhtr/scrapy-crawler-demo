# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider
from scrapy.selector import Selector
from tikilink.items import TikilinkItem

import re
import urlparse

def write_text_begin():
	with open('item_link.txt', 'a') as f:
            	f.write("[")

def write_text_end():
	with open('item_link.txt', 'a') as f:
            	f.write("]")


def format_link(url):
    	if not url.startswith('http://tiki.vn/'):
    		url = urlparse.urljoin('http://tiki.vn/', url)
    		# print url
    	return url

class LinkSpider(scrapy.Spider):
    name = "link"
    allowed_domains = ["tiki.vn"]
    start_urls = (
        'http://tiki.vn/',
    )

    

    def parse(self, response):
        source = Selector(response).xpath('//nav[@class="header-navigation"]//a/@href')
        # links = source.xpath('//a/@href')

        # write_text_begin()


        for link in source:
            item = TikilinkItem()
            
            url = link.extract()
            url = format_link(url)

            item['url'] = url
            
            # print url
            
            # with open('item_link.txt', 'a') as f:
            #	f.write("'" + url + "',\n" )
            


            with open('item_link.txt', 'a') as f:
            	if url != 'javascript:void(0);':
            		f.write(url + "\n")

            yield item

        # write_text_end()

