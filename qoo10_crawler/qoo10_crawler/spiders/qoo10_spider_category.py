import scrapy
from scrapy import Request
from qoo10_crawler.items import Qoo10Item
import csv
import os
from scrapy import Selector
import re

path = os.path.dirname(os.path.realpath(__file__))


class Qoo10Spider(scrapy.Spider):
    name = "qoo10_category"
    allowed_domains = ['qoo10.sg']

    def start_requests(self):
        category_csv = csv.DictReader(open('%s\\Input\\Category_qoo10.csv' % path))
        for category in category_csv:
            base_url = 'http://list.qoo10.sg/gmkt.inc/Category/?gdlc_cd=100000006&gdmc_cd=%s'
            category_url = base_url % category["Name"]
            print category_url
            yield Request(category_url, self.parse)

    def parse(self, response):
        hxs = Selector(response)

        # Get one item
        products_html = hxs.xpath('//div[@class="item_wrap"]')
        total_item = 30
        for product_html in products_html:

            if total_item == 0:
                break

            product = Qoo10Item()

            # Get user rating
            rating = product_html.xpath('.//span[@title="Rating"]/span/text()').extract_first()
            if rating:
                product['rating'] = rating.strip()[-1]

            # Get link to sku
            url = product_html.xpath('.//a[@class="tt"]/@href').extract_first()
            if url:
                product['url'] = url

            # Get name of sku
            name = product_html.xpath('.//a[@class="tt"]/text()').extract_first()
            if name:
                product['name'] = name.strip()

            # Get price
            price = product_html.xpath('.//div[@class="prc"]/del/text()').extract_first()
            if price:
                product['price'] = price[1:]

            # Get discount price
            discount_price = product_html.xpath('.//strong[@title="Discounted Price"]/text()').extract_first()
            if discount_price:
                product['price_discount'] = discount_price[1:]

            # Get seller name
            seller = product_html.xpath('.//div[@class="shop"]/a/@title').extract_first()
            if seller:
                product["seller"] = seller.encode('utf-8')

            # Get number of sold
            sold = product_html.xpath('.//div[@class="deal"]/dl/dd/em/text()').extract_first()
            if sold:
                product["item_sold"] = sold

            total_item = total_item - 1
            # Go into sku page
            if url:
                yield Request(product['url'], self.parse_details, meta={'product': product})

    def parse_details(self, response):
        product = response.meta["product"]
        hxs = Selector(response)

        # Get standard shipping fee
        shipping_fee = hxs.xpath(
            './/div[@class="shpp_opt"]/p[@name="delivery_option_no" and text()[contains(.,"Qxpress")]]/em/text()').extract_first()
        if not shipping_fee:
            shipping_fee = hxs.xpath(
                './/div[@class="shpp_opt"]/ul/li/label[text()[contains(.,"Qxpress")]]/em/text()').extract_first()
        if not shipping_fee:
            shipping_fee = hxs.xpath(
                './/div[@class="shpp_opt"]/ul/li/label/em/text()').extract_first()
        if shipping_fee:
            product['shipping_fee'] = shipping_fee

        # Get number of reviews
        review = hxs.xpath('.//a[@tab_name="CustomerReview"]/em/text()').extract_first()
        if review:
            product['review'] = review

        # Get seller rating
        # Format 4.1 / 5
        seller_rating = hxs.xpath('//span[@class="on"]/text()').extract_first()
        if seller_rating:
            product["seller_rating"] = seller_rating.split(" ")[-1]

        # Get oversea location
        location = hxs.xpath('//dl[@name="shipping_panel_area"]/dd/text()').extract_first()
        if location:
            product["local_overseas"] = location

        # Get sku category
        category_list = hxs.xpath('//span[@itemprop="name"]/text()').extract()
        if category_list:
            for level in range(0, len(category_list)):
                if level > 2:
                    break
                product["category_level%s" % str(level + 1)] = category_list[level]

        # Get variations

        variation_list = hxs.xpath(
            '//div[@id="inventory_layer_0"]/div[@class="innerWrap"]/div[@class="select_inner"]/ul/li/a/span/text()').extract()
        if not variation_list:
            variation_list = hxs.xpath(
                '//div[@id="opt_layer_0"]/div[@class="innerWrap"]/div[@class="select_inner"]/ul/li/a/span/text()').extract()
        if variation_list:
            max_variations = 10
            for i in range(0, min(max_variations, len(variation_list))):
                if '----' not in variation_list[i]:
                    product["V%s" % str(i + 1)] = variation_list[i]
                    quantity = re.search(r'(Qty\s\:\s)([0-9]+)([\w]*)', variation_list[i])
                    if quantity:
                        product["Q%s" % str(i + 1)] = quantity.group(2)
                    price = re.search(r'(.+\()([+-]\$[0-9]+\.[0-9]+)(\)\w*)', variation_list[i])
                    if price:
                        product["P%s" % str(i + 1)] = price.group(2)

        yield product
