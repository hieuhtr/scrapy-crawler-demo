# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from tikicrawler.items import TikicrawlerItem


class TikiSpider(CrawlSpider):
    name = 'tiki'
    allowed_domains = ['tiki.vn']
    start_urls = ['http://www.tiki.vn/']

    rules = (
        Rule(LinkExtractor(allow='/(.*?)-p[0-9]+\.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = TikicrawlerItem()
        
        try:
            i['title'] = response.xpath('//h1[@class="item-name"]/text()').extract()[0].strip()
        except Exception:
            i['title'] = ''

        try:
            i['special_price'] = response.xpath('//p[@class="special-price-item"]/@data-value').extract()[0]
        except Exception:
            i['special_price'] = ''

        try:
            i['category'] = response.xpath('//table[@id="chi-tiet"]/tbody/tr[last()]/td[@class="last"]/a/text()').extract()[0]
        except Exception:
            i['category'] = ''

        try:
            i['original_price'] = response.xpath('//p[@class="old-price-item"]/@data-value').extract()[0]
        except Exception:
            i['original_price'] = ''
        
        try:
            i['description'] = response.xpath('//div[@id="gioi-thieu"]/p/text()').extract()[0]
        except Exception:
            i['description'] = ''

        try:
            i['rating'] = response.xpath('//p[@class="total-review-point"]/text()').extract()[0]
        except Exception:
            i['rating'] = ''

        try:
            i['comments_count'] = response.xpath('//p[@class="comments-count"]/a/text()').extract()[0] 
        except Exception:
            i['comments_count'] = ''

        if  i['title'] == i['special_price'] == i['category'] == i['original_price'] == i['description'] == i['rating'] == i['comments_count'] == '':
            return None
        else:
            return i
