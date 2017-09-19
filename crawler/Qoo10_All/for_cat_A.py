import requests, grequests, bs4
import csv, json, ast
import time
from datetime import datetime
from collections import defaultdict

# start_time = datetime.datetime.now()

# class for shop info
class ShopScraper(object):
    def __init__(self, res):
        self.url = None
        self.id = None
        self.soup = None
        self.res = res
        self.name = None
        self.cat_sku = {}
        self.follower = None
        self.rank = None
        self.sku = None
        self.contact = None
        self.search_request = None
        self.header = {'Accept-Encoding': 'gzip, deflate',
                       'Accept-Language': 'en-US,en;q=0.8',
                       'Connection': 'keep-alive',
                       'Host': 'list.qoo10.sg',
                       'Origin': 'http://list.qoo10.sg',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
                       }

    def get_soup(self):
        # type: () -> object
        # self.url = self.url.split("?")[0] + '?search_mode=basic'
        # res = requests.get(self.url, headers=self.header)
        self.soup = bs4.BeautifulSoup(self.res.text, 'html5lib')

    def get_url(self):
        self.url = self.soup.find('link', {'rel': 'canonical'})['href']

    def get_name(self):
        try:
            self.name = self.soup.find('a', {'class': 'name'}).text.encode('utf-8')
        except:
            self.name = -1

    def get_id(self):
        try:
            self.id = self.soup.find('input', {'id': 'sell_coupon_cust_no'})['value']
        except:
            self.id = -1

    def contact_scraper(self):
        if self.id == -1:
            self.contact = ['', '', '']
        else:
            self.search_request = {'enc_seller_cust_no': self.id, 'svc_nation_cd': 'SG',
                                   '___cache_expire___': '1479524022544'}
            payload = json.dumps(self.search_request)

            r = requests.post(
                url='http://www.qoo10.sg/gmkt.inc/swe_CSAjaxService.asmx/GetQpostSellerInfo',
                data=payload,
                headers={'Accept': '*/*',
                         'Accept-Encoding': 'gzip, deflate',
                         'Accept-Language': 'en-US,en;q=0.8',
                         'Connection': 'keep-alive',
                         'Content-Length': '107',
                         'Content-Type': 'application/json',
                         'Host': 'www.qoo10.sg',
                         'Origin': 'http://www.qoo10.sg',
                         'Referer': self.url,
                         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36}'
                         })
            s = bs4.BeautifulSoup(r.text, 'lxml')

            try:
                rows = ast.literal_eval(s.find('p').text)['d']['Rows'][0]
                self.contact = [rows['qphone_no'], rows['receive_call_phone_no'].replace('-', '')[1:],
                                rows['qtalk_qid']]
            except:
                self.contact = ['', '', '']

    def get_follower(self):
        try:
            self.follower = int(self.soup.find('span', {'class': 'flw_num'}).find('em').text.replace(',', ''))
        except:
            self.follower = ''

    def get_rank(self):
        try:
            self.rank = self.soup.find('div', {'class': 'rt_area'}).find('img')['alt']
        except:
            self.rank = " "

    def get_total_sku(self):
        try:
            self.sku = int(self.soup.find('li', {'id': 'tab_items'}).find('span', {'class': "num"}).text)
        except:
            self.sku = " "

    # get sub-cats and sku number
    def get_cat_sku(self):
        try:
            cats = self.soup.find('ul', {'id': 'category_result_list'}).find_all('li')
            for cat in cats:
                subcat = cat.find('a')['title'].encode('utf-8')
                self.cat_sku[subcat] = int(cat.find('a').find('strong').text.replace(',', ''))
        except:
            self.cat_sku = self.cat_sku


# class for sku info
# class for scraping sku info and patterns
# input should be the response returned from requests, get soup and url(reverese direction)

class SKUScraper(object):
    def __init__(self, res):
        self.id = None
        self.name = None
        self.url = None
        self.soup = None
        self.res = res
        self.shiprate = None
        self.qprice = None
        self.cprice = None
        self.review = None
        self.sold = None
        self.category = []
        self.search_request = None
        self.variation = []
        self.header = {'Accept-Encoding': 'gzip, deflate',
                       'Accept-Language': 'en-US,en;q=0.8',
                       'Connection': 'keep-alive',
                       'Host': 'list.qoo10.sg',
                       'Origin': 'http://list.qoo10.sg',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
                       }

    def get_soup(self):
        # self.url = self.url.split("?")[0] + '?search_mode=basic'
        # res = requests.get(self.url, headers=self.header)
        self.soup = bs4.BeautifulSoup(self.res.text, 'html5lib')

    def get_url(self):
        try:
            self.url = self.soup.find('link', {'rel': 'canonical'})['href']
        except:
            self.url = "NA"

    def get_sku_id(self):
        # print self.soup.find('input', {'id': 'gd_no'})['value']
        try:
            self.id = self.soup.find('input', {'name': 'gd_no'})['value']
        except:
            self.id = -1

    def get_sku_name(self):
        self.name = self.soup.find('h2', {'class': 'name', 'id': 'goods_name'}).text.encode('utf-8')

    def scrape_var(self):
        if self.id == -1:
            self.variation = []
        else:
            self.search_request = {"inventory_no": "ST" + str(self.id), "lang_cd": "en", "inventory_yn": "",
                                   "link_type": "N",
                                   "gd_no": str(self.id), "global_order_type": "L",
                                   "___cache_expire___": "1478791051620"}
            payload = json.dumps(self.search_request)

            r = requests.post(
                url='http://list.qoo10.sg/gmkt.inc/swe_GoodsAjaxService.asmx/GetGoodsInventoryAvailableList',
                data=payload,
                headers={'Accept-Encoding': 'gzip, deflate',
                         'Accept-Language': 'en-US,en;q=0.8',
                         'Connection': 'keep-alive',
                         'Content-Type': 'application/json',
                         'Host': 'list.qoo10.sg',
                         'Origin': 'http://list.qoo10.sg',
                         'Referer': self.url,
                         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
                         }
            )
            s = bs4.BeautifulSoup(r.text, 'lxml')
            try:
                rows = ast.literal_eval(s.find('p').text)['d']['Rows']
            except:
                rows = dict.fromkeys(['sel_value1', 'sel_value2', 'sel_item_price', 'inventory_cnt'], 0)

            for v in rows:
                a = v['sel_value1']
                b = v['sel_value2']
                p = v['sel_item_price']
                c = v['inventory_cnt']
                self.variation.append([a, b, p, c])

    def get_sold(self):
        self.sold = self.soup.find('span', {'class': 'sold'})
        # print int(self.soup.find('span', {'class': 'sold'}).text.split(' ')[0])

        if self.sold is None:
            self.sold = 0
        else:
            self.sold = int(self.sold.text.split(' ')[0])
            # print self.sold

    def get_review(self):
        try:
            self.review = int(self.soup.find('em', id="opinion_count_1").text.replace(',', ''))
        except:
            self.review = ''

    def get_cat(self):
        try:
            cat_list = self.soup.find_all('dd', {'itemprop': 'itemListElement'})
            for cat in cat_list:
                c = cat.find('span', {'itemprop': 'name'}).text
                self.category.append(c)
        except:
            self.category = self.category
            # print category

    def get_shiprate(self):
        shipfrom = self.soup.find('dl', {'class': 'detailsArea', 'name': 'shipping_panel_area'}).find('dd').text
        if shipfrom != 'Domestic':
            self.shiprate = self.soup.find('em', {'id': 'delivery_option_fee_0'}).text
        else:
            self.shiprate = ''
        try:
            self.shiprate = float(filter(unicode.isdigit, self.shiprate)) / 100
        except:
            self.shiprate = ''

    def get_price(self):
        groupbuy = self.soup.find('div', {'class': 'goods_type'})
        # print type(groupbuy)
        if groupbuy is None:
            self.qprice = self.soup.find('dl', {'class': 'detailsArea lsprice', 'id': 'dl_sell_price'}).find('dd').find(
                'strong').text
            try:
                self.cprice = self.soup.find('dl', {'class': 'detailsArea q_dcprice'}).find('dd').find('strong').text
            except:
                self.cprice = self.qprice
        else:
            self.qprice = self.soup.find('li', {'class': 'infoData groupbuy'}).find('dl').find('dd').find('del').text
            self.cprice = self.soup.find('li', {'class': 'infoData groupbuy'}).find('dl').find('dd').find('strong').text

        try:
            self.qprice = float(filter(unicode.isdigit, self.qprice)) / 100
            self.cprice = float(filter(unicode.isdigit, self.cprice)) / 100
        except:
            self.cprice = self.qprice


header = {'Accept-Encoding': 'gzip, deflate',
          'Accept-Language': 'en-US,en;q=0.8',
          'Connection': 'keep-alive',
          'Host': 'list.qoo10.sg',
          'Origin': 'http://list.qoo10.sg',
          'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
          }
category = {}
fin = csv.DictReader(open('Categories_A.csv', 'rb'))
for row in fin:
    category[row['Category']] = row['URL']

for k, v in category.items():

    sku_writer = csv.writer(open(k + '_sku_output.csv', 'wb'))
    shop_writer = csv.writer(open(k + '_shop_output.csv', 'wb'))

    item_count = 0
    shop_count = 0

    pmax = 10
    shop_link = []
    shop_list = []

    for page in range(pmax):

        # time.sleep(2)

        page_cat = v + '&curPage=' + str(page)


        try:
            res = requests.get(page_cat, headers=header)
            soup = bs4.BeautifulSoup(res.text, 'html5lib')
            items = soup.find_all('div', {'class': 'item_wrap'})
        except:
            continue

        sku_link = []
        shop_new_link = []

        print "Scraping from " + k + ", page " + str(page + 1)
        print "Current sku: " + str(item_count)
        print "Current shop: " + str(shop_count)
        print datetime.strftime(datetime.now(), "%Y-%m-%d, %H:%M:%S")

        for item in items:
            sku_link.append(item.find('a', {'class': 'tt'})['href'])
            shop = item.find('div', {'class': 'shop'}).find('a')['title']
            if shop not in shop_list:
                shop_list.append(shop)
                shop_new_link.append(
                    item.find('div', {'class': 'shop'}).find('a')['href'].split("?")[0] + '?search_mode=basic')

        for i in sku_link:
            sku_res = requests.get(i, headers=header)
            sku_info = SKUScraper(sku_res)
            item_count += 1
            # time.sleep(1)
            try:
                sku_info.get_soup()
                sku_info.get_url()
                sku_info.get_sku_name()
                sku_info.get_price()
                sku_info.get_sold()
                sku_info.get_shiprate()
                # print sku_info.name
                # sku.append(sku_info.name)
                sku = [sku_info.name, k, sku_info.url, sku_info.qprice, sku_info.sold, sku_info.shiprate]
                sku_writer.writerow(sku)
            except AttributeError:
                continue

        for j in shop_new_link:
            shop_res = requests.get(j, headers=header)
            shop_info = ShopScraper(shop_res)
            shop_count += 1
            # time.sleep(1)
            try:
                shop_info.get_soup()
                shop_info.get_url()
                shop_info.get_name()
                if shop_info.name != (-1):
                    shop_info.get_total_sku()
                    shop_info.get_follower()
                    shop_info.get_rank()
                    shop_info.get_id()
                    shop_info.contact_scraper()
                    # print shop_info.name
                    shop = [shop_info.name, k, shop_info.url, shop_info.sku, shop_info.follower, shop_info.rank] + shop_info.contact
                    # print shop
                    shop_writer.writerow(shop)
                    # print 'y'
            except AttributeError, e:
                print e
                continue
