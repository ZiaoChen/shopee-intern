# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LazadaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    price_discount = scrapy.Field()
    url = scrapy.Field()
    rating = scrapy.Field()
    review = scrapy.Field()
    seller = scrapy.Field()
    seller_rating = scrapy.Field()
    shipping_fee = scrapy.Field()
    size = scrapy.Field()
    weight = scrapy.Field()
    category_level1 = scrapy.Field()
    category_level2 = scrapy.Field()
    category_level3 = scrapy.Field()
    local_overseas = scrapy.Field()


