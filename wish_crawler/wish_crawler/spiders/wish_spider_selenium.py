from selenium import webdriver
import os
from selenium.webdriver.common.keys import Keys
import time
import json
import csv
import signal
import pandas as pd
import sys

reload(sys)
sys.setdefaultencoding('utf8')

# Config Variables
path = os.path.dirname(os.path.realpath(__file__))
seller_url_base = 'http://www.wish.com/merchant/%s'
sku_url_base = 'http://www.wish.com/c/%s'
wish_url = 'http://www.wish.com'
username = "mingjie.lyu@shopee.com"
password = "rainyoutside"
fieldnames = ['ps_product_name',
              'ps_gender',
              'ps_url',
              'ps_rating',
              'ps_rating_count',
              'ps_seller',
              'ps_seller_rating',
              'ps_img_1',
              'ps_img_2',
              'ps_img_3',
              'ps_img_4',
              'ps_img_5',
              'ps_img_6',
              'ps_img_7',
              'ps_img_8',
              'ps_img_9',
              'ps_sku_ref_no_parent',
              'ps_stock',
              'ps_num_bought',
              'ps_brand',
              'ps_product_description',
              'ps_variation 1 ps_variation_price',
              'ps_variation 1 ps_variation_price_discount',
              'ps_variation 1 ps_variation_min_fullfillment_time',
              'ps_variation 1 ps_variation_max_fullfillment_time',
              'ps_variation 1 ps_variation_stock',
              'ps_variation 1 ps_variation_size',
              'ps_variation 1 ps_variation_color',
              'ps_variation 1 ps_variation_shipping_fee',
              'ps_variation 2 ps_variation_price',
              'ps_variation 2 ps_variation_price_discount',
              'ps_variation 2 ps_variation_min_fullfillment_time',
              'ps_variation 2 ps_variation_max_fullfillment_time',
              'ps_variation 2 ps_variation_stock',
              'ps_variation 2 ps_variation_size',
              'ps_variation 2 ps_variation_color',
              'ps_variation 2 ps_variation_shipping_fee',
              'ps_variation 3 ps_variation_price',
              'ps_variation 3 ps_variation_price_discount',
              'ps_variation 3 ps_variation_min_fullfillment_time',
              'ps_variation 3 ps_variation_max_fullfillment_time',
              'ps_variation 3 ps_variation_stock',
              'ps_variation 3 ps_variation_size',
              'ps_variation 3 ps_variation_color',
              'ps_variation 3 ps_variation_shipping_fee',
              'ps_variation 4 ps_variation_price',
              'ps_variation 4 ps_variation_price_discount',
              'ps_variation 4 ps_variation_min_fullfillment_time',
              'ps_variation 4 ps_variation_max_fullfillment_time',
              'ps_variation 4 ps_variation_stock',
              'ps_variation 4 ps_variation_size',
              'ps_variation 4 ps_variation_color',
              'ps_variation 4 ps_variation_shipping_fee',
              'ps_variation 5 ps_variation_price',
              'ps_variation 5 ps_variation_price_discount',
              'ps_variation 5 ps_variation_min_fullfillment_time',
              'ps_variation 5 ps_variation_max_fullfillment_time',
              'ps_variation 5 ps_variation_stock',
              'ps_variation 5 ps_variation_size',
              'ps_variation 5 ps_variation_color',
              'ps_variation 5 ps_variation_shipping_fee',
              'ps_variation 6 ps_variation_price',
              'ps_variation 6 ps_variation_price_discount',
              'ps_variation 6 ps_variation_min_fullfillment_time',
              'ps_variation 6 ps_variation_max_fullfillment_time',
              'ps_variation 6 ps_variation_stock',
              'ps_variation 6 ps_variation_size',
              'ps_variation 6 ps_variation_color',
              'ps_variation 6 ps_variation_shipping_fee',

              'ps_variation 7 ps_variation_price',
              'ps_variation 7 ps_variation_price_discount',
              'ps_variation 7 ps_variation_min_fullfillment_time',
              'ps_variation 7 ps_variation_max_fullfillment_time',
              'ps_variation 7 ps_variation_stock',
              'ps_variation 7 ps_variation_size',
              'ps_variation 7 ps_variation_color',
              'ps_variation 7 ps_variation_shipping_fee',

              'ps_variation 8 ps_variation_price',
              'ps_variation 8 ps_variation_price_discount',
              'ps_variation 8 ps_variation_min_fullfillment_time',
              'ps_variation 8 ps_variation_max_fullfillment_time',
              'ps_variation 8 ps_variation_stock',
              'ps_variation 8 ps_variation_size',
              'ps_variation 8 ps_variation_color',
              'ps_variation 8 ps_variation_shipping_fee',

              'ps_variation 9 ps_variation_price',
              'ps_variation 9 ps_variation_price_discount',
              'ps_variation 9 ps_variation_min_fullfillment_time',
              'ps_variation 9 ps_variation_max_fullfillment_time',
              'ps_variation 9 ps_variation_stock',
              'ps_variation 9 ps_variation_size',
              'ps_variation 9 ps_variation_color',
              'ps_variation 9 ps_variation_shipping_fee',

              'ps_variation 10 ps_variation_price',
              'ps_variation 10 ps_variation_price_discount',
              'ps_variation 10 ps_variation_min_fullfillment_time',
              'ps_variation 10 ps_variation_max_fullfillment_time',
              'ps_variation 10 ps_variation_stock',
              'ps_variation 10 ps_variation_size',
              'ps_variation 10 ps_variation_color',
              'ps_variation 10 ps_variation_shipping_fee',

              'ps_variation 11 ps_variation_price',
              'ps_variation 11 ps_variation_price_discount',
              'ps_variation 11 ps_variation_min_fullfillment_time',
              'ps_variation 11 ps_variation_max_fullfillment_time',
              'ps_variation 11 ps_variation_stock',
              'ps_variation 11 ps_variation_size',
              'ps_variation 11 ps_variation_color',
              'ps_variation 11 ps_variation_shipping_fee',

              'ps_variation 12 ps_variation_price',
              'ps_variation 12 ps_variation_price_discount',
              'ps_variation 12 ps_variation_min_fullfillment_time',
              'ps_variation 12 ps_variation_max_fullfillment_time',
              'ps_variation 12 ps_variation_stock',
              'ps_variation 12 ps_variation_size',
              'ps_variation 12 ps_variation_color',
              'ps_variation 12 ps_variation_shipping_fee',

              'ps_variation 13 ps_variation_price',
              'ps_variation 13 ps_variation_price_discount',
              'ps_variation 13 ps_variation_min_fullfillment_time',
              'ps_variation 13 ps_variation_max_fullfillment_time',
              'ps_variation 13 ps_variation_stock',
              'ps_variation 13 ps_variation_size',
              'ps_variation 13 ps_variation_color',
              'ps_variation 13 ps_variation_shipping_fee',

              'ps_variation 14 ps_variation_price',
              'ps_variation 14 ps_variation_price_discount',
              'ps_variation 14 ps_variation_min_fullfillment_time',
              'ps_variation 14 ps_variation_max_fullfillment_time',
              'ps_variation 14 ps_variation_stock',
              'ps_variation 14 ps_variation_size',
              'ps_variation 14 ps_variation_color',
              'ps_variation 14 ps_variation_shipping_fee',

              'ps_variation 15 ps_variation_price',
              'ps_variation 15 ps_variation_price_discount',
              'ps_variation 15 ps_variation_min_fullfillment_time',
              'ps_variation 15 ps_variation_max_fullfillment_time',
              'ps_variation 14 ps_variation_stock',
              'ps_variation 15 ps_variation_size',
              'ps_variation 15 ps_variation_color',
              'ps_variation 15 ps_variation_shipping_fee'
              ]
fieldnames_shopee = [
    'ps_category_list_id',
    'ps_product_name',
    'ps_product_description',
    'ps_price',  #
    'ps_stock',
    'ps_product_weight',
    'ps_days_to_ship',  #
    'ps_sku_ref_no_parent',
    'ps_mass_upload_variation_help',
    'ps_variation 1 ps_variation_sku',
    'ps_variation 1 ps_variation_name',  #
    'ps_variation 1 ps_variation_price',
    'ps_variation 1 ps_variation_stock',
    'ps_variation 2 ps_variation_sku',
    'ps_variation 2 ps_variation_name',
    'ps_variation 2 ps_variation_price',
    'ps_variation 2 ps_variation_stock',
    'ps_variation 3 ps_variation_sku',
    'ps_variation 3 ps_variation_name',
    'ps_variation 3 ps_variation_price',
    'ps_variation 3 ps_variation_stock',
    'ps_variation 4 ps_variation_sku',
    'ps_variation 4 ps_variation_name',
    'ps_variation 4 ps_variation_price',
    'ps_variation 4 ps_variation_stock',
    'ps_variation 5 ps_variation_sku',
    'ps_variation 5 ps_variation_name,'
    'ps_variation 5 ps_variation_price',
    'ps_variation 5 ps_variation_stock',
    'ps_variation 6 ps_variation_sku',
    'ps_variation 6 ps_variation_name',
    'ps_variation 6 ps_variation_price',
    'ps_variation 6 ps_variation_stock',
    'ps_variation 7 ps_variation_sku',
    'ps_variation 7 ps_variation_name',
    'ps_variation 7 ps_variation_price',
    'ps_variation 7 ps_variation_stock',
    'ps_variation 8 ps_variation_sku',
    'ps_variation 8 ps_variation_name',
    'ps_variation 8 ps_variation_price',
    'ps_variation 8 ps_variation_stock',
    'ps_variation 9 ps_variation_sku',
    'ps_variation 9 ps_variation_name',
    'ps_variation 9 ps_variation_price',
    'ps_variation 9 ps_variation_stock',
    'ps_variation 10 ps_variation_sku',
    'ps_variation 10 ps_variation_name',
    'ps_variation 10 ps_variation_price',
    'ps_variation 10 ps_variation_stock',
    'ps_variation 11 ps_variation_sku',
    'ps_variation 11 ps_variation_name',
    'ps_variation 11 ps_variation_price',
    'ps_variation 11 ps_variation_stock',
    'ps_variation 12 ps_variation_sku',
    'ps_variation 12 ps_variation_name',
    'ps_variation 12 ps_variation_price',
    'ps_variation 12 ps_variation_stock',
    'ps_variation 13 ps_variation_sku',
    'ps_variation 13 ps_variation_name',
    'ps_variation 13 ps_variation_price',
    'ps_variation 13 ps_variation_stock',
    'ps_variation 14 ps_variation_sku',
    'ps_variation 14 ps_variation_name',
    'ps_variation 14 ps_variation_price',
    'ps_variation 14 ps_variation_stock',
    'ps_variation 15 ps_variation_sku',
    'ps_variation 15 ps_variation_name',
    'ps_variation 15 ps_variation_price',
    'ps_variation 15 ps_variation_stock',
    'ps_img_1',
    'ps_img_2',
    'ps_img_3',
    'ps_img_4',
    'ps_img_5',
    'ps_img_6',
    'ps_img_7',
    'ps_img_8',
    'ps_img_9'
]


def get_sku_details(sku_json):
    """
    Get attributes from a specific sku page
    :param sku_json:
    :return sku:
    """

    sku = {}
    sku_json_keys = sku_json.keys()

    # Get rating and rating_count
    if "product_rating" in sku_json_keys:
        if "rating" in sku_json["product_rating"].keys():
            sku["ps_rating"] = sku_json["product_rating"]["rating"]

        if "rating_count" in sku_json["product_rating"].keys():
            sku["ps_rating_count"] = sku_json["product_rating"]["rating_count"]

    # Get images
    if "small_picture" in sku_json_keys:
        sku["ps_img_1"] = sku_json["small_picture"]
    if "extra_photo_urls" in sku_json_keys:
        for i in range(min(8, len(sku_json["extra_photo_urls"].keys()))):
            sku["ps_img_%s" % str(i + 2)] = sku_json["extra_photo_urls"][str(i + 1)]

    # Get other attributes
    sku["ps_sku_ref_no_parent"] = str(sku_json["id"])
    sku["ps_url"] = sku_url_base % sku_json["id"]
    sku['ps_product_name'] = sku_json["name"].encode('utf-8')
    sku["ps_seller"] = sku_json["commerce_product_info"]["variations"][0]["merchant"].encode('utf-8')

    if "total_inventory" in sku_json["commerce_product_info"].keys():
        sku["ps_stock"] = int(sku_json["commerce_product_info"]["total_inventory"])

    if "num_bought" in sku_json_keys:
        sku["ps_num_bought"] = sku_json["num_bought"]

    if "brand" in sku_json_keys:
        sku["ps_brand"] = sku_json["brand"]

    if "description" in sku_json_keys:
        sku["ps_product_description"] = str(sku_json["description"].encode('utf-8'))

    if "gender" in sku_json_keys:
        sku["ps_gender"] = sku_json["gender"]

    if "merchant_rating" in sku_json["commerce_product_info"]["variations"][0].keys():
        sku["ps_seller_rating"] = sku_json["commerce_product_info"]["variations"][0]["merchant_rating"]

    # Get attributes corresponding to each variation
    variations = sku_json["commerce_product_info"]["variations"]
    for i in range(min(15, len(sku_json["commerce_product_info"]["variations"]))):
        sku["ps_variation %s ps_variation_price" % str(i + 1)] = float(variations[i]["retail_price"])

        # sku price  = min (prices of all variations)
        if "ps_price" not in sku:
            sku["ps_price"] = float(variations[i]["retail_price"])
        else:
            sku["ps_price"] = min(sku["ps_price"], float(variations[i]["retail_price"]))
        sku["ps_variation %s ps_variation_price_discount" % str(i + 1)] = variations[i]["price"]
        sku["ps_variation %s ps_variation_min_fullfillment_time" % str(i + 1)] = variations[i]["min_fulfillment_time"]

        # sku days to ship = max (minimum fullfillment time of all variations)
        if "ps_days_to_ship" not in sku:
            sku["ps_days_to_ship"] = int(variations[i]["min_fulfillment_time"])
        else:
            sku["ps_days_to_ship"] = max(sku["ps_days_to_ship"], int(variations[i]["min_fulfillment_time"]))

        sku["ps_variation %s ps_variation_max_fullfillment_time" % str(i + 1)] = variations[i]["max_fulfillment_time"]
        sku["ps_variation %s ps_variation_stock" % str(i + 1)] = int(variations[i]["inventory"])

        # Get size, if cannot, get color
        if "size" in variations[i].keys():
            sku["ps_variation %s ps_variation_size" % str(i + 1)] = variations[i]["size"]
            sku["ps_variation %s ps_variation_name" % str(i + 1)] = str(variations[i]["size"])
        if "color" in variations[i].keys():
            sku["ps_variation %s ps_variation_color" % str(i + 1)] = variations[i]["color"]
            if not sku["ps_variation %s ps_variation_name" % str(i + 1)]:
                sku["ps_variation %s ps_variation_name" % str(i + 1)] = str(variations[i]["color"])

        # Get Shipping fee
        sku["ps_variation %s ps_variation_shipping_fee" % str(i + 1)] = variations[i]["shipping"]

    return sku


def get_sku(sku_url, temp_writer):
    """
    Go to sku page
    :param sku_url:
    :return sku:
    """

    # Open a new browser
    browser_sku = webdriver.PhantomJS()
    # browser_sku = webdriver.Chrome('chromedriver')
    browser_sku.get(sku_url)

    # Check if connection is blocked
    script_content = browser_sku.find_elements_by_tag_name("script")[-2].get_attribute('innerHTML')
    while not script_content:
        print "Connection blocked. Retrying..."
        time.sleep(15)
        browser_sku.get(sku_url)
        script_content = browser_sku.find_elements_by_tag_name("script")[-2].get_attribute('innerHTML')

    # Get sku info from script json
    sku_json = json.loads(script_content.rsplit(";", 6)[0].split(" = ", 1)[1])
    browser_sku.quit()
    sku_dict = get_sku_details(sku_json)
    temp_writer.writerow(filter_sku_attributes(sku_dict, fieldnames))
    return sku_dict


def filter_sku_attributes(sku, fieldnames):
    """
    Filter the sku information based on the available field names
    :param sku:
    :param fieldnames:
    :return filtered:
    """

    filtered = {}
    for key in fieldnames:
        if key in sku:
            filtered[key] = sku[key]

        else:
            filtered[key] = None
    return filtered


def login(browser_main):
    """
    Login
    :param browser_main:
    :return:
    """
    browser_main.find_element_by_xpath("//div[@class='email-login-btn btn']").click()
    username_element = browser_main.find_element_by_id("login-email")
    password_element = browser_main.find_element_by_id("login-password")
    username_element.send_keys(username)
    password_element.send_keys(password)
    browser_main.find_element_by_xpath("//button[@class='submit-btn btn']").click()
    browser_main.set_window_size(500, 500)
    time.sleep(3)
    print "Successfully logined"


def main():
    """
    Main Function
    :return:
    """

    # Get user input
    no_skus = int(input("Please input number of skus to crawl: "))

    # Read seller name
    input_csv = open('%s\\Input\\Shop.csv' % path)
    seller_csv = csv.DictReader(input_csv)
    print "User input obtained"

    # Initialize temp file writer
    temp_writer = csv.DictWriter(open("%s\\temp.csv" % path, "wb"), fieldnames=fieldnames)
    temp_writer.writeheader()

    # Start Selenium
    browser_main = webdriver.PhantomJS()
    # browser_main = webdriver.Chrome('chromedriver')
    browser_main.get(wish_url)

    # User login
    login(browser_main)

    # Crawl info for each seller
    for seller in seller_csv:
        raw_dataframe = pd.DataFrame([])
        shopee_dataframe = pd.DataFrame([])
        raw_writer = pd.ExcelWriter("%s.xlsx" % seller["Name"])
        shopee_writer = pd.ExcelWriter("%s_shopee_format.xlsx" % seller["Name"])
        seller_url = seller_url_base % (seller["Name"])
        browser_main.get(seller_url)
        times_to_scroll = int((no_skus - 58) / 10) + 1

        # Scroll down the page to get more skus
        print "Start scrolling"
        for _ in range(times_to_scroll):
            browser_main.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
        sku_list = browser_main.find_elements_by_class_name("feed-product-item")
        print "Find %s skus to crawl" % min(no_skus, len(sku_list))

        # Crawl detailed information for each sku
        for i in range(min(no_skus, len(sku_list))):
            sku_url = sku_list[i].find_element_by_tag_name("a").get_attribute('href')
            print "Crawling data from %s ......" % sku_url
            sku = get_sku(sku_url, temp_writer)
            raw_dataframe = pd.concat([raw_dataframe, pd.DataFrame.from_dict([filter_sku_attributes(sku, fieldnames)])])
            shopee_dataframe = pd.concat(
                [shopee_dataframe, pd.DataFrame.from_dict([filter_sku_attributes(sku, fieldnames_shopee)])])
            # writer.writerow(filter_sku_attributes(sku, fieldnames))
            # writer_shopee_format.writerow(filter_sku_attributes(sku, fieldnames_shopee))
        raw_dataframe.to_excel(raw_writer, "Sheet1", index=False, encoding='utf8')
        shopee_dataframe.to_excel(shopee_writer, "Sheet1", index=False, encoding='utf8')

    # Close files and browser
    raw_writer.close()
    shopee_writer.close()
    # output_csv.close()
    input_csv.close()
    # output_csv_shopee.close()
    browser_main.service.process.send_signal(signal.SIGTERM)
    browser_main.quit()


main()
