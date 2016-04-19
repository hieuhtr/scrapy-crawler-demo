# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from WebAnalysis.items import WebanalysisItem
import re
from datetime import datetime

FILE_PATH = 'lazada_category_links.txt'
date = datetime.now()

def read_list_from_file(path):
    list_of_start_urls = []
    for line in open(path, 'r'):
        list_of_start_urls.append(line.strip())
    return list_of_start_urls

def strip_value(value):
    m = re.search("http[^\s]+(\s)*h?(http[^\s>]+)(\s)*", value)
    if m:
        #print m.group(2).encode('UTF-8')
        return m.group(2)
    else:
        #print value.encode('UTF-8')
        return value

class LazadaSpider(CrawlSpider):
    name = 'lazada'
    list_of_start_urls = read_list_from_file(FILE_PATH)

    allowed_domains = ['lazada.vn']
    start_urls = list_of_start_urls

    rules = (
        Rule(LinkExtractor(allow='page=\d+', 
            deny=['/assets/', '/sales/', '/recommendation/', '/*viewOrderTracking/', '/*ordertrackinghelplink/', 
                  '/catalog/ajaxSearchBrands/', '/tracking/sessioncounter/', '/checkout/', '/customer/', '/cart/', '/catalog/review/',
                  '/index/error/', '/images/core_mobile/l/splash.png', '/catalog/gallery/', '/index/index/', '/ajax/locationtree/getall/',
                  '/viewOrderTracking/', '/ordertrackinghelplink/', '/new-products/', '/special-price/', '/?viewType=listView'],
            process_value=strip_value,
            restrict_xpaths=['//span[@class="paging-wrapper"]']), follow=True, process_links=None),
        
        Rule(LinkExtractor(allow='\d+.html', 
            deny=['/assets/', '/sales/', '/recommendation/', '/*viewOrderTracking/', '/*ordertrackinghelplink/', 
                  '/catalog/ajaxSearchBrands/', '/tracking/sessioncounter/', '/checkout/', '/customer/', '/cart/', '/catalog/review/',
                  '/index/error/', '/images/core_mobile/l/splash.png', '/catalog/gallery/', '/index/index/', '/ajax/locationtree/getall/',
                  '/viewOrderTracking/', '/ordertrackinghelplink/', '/new-products/', '/special-price/', '/?viewType=listView'],
            process_value=strip_value,
            restrict_xpaths=['//div[@class="component component-product_list product_list grid    toclear"]']), follow=False, callback='parse_item', process_links=None)        

    )

    def parse_item(self, response):
        i = WebanalysisItem()
        
        try:
            i['product_id'] = response.xpath('//input[@id="config_id"]/@value').extract()[0].strip().encode('UTF-8')
            i['url_product'] = response.url
            i['website'] = 'Lazada - Sold by ' + response.xpath('//div[@class="product__seller__name product-fulfillment__seller__name"]/a/text()').extract()[0].strip().encode('UTF-8')
            i['date'] = date
        except Exception:
            pass

        try:
            i['title'] = response.xpath('//h1[@id="prod_title"]/text()').extract()[0].strip().encode('UTF-8')
        except Exception:
            pass

        try:
            i['current_price'] = response.xpath('//span[@id="product_price"]/text()').extract()[0].strip().encode('UTF-8')
        except Exception:
            pass

        try:
            i['original_price'] = response.xpath('//span[@id="price_box"]/text()').extract()[0].strip().encode('UTF-8')
        except Exception:
            i['original_price'] = i['current_price']

        try:
            block_desc = response.xpath('//div[@class="product-description__block"]//p/text()').extract()
            description = " ".join([block.strip().encode('UTF-8') for block in block_desc])
            i['description'] = description
        except Exception:
            pass

        try:
            detail_info = {}
            detail_table = response.xpath('//table[@class="specification-table"]')

            number_of_rows = len(detail_table.xpath('tr').extract())

            for row in range(number_of_rows):
                key = detail_table.xpath('tr/td[1]/text()').extract()[row].strip().encode('UTF-8') .replace(".","")
                value = detail_table.xpath('tr/td[2]/text()').extract()[row].strip().encode('UTF-8')     
                detail_info[key] = value           
            i['detail_info'] = detail_info  
        except Exception:
            pass

        try:
            i['rating'] = response.xpath('//span[@class="ratingNumber"]/text()').extract()[0].strip().encode('UTF-8')
        except Exception:
            pass

        try:
            i['number_of_rating'] = response.xpath('//div[@class="ratingNumberText"]/@content').extract()[0].strip().encode('UTF-8')
        except Exception:
            pass

        try:
            list_of_comment = []
            comment_table = response.xpath('//ul[@id="js_reviews_list"]')

            number_of_comment = len(comment_table.xpath('li').extract())
            for row in range(1, 6 if number_of_comment > 5 else number_of_comment + 1):
                comment = {}
                
                name = comment_table.xpath('li['+str(row)+']//span[@class="ratRev-revNickname"]/text()').extract()[0].strip().encode('UTF-8')
            
                days = comment_table.xpath('li['+str(row)+']//meta[@itemprop="datePublished"]/@content').extract()[0].strip().encode('UTF-8')
                
                review = comment_table.xpath('li['+str(row)+']//span[@class="ratRev_revTitle"]/text()').extract()[0].strip().encode('UTF-8')
                
                review_detail = comment_table.xpath('li['+str(row)+']//div[@class="ratRev_revDetail"]/text()').extract()[0].strip().encode('UTF-8')
                
                comment['name'] = name
                comment['days'] = days
                comment['review'] = review
                comment['review_detail'] = review_detail
                
                list_of_comment.append(comment)
            if list_of_comment:
                i['list_of_comment'] = list_of_comment
        except Exception:
            pass

        return i
        


