import os
# import grequests
import bs4
import requests
import json
import csv
import sys
import time

reload(sys)
sys.setdefaultencoding('UTF8')

path = os.path.dirname(os.path.realpath(__file__))

shops = []
shops_csv = csv.DictReader(open(path + '/Review_Scraping_Input.csv'))
for shops_row in shops_csv:
    shops.append(shops_row['Shop Name'])

fieldname = [u'shop', u'sku', u'age_restriction', u'max_saving_percentage', u'name', u'url', u'brand', u'special_price',
             u'price', u'new-product', u'categories', u'is_fast_delivery', u'max_special_price', u'max_price',
             u'simples', u'description', u'ratings_total', u'product_sticker', u'Category', u'shipping_weight',
             u'Product ID', u'# of Ratings', u'Avg Rating', u'Category ID']

f = csv.DictWriter(open("lazadaResult.csv", "wb"), fieldnames=fieldname)
# Write CSV Header, If you dont need that, remove this line
f.writeheader()

# ff = open('raw.txt', 'w')

for shop in shops:
    page = 1
    sku = 1
    # while page == 67:
    while (sku > 0) and (page <= 10):
        url = 'http://www.lazada.sg/mobapi/' + shop + '/?sort=name&dir=asc&page=' + str(page) + '&maxitems=200'
        # url = 'http://www.lazada.co.id/mobapi/tomtop_/?sort=name&dir=asc&page=' + str(page) + '&maxitems=300'
        print "Scraping from " + shop + " page = " + str(page)
        response = requests.get(url)
        soup = bs4.BeautifulSoup(response.text, 'html5lib').find('body').text
        a = json.loads(soup)
            #  print a["metadata"][u'results']
        try:
            sku = len(a["metadata"][u'results'])
            # print a["metadata"][u'results'][0][u'data'].keys()
        except:
            break
        k = []

        for i in range(0, sku):
            # if i == 133:
            ab = a["metadata"][u'results'][i][u'data'][u'description']
            print ab
                # break
                # ff.write(ab)
                # ff.close()
            # print i
            # k.append(a["metadata"][u'results'][i][u'data'])
            x = a["metadata"][u'results'][i][u'data']
            try:
                x[u'# of Ratings'] = x[u'ratings_total'][u'sum']
                x[u'Avg Rating'] = x[u'ratings_total'][u'avr']
            except:
                continue
            x[u'url'] = x[u'url'].replace("mobapi/", "")
            x[u'shop'] = shop
            x[u'Category'] = x[u'simples'][x[u'simples'].keys()[0]][u'meta'][u'attribute_set_name']
            x[u'shipping_weight'] = x[u'simples'][x[u'simples'].keys()[0]][u'meta'][u'shipping_weight']
            x[u'Product ID'] = x[u'simples'][x[u'simples'].keys()[0]][u'id_catalog_simple']
            x[u'Category ID'] = x[u'categories'][len(x[u'categories']) - 1]
            f.writerow(x)
            # print k[0].keys()

        page += 1
        print sku
        time.sleep(1)
