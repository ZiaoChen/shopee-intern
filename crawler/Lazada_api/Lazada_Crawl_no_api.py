# -*- coding: utf-8 -*-

import os
# import grequests
import bs4
import requests
import json
import csv
import sys
import time
import urllib2
import re
import unicodecsv


page = list(range(1,11))
seller_total = []
seller_page = []


def get_info(link):

    res = requests.get(link)
    res.encoding = 'utf-8'
    soup = bs4.BeautifulSoup(res.text, 'html5lib')

    s = soup.find('div', {'class': 'seller-details'}).find('div', {'class': 'basic-info__name'}).text.encode('utf8')
    # print s
    title = soup.find('h1', {'id': 'prod_title'}).text.strip().encode('utf8')
    # rr = soup.find('div', {'class': 'ratingNumberText'}).text.strip()
    # rr = re.findall(r'\d+', rr)
    # rating = rr[0]
    # review = rr[1]

    price_o = float(soup.find('span', {'id':'price_box'}).text.split(" ")[1][:-1])
    # print price_o
    price_d = float(soup.find('span', {'id':'special_price_box'}).text)
    # print price_o, price_d

    # print s, rr
    # return [title, s, rating, review, price_o, price_d]
    return [title, s, price_o, price_d]


# writer = csv.writer(open('seller_list.csv','wb'))
with open('sg_result_new.csv', 'wb') as f:
    f.write(u'\ufeff'.encode('utf8'))
    w = csv.writer(f)

    for p in page:
        #link = "http://www.lazada.sg/taobao-collection/?spm=a2o42.campaign-714.0.0.wuLFxN&dir=desc&page=" + str(p) + "&sc=IcoC&sort=ratingdesc"
        link = "http://www.lazada.sg/taobao-collection/?spm=a2o42.campaign-714.0.0.oW5MBl&dir=desc&itemperpage=120&page=" + str(p) + "&sc=IcoC&sort=ratingdesc"
        res = requests.get(link)
        print "Scraping from page " + str(p)
        soup = bs4.BeautifulSoup(res.text, 'html5lib')

        p_name = soup.find_all('div', {'class': 'c-product-card__description'})

        for p in p_name:
            # print p
            rating = float(p.find('div', {'class': 'c-rating-stars c-product-card__rating-stars '})['data-value'])
            review = p.find('div', {'class': 'c-product-card__review-num'}).text.split(" ")[0][1:]
            # print rating, review

            link = p.find('a')['href']
            p_link = "http://www.lazada.sg/taobao-collection/" + str(link)
            # print p_link

            data = get_info(p_link)
            # print data

            try:
                data = get_info(p_link)
                data.append(rating)
                data.append(review)
                data.append(p_link)
                w.writerow(data)
                # print data

            except:
                print 'bad'
                pass
