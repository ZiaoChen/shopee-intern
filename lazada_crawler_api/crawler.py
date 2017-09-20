import csv
import sys
import os
import requests
import time
import pandas as pd

# Config
reload(sys)
sys.setdefaultencoding('UTF8')
path = os.path.dirname(os.path.realpath(__file__))
base_url = 'http://www.lazada.%s/mobapi/%s/?sort=name&dir=asc&page=%s&maxitems=400'
output_path = "output.csv"

raw_field_names = [
    'ps_id',
    'ps_url',
    'ps_category_list_id',
    'ps_product_name',
    'ps_product_description',
    'ps_price',
    'ps_stock',
    'ps_product_weight',
    'ps_days_to_ship',
    'ps_sku_ref_no_parent',
    'ps_seller_name',
    'ps_size',
    'ps_special_price',
    'ps_rating',
    'ps_brand',
    'ps_variation 1 ps_variation_sku',
    'ps_variation 1 ps_variation_name',
    'ps_variation 1 ps_variation_price',
    'ps_variation 1 ps_variation_stock',
    'ps_variation 1 attribute_set_name',
    'ps_variation 1 min_delivery_time',
    'ps_variation 1 special_price',
    'ps_variation 1 shipping_weight',
    'ps_variation 2 ps_variation_sku',
    'ps_variation 2 ps_variation_name',
    'ps_variation 2 ps_variation_price',
    'ps_variation 2 ps_variation_stock',
    'ps_variation 2 attribute_set_name',
    'ps_variation 2 min_delivery_time',
    'ps_variation 2 special_price',
    'ps_variation 2 shipping_weight',
    'ps_variation 3 ps_variation_sku',
    'ps_variation 3 ps_variation_name',
    'ps_variation 3 ps_variation_price',
    'ps_variation 3 ps_variation_stock',
    'ps_variation 3 attribute_set_name',
    'ps_variation 3 min_delivery_time',
    'ps_variation 3 special_price',
    'ps_variation 3 shipping_weight',
    'ps_variation 4 ps_variation_sku',
    'ps_variation 4 ps_variation_name',
    'ps_variation 4 ps_variation_price',
    'ps_variation 4 ps_variation_stock',
    'ps_variation 4 attribute_set_name',
    'ps_variation 4 min_delivery_time',
    'ps_variation 4 special_price',
    'ps_variation 4 shipping_weight',
    'ps_variation 5 ps_variation_sku',
    'ps_variation 5 ps_variation_name',
    'ps_variation 5 ps_variation_price',
    'ps_variation 5 ps_variation_stock',
    'ps_variation 5 attribute_set_name',
    'ps_variation 5 min_delivery_time',
    'ps_variation 5 special_price',
    'ps_variation 5 shipping_weight',
    'ps_variation 6 ps_variation_sku',
    'ps_variation 6 ps_variation_name',
    'ps_variation 6 ps_variation_price',
    'ps_variation 6 ps_variation_stock',
    'ps_variation 6 attribute_set_name',
    'ps_variation 6 min_delivery_time',
    'ps_variation 6 special_price',
    'ps_variation 6 shipping_weight',
    'ps_variation 7 ps_variation_sku',
    'ps_variation 7 ps_variation_name',
    'ps_variation 7 ps_variation_price',
    'ps_variation 7 ps_variation_stock',
    'ps_variation 7 attribute_set_name',
    'ps_variation 7 min_delivery_time',
    'ps_variation 7 special_price',
    'ps_variation 7 shipping_weight',
    'ps_variation 8 ps_variation_sku',
    'ps_variation 8 ps_variation_name',
    'ps_variation 8 ps_variation_price',
    'ps_variation 8 ps_variation_stock',
    'ps_variation 8 attribute_set_name',
    'ps_variation 8 min_delivery_time',
    'ps_variation 8 special_price',
    'ps_variation 8 shipping_weight',
    'ps_variation 9 ps_variation_sku',
    'ps_variation 9 ps_variation_name',
    'ps_variation 9 ps_variation_price',
    'ps_variation 9 ps_variation_stock',
    'ps_variation 9 attribute_set_name',
    'ps_variation 9 min_delivery_time',
    'ps_variation 9 special_price',
    'ps_variation 9 shipping_weight',
    'ps_variation 10 ps_variation_sku',
    'ps_variation 10 ps_variation_name',
    'ps_variation 10 ps_variation_price',
    'ps_variation 10 ps_variation_stock',
    'ps_variation 10 attribute_set_name',
    'ps_variation 10 min_delivery_time',
    'ps_variation 10 special_price',
    'ps_variation 10 shipping_weight',
    'ps_variation 11 ps_variation_sku',
    'ps_variation 11 ps_variation_name',
    'ps_variation 11 ps_variation_price',
    'ps_variation 11 ps_variation_stock',
    'ps_variation 11 attribute_set_name',
    'ps_variation 11 min_delivery_time',
    'ps_variation 11 special_price',
    'ps_variation 11 shipping_weight',
    'ps_variation 12 ps_variation_sku',
    'ps_variation 12 ps_variation_name',
    'ps_variation 12 ps_variation_price',
    'ps_variation 12 ps_variation_stock',
    'ps_variation 12 attribute_set_name',
    'ps_variation 12 min_delivery_time',
    'ps_variation 12 special_price',
    'ps_variation 12 shipping_weight',
    'ps_variation 13 ps_variation_sku',
    'ps_variation 13 ps_variation_name',
    'ps_variation 13 ps_variation_price',
    'ps_variation 13 ps_variation_stock',
    'ps_variation 13 attribute_set_name',
    'ps_variation 13 min_delivery_time',
    'ps_variation 13 special_price',
    'ps_variation 13 shipping_weight',
    'ps_variation 14 ps_variation_sku',
    'ps_variation 14 ps_variation_name',
    'ps_variation 14 ps_variation_price',
    'ps_variation 14 ps_variation_stock',
    'ps_variation 14 attribute_set_name',
    'ps_variation 14 min_delivery_time',
    'ps_variation 14 special_price',
    'ps_variation 14 shipping_weight',
    'ps_variation 15 ps_variation_sku',
    'ps_variation 15 ps_variation_name',
    'ps_variation 15 ps_variation_price',
    'ps_variation 15 ps_variation_stock',
    'ps_variation 15 attribute_set_name',
    'ps_variation 15 min_delivery_time',
    'ps_variation 15 special_price',
    'ps_variation 15 shipping_weight',
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
shopee_field_names = [
    'ps_url',
    'ps_category_list_id',
    'ps_product_name',
    'ps_product_description',
    'ps_price',
    'ps_stock',
    'ps_product_weight',
    'ps_days_to_ship',
    'ps_sku_ref_no_parent',
    'ps_mass_upload_variation_help',
    'ps_variation 1 ps_variation_sku',
    'ps_variation 1 ps_variation_name',
    'ps_variation 1 ps_variation_price',
    'ps_variation 1 ps_variation_stock',
    'ps_variation 1 ps_variation_attribute_set_name',
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
    'ps_variation 5 ps_variation_name',
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


def output_to_excel(whole_dataframe, seller):
    excel_writer = pd.ExcelWriter(seller + ".xlsx")
    whole_dataframe = whole_dataframe[shopee_field_names]

    # Change the encoding and write to excel
    whole_dataframe["ps_product_description"] = whole_dataframe["ps_product_description"].str.encode('utf-8')
    whole_dataframe["ps_product_name"] = whole_dataframe["ps_product_name"].str.encode('utf-8')
    whole_dataframe['ps_variation 1 ps_variation_name'] = whole_dataframe[
        "ps_variation 1 ps_variation_name"].str.encode('utf-8')
    whole_dataframe['ps_variation 2 ps_variation_name'] = whole_dataframe[
        "ps_variation 2 ps_variation_name"].str.encode('utf-8')
    whole_dataframe['ps_variation 3 ps_variation_name'] = whole_dataframe[
        "ps_variation 3 ps_variation_name"].str.encode('utf-8')
    whole_dataframe['ps_variation 4 ps_variation_name'] = whole_dataframe[
        "ps_variation 4 ps_variation_name"].str.encode('utf-8')
    whole_dataframe['ps_variation 5 ps_variation_name'] = whole_dataframe[
        "ps_variation 5 ps_variation_name"].str.encode('utf-8')
    whole_dataframe['ps_variation 6 ps_variation_name'] = whole_dataframe[
        "ps_variation 6 ps_variation_name"].str.encode('utf-8')
    whole_dataframe['ps_variation 7 ps_variation_name'] = whole_dataframe[
        "ps_variation 7 ps_variation_name"].str.encode('utf-8')
    whole_dataframe['ps_variation 8 ps_variation_name'] = whole_dataframe[
        "ps_variation 8 ps_variation_name"].str.encode('utf-8')
    whole_dataframe['ps_variation 9 ps_variation_name'] = whole_dataframe[
        "ps_variation 9 ps_variation_name"].str.encode('utf-8')
    whole_dataframe['ps_variation 10 ps_variation_name'] = whole_dataframe[
        "ps_variation 10 ps_variation_name"].str.encode('utf-8')
    whole_dataframe['ps_variation 11 ps_variation_name'] = whole_dataframe[
        "ps_variation 11 ps_variation_name"].str.encode('utf-8')
    whole_dataframe['ps_variation 12 ps_variation_name'] = whole_dataframe[
        "ps_variation 12 ps_variation_name"].str.encode('utf-8')
    whole_dataframe['ps_variation 13 ps_variation_name'] = whole_dataframe[
        "ps_variation 13 ps_variation_name"].str.encode('utf-8')
    whole_dataframe['ps_variation 14 ps_variation_name'] = whole_dataframe[
        "ps_variation 14 ps_variation_name"].str.encode('utf-8')
    whole_dataframe['ps_variation 15 ps_variation_name'] = whole_dataframe[
        "ps_variation 15 ps_variation_name"].str.encode('utf-8')
    whole_dataframe = whole_dataframe.drop_duplicates()
    whole_dataframe.to_excel(excel_writer, 'Sheet1', index=False)
    excel_writer.save()


def main():
    """
    Start the program
    :return:
    """
    mode = int(input("Please choose the mode 1 (predefine file name) or mode 2 (user define file name): "))
    if mode == 1:

        # Mode 1
        # Crawl seller based on CSV file
        input_csv = get_input_file('%s\\Input\\Seller.csv' % path)
        pages_to_crawl = 1

        for seller in input_csv:
            whole_dataframe = pd.DataFrame([])

            for page_num in range(1, pages_to_crawl + 1):
                seller_url = base_url % (get_url(seller["Country"]), seller["Name"], page_num)
                print seller_url
                whole_dataframe = pd.concat([whole_dataframe, crawl_single_seller(seller_url=seller_url,
                                                                                  csv_writer=get_output_file(
                                                                                      seller["Name"],
                                                                                      raw_field_names))])
            output_to_excel(whole_dataframe, seller["Name"])

    else:

        # Get user input
        seller = raw_input("Please input seller's name in the url: ")
        country = raw_input("Please input seller's country: ")
        pages_to_crawl = int(input("Please input the number of pages to crawl: "))

        # Initialize excel writer

        whole_dataframe = pd.DataFrame([])

        # Crawl the data
        for page_num in range(1, pages_to_crawl + 1):
            seller_url = base_url % (get_url(country), seller, page_num)
            print seller_url
            whole_dataframe = pd.concat([whole_dataframe, crawl_single_seller(seller_url=seller_url,
                                                                              csv_writer=get_output_file(seller,
                                                                                                         raw_field_names))])
        output_to_excel(whole_dataframe, seller)


def crawl_single_seller(seller_url, csv_writer):
    """
    Crawl single seller's information
    :param seller_url:
    :return:
    """
    while True:
        try:
            response = requests.get(seller_url)
            break
        except:
            print "Connection blocked. Retrying..."
            time.sleep(15)

    # Initialize variables
    sku_list = response.json()["metadata"]["results"]
    counter = 0
    page_dataframe = pd.DataFrame([])
    csv_writer.writeheader()

    for sku_raw in sku_list:
        counter += 1
        sku = sku_raw["data"]
        processed_sku = dict()
        processed_sku["ps_id"] = sku_raw["id"]
        processed_sku["ps_product_name"] = sku["name"].replace("\n", "")
        processed_sku["ps_sku_ref_no_parent"] = str(sku["sku"])
        processed_sku["ps_url"] = sku["url"].replace("/mobapi", "")
        processed_sku["ps_product_description"] = sku["description"].replace("\n", "")
        processed_sku["ps_price"] = float(sku["price"])
        if "special_price" in sku:
            processed_sku["ps_special_price"] = float(sku["special_price"])

        if "ratings_total" in sku:
            processed_sku["ps_rating"] = sku["ratings_total"]["avr"]
        else:
            processed_sku["ps_rating"] = "No Rating"
        processed_sku["ps_brand"] = sku["brand"]
        processed_sku["ps_category_list_id"] = str("[" + ",".join(sku["categories"]) + "]")
        if "images" in sku_raw:
            for i in range(0, min(len(sku_raw["images"]), 9)):
                processed_sku["ps_img_%s" % str(i + 1)] = "".join(sku_raw["images"][i]["path"].rsplit("-catalog", 1))
        variations = sku["simples"].keys()
        processed_sku["ps_days_to_ship"] = 0
        processed_sku["ps_stock"] = 0

        # Try to get variations
        try:
            if len(variations) > 1:
                for i in range(0, min(15, len(variations))):
                    processed_sku["ps_variation %s attribute_set_name" % str(i + 1)] = \
                        sku["simples"][variations[i]]["meta"][
                            "attribute_set_name"]
                    processed_sku["ps_variation %s min_delivery_time" % str(i + 1)] = int(
                        sku["simples"][variations[i]]["meta"][
                            "min_delivery_time"])
                    processed_sku["ps_variation %s ps_variation_price" % str(i + 1)] = float(
                        sku["simples"][variations[i]]["meta"]["price"])

                    if "special_price" in sku["simples"][variations[i]]["meta"]:
                        processed_sku["ps variation %s special_price" % str(i + 1)] = \
                            sku["simples"][variations[i]]["meta"][
                                "special_price"]
                    processed_sku["ps_variation %s ps_variation_stock" % str(i + 1)] = int(
                        sku["simples"][variations[i]]["meta"]["quantity"])
                    processed_sku["ps_variation %s shipping_weight" % str(i + 1)] = \
                        sku["simples"][variations[i]]["meta"][
                            "shipping_weight"]
                    processed_sku["ps_variation %s ps_variation_sku" % str(i + 1)] = str(
                        sku["simples"][variations[i]]["meta"]["sku"])
                    processed_sku["ps_stock"] += processed_sku["ps_variation %s ps_variation_stock" % str(i + 1)]
                    processed_sku["ps_days_to_ship"] = max(processed_sku["ps_days_to_ship"],
                                                           processed_sku["v%s_min_delivery_time" % str(i + 1)])

                    if "size" in sku["simples"][variations[i]]["attributes"]:
                        processed_sku["ps_variation %s ps_variation_name" % str(i + 1)] = str(
                            sku["simples"][variations[i]]["attributes"]["size"])
            else:
                processed_sku["ps_stock"] = int(
                    sku["simples"][variations[0]]["meta"]["quantity"])
                processed_sku["ps_days_to_ship"] = int(sku["simples"][variations[0]]["meta"][
                                                           "min_delivery_time"])
        except:
            pass

        # Go to sku page to get more information
        print sku["url"]
        while True:
            try:
                response_sku = requests.get(sku['url'])
                if not response_sku.json()["metadata"]["data"]:
                    print "Empty response. Retrying..."
                else:
                    break
            except:
                print "Connection Blocked. Retrying..."
                time.sleep(15)

        sku_details = response_sku.json()["metadata"]["data"]
        if sku_details["supplierName"] == "Taobao Collection" and "taobao_seller_name" in sku_details["attributes"]:
            processed_sku["ps_seller_name"] = sku_details["attributes"]["taobao_seller_name"]
        else:
            processed_sku["ps_seller_name"] = sku_details["supplierName"]
        if "product_measures" in sku_details["attributes"]:
            processed_sku["ps_size"] = sku_details["attributes"]["product_measures"]
        if "product_weight" in sku_details["attributes"]:
            processed_sku["ps_product_weight"] = float(sku_details["attributes"]["product_weight"])

        # Write to raw csv
        csv_writer.writerow(processed_sku)

        # Convert to Shopee format
        processed_sku_filtered = {}
        for key in shopee_field_names:
            if key in processed_sku:
                processed_sku_filtered[key] = processed_sku[key]
            else:
                processed_sku_filtered[key] = None

        page_dataframe = pd.concat([page_dataframe, pd.DataFrame.from_dict([processed_sku_filtered])])
    return page_dataframe


def get_url(name):
    """
    Get the country prefix for the url
    :param name:
    :return:
    """

    if name == "Singapore":
        return "sg"
    elif name == "Indonesia":
        return "co.id"
    elif name == "Malaysia":
        return "com.my"


def get_input_file(input_path):
    """
    Get input file
    :param input_path:
    :return:
    """

    return csv.DictReader(open(input_path))


def get_output_file(output_path, output_fieldname):
    """
    Get csv output writer
    :param output_path:
    :param output_fieldname:
    :return:
    """

    return csv.DictWriter(open(output_path+".csv", "wb"), fieldnames=output_fieldname)


main()
