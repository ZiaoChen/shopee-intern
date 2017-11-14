import scrapy
from scrapy import Request, FormRequest
from wish_crawler.items import WishItem
import csv
import sys
import os
from scrapy import Selector
import json
import re

reload(sys)
sys.setdefaultencoding('UTF8')

path = os.path.dirname(os.path.realpath(__file__))


class WishSpider(scrapy.Spider):
    handle_httpstatus_list = [404, 500]
    name = "wish_seller"
    no_skus = 58
    base_url = 'http://www.wish.com/merchant/%s'
    base_url_sku = 'http://www.wish.com/c/%s'
    more_items_url = 'https://www.wish.com/api/merchant'

    def start_requests(self):
        seller_csv = csv.DictReader(open('%s\\Input\\Shop.csv' % path))
        for seller in seller_csv:
            seller_url = self.base_url % (seller["Name"])
            print seller_url
            yield Request(seller_url, self.parse)

    def parse(self, response):
        hxs = Selector(response)
        page = json.loads(hxs.xpath('.//script').extract()[-1].split(";")[2].split(" = ", 1)[1])
        for i in range(min(self.no_skus, len(page))):
            sku = page[i]
            sku_url = self.base_url_sku % str(sku["id"])
            print sku_url
            # yield Request(sku_url, self.parse_details)
        merchant_name = str(hxs.xpath('.//script/text()').extract()[-1].split(";")[-2].split(" = ", 1)[1])

        form_data = {
            "start": "90",
            "query": "nantongxinxiatextilegarmentcoltd",
            "is_commerce": "true",
            "transform": "true",
            "last_cids": ["53f882161c105e63e266b617",
            "550de9188e8def3726fc4058",
            "55a7a7de7e10364065664590",
            "566d6b5c4ee3b347dcdea0bd",
            "55973c6d0bf6684040c5485b",
            "558b146885c59e67d84d523b",
            "558b0b831739d0403a8ad959",
            "56603b5b8c6546103c73f595",
            "5780ba4f2b3bd87888af6af0",
            "54c44be0d7df3c160293bca4",
            "54fadee5a0086e380d602f4c",
            "54c26eac39b8c07edc26f48e",
            "574c23f54c724460c7427e84",
            "57491e3a38d91c60c4dc4f36",
            "573842d6063b655ebd22d918",
            "57fdedd5d8045d2f1a211886",
            "544b8acd9719cd33351a7b28",
            "54d97db5bbac3405122026d1"],
            "count": "21",
            "include_buy_link": "true",
            "_buckets": "",
            "_experiments": ""}
        headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept - Encoding":"gzip, deflate, br",
        "Accept - Language":"en-US, en;q=0.8",
        "Connection":"keep-alive",
        "Content - Length":"888",
        "Content - Type":"application/x-www-form-urlencoded;charset=UTF-8",
        "Host":"www.wish.com",
        "Origin":"https://www.wish.com",
        "Referer":"https://www.wish.com/merchant/nantongxinxiatextilegarmentcoltd",
        "X - Requested - With":"XMLHttpRequest",
        "X - XSRFToken":"2|8eff6ca2|8057759fdc973318de2258eee653c7bf|1504779935"
        }
        yield FormRequest(url=self.more_items_url, callback=self.get_more_skus,
                          formdata=form_data,headers=headers)

    def get_more_skus(self, response):
        print response

    def parse_details(self, response):
        sku_selector = Selector(response)
        sku = WishItem()
        sku_json = json.loads(sku_selector.xpath('.//script').extract()[-2].rsplit(";", 5)[0].split(" = ", 1)[1])
        sku_json_keys = sku_json.keys()
        # Get rating
        if "product_rating" in sku_json_keys:
            if "rating" in sku_json["product_rating"].keys():
                sku["rating"] = sku_json["product_rating"]["rating"]

            if "rating_count" in sku_json["product_rating"].keys():
                sku["rating_count"] = sku_json["product_rating"]["rating_count"]

        # Get main picture
        if "small_picture" in sku_json_keys:
            sku["img_1"] = sku_json["small_picture"]

        if "extra_photo_urls" in sku_json_keys:
            for i in range(min(8, len(sku_json["extra_photo_urls"].keys()))):
                sku["img_%s" % str(i + 2)] = sku_json["extra_photo_urls"][str(i + 1)]

        sku["id"] = sku_json["id"]
        sku["url"] = self.base_url_sku % sku["id"]
        sku["name"] = sku_json["name"]
        sku["seller"] = sku_json["commerce_product_info"]["variations"][0]["merchant"]

        if "total_inventory" in sku_json["commerce_product_info"].keys():
            sku["total_inventory"] = sku_json["commerce_product_info"]["total_inventory"]

        if "num_bought" in sku_json_keys:
            sku["num_bought"] = sku_json["num_bought"]

        if "brand" in sku_json_keys:
            sku["brand"] = sku_json["brand"]

        if "description" in sku_json_keys:
            sku["description"] = sku_json["description"]

        if "gender" in sku_json_keys:
            sku["gender"] = sku_json["gender"]

        if "merchant_rating" in sku_json["commerce_product_info"]["variations"][0].keys():
            sku["seller_rating"] = sku_json["commerce_product_info"]["variations"][0]["merchant_rating"]

        variations = sku_json["commerce_product_info"]["variations"]
        for i in range(min(15, len(sku_json["commerce_product_info"]["variations"]))):
            sku["v%s_price" % str(i + 1)] = variations[i]["retail_price"]
            sku["v%s_price_discount" % str(i + 1)] = variations[i]["price"]
            sku["v%s_min_fullfillment_time" % str(i + 1)] = variations[i]["min_fulfillment_time"]
            sku["v%s_max_fullfillment_time" % str(i + 1)] = variations[i]["max_fulfillment_time"]
            sku["v%s_inventory" % str(i + 1)] = variations[i]["inventory"]
            if "size" in variations[i].keys():
                sku["v%s_size" % str(i + 1)] = variations[i]["size"]
            if "color" in variations[i].keys():
                sku["v%s_color" % str(i + 1)] = variations[i]["color"]

            sku["v%s_shipping_fee" % str(i + 1)] = variations[i]["shipping"]

        yield sku
