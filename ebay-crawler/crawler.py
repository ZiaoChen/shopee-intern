from ebaysdk.finding import Connection as Finding
from ebaysdk.shopping import Connection as Shopping
import csv
import sys
import pandas as pd

reload(sys)
sys.setdefaultencoding('UTF8')

# Config
ebay_app_id = 'ZiaoChen-SKUInfoR-PRD-65d8a3c47-36bbd3c7'
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
raw_field_names = [
    'id',
    'name',
    # 'sku',
    'category',
    'price',
    'seller_name',
    'seller_rating_score',
    'handling_time',
    'url',
    'quantity',
    'quantity_sold',
    'no_of_view',
    'seller_positive_feedback_percent',
    'description',
    'v1_name',
    'v1_price',
    'v1_quantity_sold',
    'v2_name',
    'v2_price',
    'v2_quantity_sold',
    'v3_name',
    'v3_price',
    'v3_quantity_sold',
    'v4_name',
    'v4_price',
    'v4_quantity_sold',
    'v5_name',
    'v5_price',
    'v5_quantity_sold',
    'v6_name',
    'v6_price',
    'v6_quantity_sold',
    'v7_name',
    'v7_price',
    'v7_quantity_sold',
    'v8_name',
    'v8_price',
    'v8_quantity_sold',
    'v9_name',
    'v9_price',
    'v9_quantity_sold',
    'v10_name',
    'v10_price',
    'v10_quantity_sold',
    'v11_name',
    'v11_price',
    'v11_quantity_sold',
    'v12_name',
    'v12_price',
    'v12_quantity_sold',
    'v13_name',
    'v13_price',
    'v13_quantity_sold',
    'v14_name',
    'v14_price',
    'v14_quantity_sold',
    'v15_name',
    'v15_price',
    'v15_quantity_sold',
    'img_1',
    'img_2',
    'img_3',
    'img_4',
    'img_5',
    'img_6',
    'img_7',
    'img_8',
    'img_9'
]
no_of_images = 9
no_of_variations = 15


def get_country(country_name):
    """
    Function to return the country code based on country name
    :param country_name:
    :return:
    """
    country_code_list = {

        'United States': 'EBAY-US',
        'Canada': 'EBAY-ENCA',
        'UK': 'EBAY-GB',
        'Australia': 'EBAY-AU',
        'Austria': 'EBAY-AT',
        'Belgium (French)': 'EBAY-FRBE',
        'France': 'EBAY-FR',
        'Germany': 'EBAY-DE',
        'Motors': 'EBAY-MOTOR',
        'Italy': 'EBAY-IT',
        'Belgium(Dutch)': 'EBAY-NLBE',
        'Netherlands': 'EBAY-NL',
        'Spain': 'EBAY-ES',
        'Switzerland': 'EBAY-CH',
        'Hong Kong': 'EBAY-HK',
        'India': 'EBAY-IN',
        'Ireland': 'EBAY-IE',
        'Malaysia': 'EBAY-MY',
        'Canada(French)': 'EBAY-FRCA',
        'Philippines': 'EBAY-PH',
        'Poland': 'EBAY-PL',
        'Singapore': 'EBAY-SG'
    }
    if country_name in country_code_list:
        return country_code_list[country_name]
    else:
        print "No country code available for %s" % country_name
        sys.exit()


def get_csv_writer(filename, fieldnames):
    """
    Get CSV Writer
    :param filename:
    :param fieldnames:
    :return:
    """
    return csv.DictWriter(open(filename, "wb"), fieldnames=fieldnames)


def get_user_input():
    """
    Return user input value
    :return:
    """

    store_name = raw_input("Please input shop name: ")
    country_code = get_country(raw_input("Please input country name: "))
    pages_to_crawl = int(input("Please input the number of pages to crawl (Each page 100 items):"))
    return (store_name, country_code, pages_to_crawl)


def filter_sku_id(response):
    """
    Filter sku id from the repsonse
    :param response:
    :return:
    """

    sku_id_list = []
    sku_list = response["searchResult"]["item"]
    print sku_list
    for sku in sku_list:
        sku_id_list.append(sku["itemId"])
    return sku_id_list


def get_sku_id_list(store_name, pages_to_crawl):
    """
    Get all sku ids in a given store
    :param response:
    :return:
    """

    sku_id_list = []
    for page in range(1, pages_to_crawl + 1):
        response = api_finding.execute('findItemsIneBayStores', {
            'storeName': store_name,
            'paginationOutput': {
                'pageNumber': page
            },
            'itemFilter': {
                'name': 'HideDuplicateItems',
                'value': True
            }
        })

        # Combine sku ids from all pages
        if not sku_id_list:
            sku_id_list = filter_sku_id(response.dict())
        else:
            sku_id_list.extend(filter_sku_id(response.dict()))
    return sku_id_list


def parse_sku_details_shopee(details, variations, descriptions):
    """
    Parse sku details from the api response and write specific fields to csv
    :param details:
    :param variations:
    :param descriptions:
    :param shopee_writer:
    :return:
    """
    whole_dataframe = pd.DataFrame([])
    for sku, sku_variation, sku_description in zip(details, variations, descriptions):
        sku_dict = dict()

        sku_dict["ps_product_name"] = str(sku["Title"])
        sku_dict["ps_url"] = sku["ViewItemURLForNaturalSearch"]
        sku_dict["ps_stock"] = int(sku["Quantity"])
        sku_dict["ps_price"] = float(sku["ConvertedCurrentPrice"]['value'])
        sku_dict["ps_days_to_ship"] = int(sku["HandlingTime"])
        if "Description" in sku_description:
            sku_dict["ps_product_description"] = str(sku_description["Description"])

        if 'PictureURL' in sku:
            for i in range(min(no_of_images, len(sku["PictureURL"]))):
                sku_dict["ps_img_%s" % str(i + 1)] = sku["PictureURL"][i]

        if "Variations" in sku_variation:
            if "Variation" in sku_variation["Variations"]:
                sku_variation_list = sku_variation["Variations"]["Variation"]
                for i in range(min(no_of_variations, len(sku_variation_list))):

                    # In case it just has one variation attribute
                    if type(sku_variation_list[i]["VariationSpecifics"]["NameValueList"]) is list:
                        sku_dict["ps_variation %s ps_variation_name" % str(i + 1)] = ' '.join(
                            [attribute['Value'] for attribute in
                             sku_variation_list[i]["VariationSpecifics"]["NameValueList"]])
                    else:
                        sku_dict["ps_variation %s ps_variation_name" % str(i + 1)] = \
                            str(sku_variation_list[i]["VariationSpecifics"]["NameValueList"]['Value'])
                    sku_dict["ps_variation %s ps_variation_price" % str(i + 1)] = float(sku_variation_list[i]["StartPrice"][
                        'value'])

        # Fill in the values for the keys that not in the api
        sku_filtered = {}
        for key in shopee_field_names:
            if key in sku_dict:
                sku_filtered[key] = sku_dict[key]
            else:
                sku_filtered[key] = None

        whole_dataframe = pd.concat([whole_dataframe, pd.DataFrame.from_dict([sku_filtered])])
    return whole_dataframe


def parse_sku_details_raw(details, variations, descriptions, raw_writer):
    """
    Parse sku details from the api response and write all fields to csv
    :param details:
    :param variations:
    :param descriptions:
    :param raw_writer:
    :return:
    """
    for sku, sku_variation, sku_description in zip(details, variations, descriptions):
        sku_dict = dict()

        sku_dict["id"] = sku["ItemID"]
        sku_dict["name"] = sku["Title"]
        sku_dict["url"] = sku["ViewItemURLForNaturalSearch"]
        sku_dict["category"] = sku["PrimaryCategoryName"]
        sku_dict["seller_name"] = sku["Seller"]["UserID"]
        sku_dict["quantity_sold"] = sku["QuantitySold"]
        sku_dict["quantity"] = sku["Quantity"]
        sku_dict["price"] = sku["ConvertedCurrentPrice"]['value']
        sku_dict["no_of_view"] = sku["HitCount"]
        sku_dict["handling_time"] = sku["HandlingTime"]
        if "Description" in sku_description:
            sku_dict["description"] = sku_description["Description"]
        # if "SKU" in sku:
        #     sku_dict["sku"] = sku["SKU"].encode('utf-8')
        if "FeedbackScore" in sku["Seller"]:
            sku_dict["seller_rating_score"] = sku["Seller"]["FeedbackScore"]
        if "PositiveFeedbackPercent" in sku["Seller"]:
            sku_dict["seller_positive_feedback_percent"] = sku["Seller"]["PositiveFeedbackPercent"]

        if 'PictureURL' in sku:
            for i in range(min(no_of_images, len(sku["PictureURL"]))):
                sku_dict["img_%s" % str(i + 1)] = sku["PictureURL"][i]

        if "Variations" in sku_variation:
            if "Variation" in sku_variation["Variations"]:
                sku_variation_list = sku_variation["Variations"]["Variation"]
                for i in range(min(no_of_variations, len(sku_variation_list))):
                    if type(sku_variation_list[i]["VariationSpecifics"]["NameValueList"]) is list:
                        sku_dict["v%s_name" % str(i + 1)] = ' '.join([attribute['Value'] for attribute in
                                                                      sku_variation_list[i]["VariationSpecifics"][
                                                                          "NameValueList"]])
                    else:
                        sku_dict["v%s_name" % str(i + 1)] = \
                            sku_variation_list[i]["VariationSpecifics"]["NameValueList"]['Value']
                    sku_dict["v%s_price" % str(i + 1)] = sku_variation_list[i]["StartPrice"]['value']
                    sku_dict["v%s_quantity_sold" % str(i + 1)] = sku_variation_list[i]["SellingStatus"]["QuantitySold"]
        raw_writer.writerow(sku_dict)


# Read user input and initialize writer
store_name, country_code, pages_to_crawl = get_user_input()
raw_writer = get_csv_writer("%s_raw.csv" % store_name, raw_field_names)
raw_writer.writeheader()
shopee_dataframe = pd.DataFrame([])

# Initialize API connection
api_finding = Finding(appid=ebay_app_id, config_file=None, siteid=country_code)
api_shopping = Shopping(appid=ebay_app_id, config_file=None, siteid=country_code)

# Find Item IDs in the store
sku_id_list = get_sku_id_list(store_name, pages_to_crawl)

if sku_id_list:
    times_to_query = int(len(sku_id_list) / 20)  # One time can only query 20 skus
    for i in range(times_to_query):
        # Get sku details
        response_sku = api_shopping.execute('GetMultipleItems', {'ItemID': sku_id_list[i * 20:(i + 1) * 20],
                                                                 'IncludeSelector': 'Details'}).dict()["Item"]

        # Get sku variations
        response_variations = api_shopping.execute('GetMultipleItems',
                                                   {'ItemID': sku_id_list[i * 20:(i + 1) * 20],
                                                    'IncludeSelector': 'Variations'}).dict()["Item"]

        # Get sku descriptions
        response_descriptions = api_shopping.execute('GetMultipleItems',
                                                     {'ItemID': sku_id_list[i * 20:(i + 1) * 20],
                                                      'IncludeSelector': 'TextDescription'}).dict()["Item"]

        # Parse the api response and store them into 2 files
        parse_sku_details_raw(details=response_sku, variations=response_variations, descriptions=response_descriptions,
                              raw_writer=raw_writer)
        shopee_dataframe = pd.concat([shopee_dataframe,
                                      parse_sku_details_shopee(details=response_sku, variations=response_variations,
                                                               descriptions=response_descriptions)])

    # In case there are skus that have not been crawled
    if times_to_query * 20 < len(sku_id_list):
        response_sku = api_shopping.execute('GetMultipleItems', {'ItemID': sku_id_list[times_to_query * 20:],
                                                                 'IncludeSelector': 'Details'}).dict()["Item"]
        response_variations = api_shopping.execute('GetMultipleItems',
                                                   {'ItemID': sku_id_list[times_to_query * 20:],
                                                    'IncludeSelector': 'Variations'}).dict()["Item"]
        parse_sku_details_raw(details=response_sku, variations=response_variations, descriptions=response_descriptions,
                              raw_writer=raw_writer)
        shopee_dataframe = pd.concat([shopee_dataframe,
                                      parse_sku_details_shopee(details=response_sku, variations=response_variations,
                                                               descriptions=response_descriptions)])
    excel_writer = pd.ExcelWriter(store_name + ".xlsx")
    shopee_dataframe = shopee_dataframe[shopee_field_names]
    shopee_dataframe.to_excel(excel_writer, 'Sheet1', index=False)
    excel_writer.save()
else:

    # In case this store has no skus
    print "Store %s does not have any available items" % store_name
