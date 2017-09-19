import csv
import sys
import os
import requests
import time
import pandas as pd

reload(sys)
sys.setdefaultencoding('UTF8')
path = os.path.dirname(os.path.realpath(__file__))

base_url = 'http://www.lazada.%s/mobapi/%s/?sort=name&dir=asc&page=%s&maxitems=400'

output_path = "output.csv"

# field_names = ['id', 'name', 'sku', 'url', 'description', 'price', 'special_price', 'rating', 'brand', 'categories',
#                'seller_name', 'size', 'weight',
#                'img_1', 'img_2', 'img_3', 'img_4', 'img_5', 'img_6', 'img_7', 'img_8', 'img_9',
#                'v1_attribute_set_name',
#                'v1_min_delivery_time', 'v1_price', 'v1_special_price', 'v1_quantity', 'v1_shipping_weight', 'v1_sku',
#                'v2_attribute_set_name',
#                'v2_min_delivery_time', 'v2_price', 'v2_special_price', 'v2_quantity', 'v2_shipping_weight', 'v2_sku',
#                'v3_attribute_set_name',
#                'v3_min_delivery_time', 'v3_price', 'v3_special_price', 'v3_quantity', 'v3_shipping_weight', 'v3_sku',
#                'v4_attribute_set_name',
#                'v4_min_delivery_time', 'v4_price', 'v4_special_price', 'v4_quantity', 'v4_shipping_weight', 'v4_sku',
#                'v5_attribute_set_name',
#                'v5_min_delivery_time', 'v5_price', 'v5_special_price', 'v5_quantity', 'v5_shipping_weight', 'v5_sku',
#                'v6_attribute_set_name',
#                'v6_min_delivery_time', 'v6_price', 'v6_special_price', 'v6_quantity', 'v6_shipping_weight', 'v6_sku',
#                'v7_attribute_set_name',
#                'v7_min_delivery_time', 'v7_price', 'v7_special_price', 'v7_quantity', 'v7_shipping_weight', 'v7_sku',
#                'v8_attribute_set_name',
#                'v8_min_delivery_time', 'v8_price', 'v8_special_price', 'v8_quantity', 'v8_shipping_weight', 'v8_sku',
#                'v9_attribute_set_name',
#                'v9_min_delivery_time', 'v9_price', 'v9_special_price', 'v9_quantity', 'v9_shipping_weight', 'v9_sku',
#                'v10_attribute_set_name',
#                'v10_min_delivery_time', 'v10_price', 'v10_special_price', 'v10_quantity', 'v10_shipping_weight',
#                'v10_sku',
#                'v11_attribute_set_name',
#                'v11_min_delivery_time', 'v11_price', 'v11_special_price', 'v11_quantity', 'v11_shipping_weight',
#                'v11_sku',
#                'v12_attribute_set_name',
#                'v12_min_delivery_time', 'v12_price', 'v12_special_price', 'v12_quantity', 'v12_shipping_weight',
#                'v12_sku',
#                'v13_attribute_set_name',
#                'v13_min_delivery_time', 'v13_price', 'v13_special_price', 'v13_quantity', 'v13_shipping_weight',
#                'v13_sku',
#                'v14_attribute_set_name',
#                'v14_min_delivery_time', 'v14_price', 'v14_special_price', 'v14_quantity', 'v14_shipping_weight',
#                'v14_sku',
#                'v15_attribute_set_name',
#                'v15_min_delivery_time', 'v15_price', 'v15_special_price', 'v15_quantity', 'v15_shipping_weight',
#                'v15_sku']

field_names = [
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


def main():
    mode = int(input("Please choose the mode 1 (predefine file name) or mode 2 (user define file name): "))
    if mode == 1:
        input_csv = get_input_file('%s\\Input\\Seller.csv' % path)
        output_path = input("Please enter the file name: ")
        output_csv = get_output_file(output_path, field_names)
        output_csv.writeheader()
        pages_to_crawl = 12
        for seller in input_csv:
            for page_num in range(1, pages_to_crawl + 1):
                seller_url = base_url % (get_url(seller["Country"]), seller["Name"], page_num)
                print seller_url
                crawl_single_seller(seller_url=seller_url, output_csv=output_csv)

    else:
        seller = raw_input("Please input seller's name in the url: ")
        country = raw_input("Please input seller's country: ")
        pages_to_crawl = int(input("Please input the number of pages to crawl: "))
        excel_writer = pd.ExcelWriter(seller + ".xlsx")
        whole_dataframe = pd.DataFrame([])
        for page_num in range(1, pages_to_crawl + 1):
            seller_url = base_url % (get_url(country), seller, page_num)
            print seller_url
            whole_dataframe = pd.concat([whole_dataframe, crawl_single_seller(seller_url=seller_url)])
        whole_dataframe = whole_dataframe[field_names]
        whole_dataframe["ps_product_description"] = whole_dataframe["ps_product_description"].str.encode('utf-8')
        whole_dataframe["ps_product_name"] = whole_dataframe["ps_product_name"].str.encode('utf-8')
        whole_dataframe['ps_variation 1 ps_variation_name'] = whole_dataframe["ps_variation 1 ps_variation_name"].str.encode('utf-8')
        whole_dataframe['ps_variation 2 ps_variation_name'] = whole_dataframe["ps_variation 2 ps_variation_name"].str.encode('utf-8')
        whole_dataframe['ps_variation 3 ps_variation_name'] = whole_dataframe["ps_variation 3 ps_variation_name"].str.encode('utf-8')
        whole_dataframe['ps_variation 4 ps_variation_name'] = whole_dataframe["ps_variation 4 ps_variation_name"].str.encode('utf-8')
        whole_dataframe['ps_variation 5 ps_variation_name'] = whole_dataframe["ps_variation 5 ps_variation_name"].str.encode('utf-8')
        whole_dataframe['ps_variation 6 ps_variation_name'] = whole_dataframe["ps_variation 6 ps_variation_name"].str.encode('utf-8')
        whole_dataframe['ps_variation 7 ps_variation_name'] = whole_dataframe["ps_variation 7 ps_variation_name"].str.encode('utf-8')
        whole_dataframe['ps_variation 8 ps_variation_name'] = whole_dataframe["ps_variation 8 ps_variation_name"].str.encode('utf-8')
        whole_dataframe['ps_variation 9 ps_variation_name'] = whole_dataframe["ps_variation 9 ps_variation_name"].str.encode('utf-8')
        whole_dataframe['ps_variation 10 ps_variation_name'] = whole_dataframe["ps_variation 10 ps_variation_name"].str.encode('utf-8')
        whole_dataframe['ps_variation 11 ps_variation_name'] = whole_dataframe["ps_variation 11 ps_variation_name"].str.encode('utf-8')
        whole_dataframe['ps_variation 12 ps_variation_name'] = whole_dataframe["ps_variation 12 ps_variation_name"].str.encode('utf-8')
        whole_dataframe['ps_variation 13 ps_variation_name'] = whole_dataframe["ps_variation 13 ps_variation_name"].str.encode('utf-8')
        whole_dataframe['ps_variation 14 ps_variation_name'] = whole_dataframe["ps_variation 14 ps_variation_name"].str.encode('utf-8')
        whole_dataframe['ps_variation 15 ps_variation_name'] = whole_dataframe["ps_variation 15 ps_variation_name"].str.encode('utf-8')
        whole_dataframe = whole_dataframe.drop_duplicates()
        whole_dataframe.to_excel(excel_writer, 'Sheet1', index=False)
        excel_writer.save()


def crawl_single_seller(seller_url):
    while True:
        try:
            response = requests.get(seller_url)
            break
        except:
            print "Connection blocked. Retrying..."
            time.sleep(15)
    sku_list = response.json()["metadata"]["results"]
    counter = 0
    page_dataframe = pd.DataFrame([])
    for sku_raw in sku_list:
        counter += 1
        sku = sku_raw["data"]
        processed_sku = dict()
        processed_sku["id"] = sku_raw["id"]
        processed_sku["ps_product_name"] = sku["name"].replace("\n", "")
        processed_sku["ps_sku_ref_no_parent"] = str(sku["sku"])
        processed_sku["ps_url"] = sku["url"].replace("/mobapi", "")
        processed_sku["ps_product_description"] = sku["description"].replace("\n", "")
        processed_sku["ps_price"] = float(sku["price"])
        if "special_price" in sku:
            processed_sku["special_price"] = float(sku["special_price"])

        if "ratings_total" in sku:
            processed_sku["rating"] = sku["ratings_total"]["avr"]
        else:
            processed_sku["rating"] = "No Rating"
        processed_sku["brand"] = sku["brand"]
        processed_sku["ps_category_list_id"] = str("[" + ",".join(sku["categories"]) + "]")
        if "images" in sku_raw:
            for i in range(0, min(len(sku_raw["images"]), 9)):
                processed_sku["ps_img_%s" % str(i + 1)] = "".join(sku_raw["images"][i]["path"].rsplit("-catalog", 1))
        variations = sku["simples"].keys()
        processed_sku["ps_days_to_ship"] = 0
        processed_sku["ps_stock"] = 0
        try:
            if len(variations) > 1:
                for i in range(0, min(15, len(variations))):
                    processed_sku["v%s_attribute_set_name" % str(i + 1)] = sku["simples"][variations[i]]["meta"][
                        "attribute_set_name"]
                    processed_sku["v%s_min_delivery_time" % str(i + 1)] = int(sku["simples"][variations[i]]["meta"][
                                                                                  "min_delivery_time"])
                    processed_sku["ps_variation %s ps_variation_price" % str(i + 1)] = float(
                        sku["simples"][variations[i]]["meta"]["price"])

                    if "special_price" in sku["simples"][variations[i]]["meta"]:
                        processed_sku["v%s_special_price" % str(i + 1)] = sku["simples"][variations[i]]["meta"][
                            "special_price"]
                    processed_sku["ps_variation %s ps_variation_stock" % str(i + 1)] = int(
                        sku["simples"][variations[i]]["meta"]["quantity"])
                    processed_sku["v%s_shipping_weight" % str(i + 1)] = sku["simples"][variations[i]]["meta"][
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
            processed_sku["seller_name"] = sku_details["attributes"]["taobao_seller_name"]
        else:
            processed_sku["seller_name"] = sku_details["supplierName"]
        if "product_measures" in sku_details["attributes"]:
            processed_sku["size"] = sku_details["attributes"]["product_measures"]
        if "product_weight" in sku_details["attributes"]:
            processed_sku["ps_product_weight"] = float(sku_details["attributes"]["product_weight"])

        processed_sku_filtered = {}
        for key in field_names:
            if key in processed_sku:
                processed_sku_filtered[key] = processed_sku[key]
            else:
                processed_sku_filtered[key] = None

        page_dataframe = pd.concat([page_dataframe, pd.DataFrame.from_dict([processed_sku_filtered])])
    return page_dataframe


def get_url(name):
    if name == "Singapore":
        return "sg"
    elif name == "Indonesia":
        return "co.id"
    elif name == "Malaysia":
        return "com.my"


def get_input_file(input_path):
    return csv.DictReader(open(input_path))


def get_output_file(output_path, output_fieldname):
    return csv.DictWriter(open(output_path, "wb"), fieldnames=output_fieldname)


main()
