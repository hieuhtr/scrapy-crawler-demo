# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from tikibook.items import TikibookItem
import re


def read_file_to_list(path):
    list_of_start_urls = []
    with open(path, 'r') as f:
        list_of_start_urls.append(f.readline().strip())
    return list_of_start_urls

def strip_value(value):
    m = re.search("http[^\s]+(\s)*h?(http[^\s>]+)(\s)*", value)
    if m:
        #print m.group(2).encode('UTF-8')
        return m.group(2)
    else:
        #print value.encode('UTF-8')
        return value


class ProductSpider(CrawlSpider):
    name = 'product'
    
    list_of_start_urls = read_file_to_list('item_link.txt')

    allowed_domains = ['tiki.vn']
    #start_urls = ['http://tiki.vn/sach-truyen-tieng-viet/c316/?order=name%2Casc&limit=2000/']
    
    start_urls = list_of_start_urls

    rules = (
    #    #Rule(LinkExtractor(allow='p[0-9]+', 
    #        #deny=['/customer/', '/sales/', '/order/', '/checkout/', '/nhan-xet', '/tel', '/(\s)+/'],
    #        #process_value=strip_value), callback='parse_item', follow=True, process_links=None),
        Rule(LinkExtractor(allow='', 
            deny=['/customer/', '/sales/', '/order/', '/checkout/', '/nhan-xet', '/tel', '/(\s)+/', '/author/', '/TIKI/'],
            process_value=strip_value), follow=True, callback='parse_item', process_links=None),        
    )

    def parse_item(self, response):


        i = TikibookItem()
        try:
            i['product_id'] = response.xpath('//input[@id="product_id"]/@value').extract()[0].strip().encode('UTF-8')
        except Exception:
            pass

        try:
            i['title'] = response.xpath('//h1[@class="item-name"]/text()').extract()[0].strip().encode('UTF-8')
        except IndexError:
            pass

        try:
            i['price'] = response.xpath('//p[@class="special-price-item"]/@data-value').extract()[0].strip().encode('UTF-8')
        except IndexError:
            pass

        try:
            i['category'] = response.xpath('//table[@id="chi-tiet"]/tbody/tr[last()]/td[@class="last"]/a/text()').extract()[0].strip().encode('UTF-8')
        except IndexError:
            pass
        return i
        self.logger.info('A response from %s just arrived!', response.url)

