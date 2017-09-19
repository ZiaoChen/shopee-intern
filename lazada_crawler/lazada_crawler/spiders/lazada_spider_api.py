import scrapy
from scrapy import Request
from lazada_crawler.items import LazadaItem
import csv
import sys
import os
from scrapy import Selector
import json
import time

class LazadaSpiderAPI(scrapy.Spider):
    name = "lazada_api"
    path = os.path.dirname(os.path.realpath(__file__))

    base_url = 'http://www.lazada.%s/mobapi/%s/?sort=name&dir=asc&page=%s&maxitems=400'

    output_path = "%s.csv"

    field_names = ['id', 'name', 'sku', 'url', 'description', 'price', 'special_price', 'rating', 'brand', 'categories',
                   'seller_name', 'size', 'weight',
                   'img_1', 'img_2', 'img_3', 'img_4', 'img_5', 'img_6', 'img_7', 'img_8', 'img_9',
                   'v1_attribute_set_name',
                   'v1_min_delivery_time', 'v1_price', 'v1_special_price', 'v1_quantity', 'v1_shipping_weight',
                   'v1_sku',
                   'v2_attribute_set_name',
                   'v2_min_delivery_time', 'v2_price', 'v2_special_price', 'v2_quantity', 'v2_shipping_weight',
                   'v2_sku',
                   'v3_attribute_set_name',
                   'v3_min_delivery_time', 'v3_price', 'v3_special_price', 'v3_quantity', 'v3_shipping_weight',
                   'v3_sku',
                   'v4_attribute_set_name',
                   'v4_min_delivery_time', 'v4_price', 'v4_special_price', 'v4_quantity', 'v4_shipping_weight',
                   'v4_sku',
                   'v5_attribute_set_name',
                   'v5_min_delivery_time', 'v5_price', 'v5_special_price', 'v5_quantity', 'v5_shipping_weight',
                   'v5_sku',
                   'v6_attribute_set_name',
                   'v6_min_delivery_time', 'v6_price', 'v6_special_price', 'v6_quantity', 'v6_shipping_weight',
                   'v6_sku',
                   'v7_attribute_set_name',
                   'v7_min_delivery_time', 'v7_price', 'v7_special_price', 'v7_quantity', 'v7_shipping_weight',
                   'v7_sku',
                   'v8_attribute_set_name',
                   'v8_min_delivery_time', 'v8_price', 'v8_special_price', 'v8_quantity', 'v8_shipping_weight',
                   'v8_sku',
                   'v9_attribute_set_name',
                   'v9_min_delivery_time', 'v9_price', 'v9_special_price', 'v9_quantity', 'v9_shipping_weight',
                   'v9_sku',
                   'v10_attribute_set_name',
                   'v10_min_delivery_time', 'v10_price', 'v10_special_price', 'v10_quantity', 'v10_shipping_weight',
                   'v10_sku',
                   'v11_attribute_set_name',
                   'v11_min_delivery_time', 'v11_price', 'v11_special_price', 'v11_quantity', 'v11_shipping_weight',
                   'v11_sku',
                   'v12_attribute_set_name',
                   'v12_min_delivery_time', 'v12_price', 'v12_special_price', 'v12_quantity', 'v12_shipping_weight',
                   'v12_sku',
                   'v13_attribute_set_name',
                   'v13_min_delivery_time', 'v13_price', 'v13_special_price', 'v13_quantity', 'v13_shipping_weight',
                   'v13_sku',
                   'v14_attribute_set_name',
                   'v14_min_delivery_time', 'v14_price', 'v14_special_price', 'v14_quantity', 'v14_shipping_weight',
                   'v14_sku',
                   'v15_attribute_set_name',
                   'v15_min_delivery_time', 'v15_price', 'v15_special_price', 'v15_quantity', 'v15_shipping_weight',
                   'v15_sku']

    def start_requests(self):
        input_csv = self.get_input_file('%s\\Input\\Seller.csv' % self.path)

        pages_to_crawl = 1
        for seller in input_csv:
            for page_num in range(1, pages_to_crawl + 1):
                seller_url = self.base_url % (self.get_url(seller["Country"]), seller["Name"], page_num)
                print seller_url
                output_csv = self.get_output_file(self.output_path % seller["Name"], self.field_names)
                output_csv.writeheader()
                yield Request(seller_url, self.crawl_single_seller, meta={'output_csv': output_csv})

    def get_input_file(self, input_path):
        return csv.DictReader(open(input_path))

    def get_output_file(self, output_path, output_fieldname):
        return csv.DictWriter(open(output_path, "wb"), fieldnames=output_fieldname)

    def get_url(self, name):
        if name == "Singapore":
            return "sg"
        elif name == "Indonesia":
            return "co.id"

    def crawl_single_seller(self, response):
        hxs = Selector(response)
        data_body = hxs.xpath('//p/text()').extract_first()
        data_json = json.loads(data_body)
        sku_list = data_json["metadata"]["results"]
        for sku_raw in sku_list:
            sku = sku_raw["data"]
            processed_sku = dict()
            processed_sku["id"] = sku_raw["id"]
            processed_sku["name"] = sku["name"].replace("\n", "")
            processed_sku["sku"] = sku["sku"]
            processed_sku["url"] = sku["url"].replace("/mobapi", "")
            processed_sku["description"] = sku["description"].replace("\n", "")
            processed_sku["price"] = sku["price"]
            processed_sku["special_price"] = sku["special_price"]
            if "ratings_total" in sku:
                processed_sku["rating"] = sku["ratings_total"]["avr"]
            else:
                processed_sku["rating"] = "No Rating"
            processed_sku["brand"] = sku["brand"]
            processed_sku["categories"] = sku["categories"]
            if "images" in sku_raw:
                for i in range(0, min(len(sku_raw["images"]), 9)):
                    processed_sku["img_%s" % str(i + 1)] = sku_raw["images"][i]["path"]
            variations = sku["simples"].keys()
            for i in range(0, min(15, len(variations))):
                processed_sku["v%s_attribute_set_name" % str(i + 1)] = sku["simples"][variations[i]]["meta"][
                    "attribute_set_name"]
                processed_sku["v%s_min_delivery_time" % str(i + 1)] = sku["simples"][variations[i]]["meta"][
                    "min_delivery_time"]
                processed_sku["v%s_price" % str(i + 1)] = sku["simples"][variations[i]]["meta"]["price"]
                processed_sku["v%s_special_price" % str(i + 1)] = sku["simples"][variations[i]]["meta"]["special_price"]
                processed_sku["v%s_quantity" % str(i + 1)] = sku["simples"][variations[i]]["meta"]["quantity"]
                processed_sku["v%s_shipping_weight" % str(i + 1)] = sku["simples"][variations[i]]["meta"][
                    "shipping_weight"]
                processed_sku["v%s_sku" % str(i + 1)] = sku["simples"][variations[i]]["meta"]["sku"]

            print sku["url"]
            yield Request(sku["url"], self.crawl_details,
                          meta={'output_csv': response.meta["output_csv"], 'processed_sku': processed_sku})

    def crawl_details(self, response):
        output_csv = response.meta["output_csv"]
        processed_sku = response.meta["processed_sku"]
        hxs = Selector(response)
        data_body = hxs.xpath('//body//text()').extract()
        data_body = "".join(data_body)
        json.loads(data_body)

        data_json = json.loads(data_body)
        sku_details = data_json["metadata"]["data"]
        if sku_details["supplierName"] == "Taobao Collection" and "taobao_seller_name" in sku_details["attributes"]:
            processed_sku["seller_name"] = sku_details["attributes"]["taobao_seller_name"]
        else:
            processed_sku["seller_name"] = sku_details["supplierName"]
        if "product_measures" in sku_details["attributes"]:
            processed_sku["size"] = sku_details["attributes"]["product_measures"]
        if "product_weight" in sku_details["attributes"]:
            processed_sku["weight"] = sku_details["attributes"]["product_weight"]
        output_csv.writerow(processed_sku)
