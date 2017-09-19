import scrapy
from web_crawler.items import Item
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule


class QuotesSpider(scrapy.Spider):
    name = "lazada"
    allowed_domains = ['businessideadaily.com']
    start_urls = [
            'http://www.lazada.sg/'
        ]

    def parse(self, response):
        for href in response.css('div a::attr(href)'):
            #print href
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        product = Item()
        product['name'] = response.css('h3.c-product-item__title::text').extract()
        product['price'] = response.css('dive.c-product-item__price::text').extract()
        product['url'] = response.url
        yield product