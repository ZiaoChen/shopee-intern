import scrapy
from scrapy import Request
from lazada_crawler.items import LazadaItem
import csv
import sys
import os
from scrapy import Selector
import json

reload(sys)
sys.setdefaultencoding('UTF8')

path = os.path.dirname(os.path.realpath(__file__))


def get_url(name):
    if name == "sg":
        return "sg"
    elif name == "id":
        return "co.id"


class LazadaSpider(scrapy.Spider):
    name = "lazada_category"

    def start_requests(self):
        category_csv = csv.DictReader(open('%s\\Input\\Category.csv' % path))
        for category in category_csv:
            base_url = 'http://www.lazada.%s/%s//?spm=a2o42.campaign-714.0.0.oW5MBl&dir=desc&itemperpage=120&sc=IcoC&sort=ratingdesc&page=%s'
            try:
                total_page = int(category["Page"])
            except:
                total_page = 1
            for page_num in range(1, total_page + 1):
                category_url = base_url % (get_url(category["Country"]), category["Name"], page_num)
                print category_url
                yield Request(category_url, self.parse, meta={'Country': category["Country"]})

    def parse(self, response):
        hxs = Selector(response)
        products_html = hxs.xpath('//div[@class="c-product-card__description"]')
        country = response.meta['Country']
        base_url = 'http://www.lazada.%s' % get_url(country)
        for product_html in products_html:
            product = LazadaItem()

            # Get number of reviews
            review = product_html.xpath(
                './/div[@class="c-product-card__review-num"]/text()').extract_first()
            if review:
                product['review'] = review.split(" ")[0][1]

            # Get user rating
            rating = product_html.xpath(
                './/div[@class="c-rating-stars  c-product-card__rating-stars "]/@data-value').extract_first()
            if rating:
                product['rating'] = float(rating)

            # Get link to sku
            relative_url = product_html.xpath('.//a/@href').extract_first()
            if relative_url:
                product['url'] = base_url + relative_url.strip()

            # Get name of sku
            name = product_html.xpath('.//a/text()').extract_first()
            if name:
                product['name'] = name.strip()

            # Go into sku page
            if relative_url:
                yield Request(product['url'], self.parse_details,
                              meta={'product': product, 'country': country})

    def parse_details(self, response):
        product = response.meta["product"]
        hxs = Selector(response)

        country = response.meta["country"]
        # Get sku price
        price = hxs.xpath('//span[@id="price_box"]/text()').extract_first()
        if price:
            if country == "sg":
                product["price"] = float(price.split(" ")[1][:-1].replace(',', ""))
            elif country == "id":
                product["price"] = float(price.split(" ")[1][:-1].replace('.', ""))

        # Get sku original price
        price_discount = hxs.xpath('//span[@id="special_price_box"]/text()').extract_first()
        if price_discount:
            if country == "sg":
                product["price_discount"] = float(price_discount.replace(',', ""))
            elif country == "id":
                product["price_discount"] = float(price_discount.replace('.', ""))

        # Get seller name
        seller = hxs.xpath('//a[@class="basic-info__name"]/text()').extract_first()
        if seller:
            product["seller"] = seller

        # Get seller rating
        # Format e.g. 90 / 100
        seller_rating = hxs.xpath(
            '//div[@class="c-positive-seller-ratings c-positive-seller-ratings_state_high"]/text()').extract_first()
        print seller_rating
        if seller_rating:
            product["seller_rating"] = seller_rating.strip()

        # Get sku size and weight
        # Format
        # <tr><td class="bold">Size (L x W x H)</td><td>value</td></tr>
        specification_table = hxs.xpath('//table[@class="specification-table"]')
        if specification_table:
            specification_table_cells = specification_table.xpath('.//td/text()').extract()
            if specification_table_cells:
                # Get Size
                previous_cell = ""
                for cell in specification_table_cells:
                    if country == "sg":
                        if "Size" in previous_cell:
                            product["size"] = cell
                            break
                    elif country == "id":
                        if "Ukuran" in previous_cell:
                            product["size"] = cell
                            break
                    previous_cell = cell

                # Get Weight
                previous_cell = ""
                for cell in specification_table_cells:
                    if country == "sg":
                        if "Weight" in previous_cell:
                            product["weight"] = cell
                            break
                    elif country == "id":
                        if "Berat" in previous_cell:
                            product["weight"] = cell
                            break
                    previous_cell = cell

        # Get sku category
        category_list = hxs.xpath('//span[@class="breadcrumb__item-text"]')
        if category_list:
            for level in range(0, len(category_list)):
                if level > 2:
                    break
                product["category_level%s" % str(level + 1)] = category_list[level].xpath(
                    './/span/text()').extract_first()

        # Get standard shipping fee
        if country == "sg":
            shipping_options = hxs.xpath('//div[@class="delivery-option-st__label"]/text()').extract()
            product["local_overseas"] = "local"
            if shipping_options:
                for shipping_option in shipping_options:
                    if "Standard Delivery" in shipping_option:
                        try:
                            product["shipping_fee"] = float(shipping_option.split(" ")[-1])
                        except:
                            product["shipping_fee"] = shipping_option.split(" ")[-1]

                    if "overseas" in shipping_option:
                        product["local_overseas"] = "overseas"
            yield product
        elif country == "id":
            product["local_overseas"] = "local"
            shipping_options = hxs.xpath('//div[@class="delivery-option-st__label"]/text()').extract()
            if shipping_options:
                for shipping_option in shipping_options:
                    if "negeri" in shipping_option:
                        product["local_overseas"] = "overseas"
                        break

            sku = hxs.xpath('//input[@id="configSku"]/@value').extract_first()
            ajax_url = "http://www.lazada.co.id/ajax/delivery/deliveryTypesForProducts/?sku=%s&mp=1&FORM_TOKEN=4c4e3046d485b17f21fe0e86d4bd8a721c0592b0&maxDeliveryTime=4&minDeliveryTime=2&province_id=26&city_id=6407&ward_id=17275&blockedLocation=false" % sku
            yield Request(ajax_url, self.get_shipping_fee_Indonesia, meta={'product': product})

    def get_shipping_fee_Indonesia(self, response):
        product = response.meta["product"]
        json_response = json.loads(response.body_as_unicode())
        try:
            product["shipping_fee"] = json_response["deliveryOptions"]["standard"]["price"]
        except:
            product["shipping_fee"] = "Not exist"

        yield product
