from scrapy import Spider
from scrapy.selector import Selector

from stack.items import StackItem


class StackSpider(Spider):
    name = "stack"
    allowed_domains = ["shop.aothun.vn"]
    start_urls = [
        "http://shop.aothun.vn",
    ]

    def parse(self, response):
        questions = Selector(response).xpath('//div[@class="product-container text-left product-block"]')

        for question in questions:
            item = StackItem()
            item['url'] = question.xpath(
                'div[@class="product-image-container image"]/a[@class="product_img_link"]/@href').extract()[0]
            item['title'] = question.xpath(
                'div[@class="product-image-container image"]/a[@class="product_img_link"]/@title').extract()[0]
            item['price'] = question.xpath(
                'div[@class="product-meta"]/div[@class="clearfix"]/div[@class="content_price"]/span[@class="price product-price "]/text()').extract()[0]
            
            yield item

