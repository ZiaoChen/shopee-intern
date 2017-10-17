import csv
from collections import defaultdict
import os
import urllib
from PIL import Image
import imagehash
import glob
from numpy import zeros
import ast
import Levenshtein
import time
import cStringIO
import Queue
import threading
from io import BytesIO
import requests
import multiprocessing
from multiprocessing.pool import ThreadPool
import grequests

count_global = 0
q = Queue.Queue()

def format_url():
    sku = defaultdict(dict)
    fin = csv.DictReader(open("Input/input.csv"))
    for row in fin:
        url = "http://f.shopee.com.my/file/"
        images = [url + x for x in row['images'].split(",")]
        sku[row['shopid']][row['itemid']] = images
    return sku


def get_image(plist):
    global count_global
    global q

    result = []
    try:
        rs = (grequests.get(u) for u in plist)
        rs_list = grequests.map(rs)
        for rs in rs_list:
            image = Image.open(BytesIO(rs.content))
            hash = str(imagehash.average_hash(image))
            result.append(hash)
    except:
        print "error occurs"
        pass
    count_global = count_global + 1
    print count_global
    return result


def download_image(sid, url):
    h = {}
    writer = csv.writer(open('%s.csv' % sid, 'wb'))
    writer.writerow(['Product ID', 'Hash Value'])
    # threads = []
    for iid, plist in url.items():
        # start = time.time()
        h[iid] = get_image(plist)
        # threads.append(threading.Thread(target=get_image_3, args=(iid, plist)))
        # if (len(threads) == 50):
        #     for thread in threads:
        #         thread.start()
        #     for thread in threads:
        #         thread.join()
        #     threads = []
        #     while q.qsize():
        #         image_dict = q.get()
        #         if image_dict:
        #             h.update(image_dict)
    for k, v in h.items():
        writer.writerow([k, v])



def item_similarity(a, b):
    a_avg = 0
    if len(a) > len(b):
        c = a
        a = b
        b = c

    b_temp = b[:]
    for i in a:
        d_min = float("inf")
        for j in b_temp:
            d = Levenshtein.distance(i, j)
            # d = wagner_fischer(i, j)
            if d < d_min:
                d_min = d
                temp = j
        b_temp.remove(temp)
        a_avg += d_min
    a_avg = float(a_avg / len(a))
    return a_avg


def get_hashed_string(sid):
    hashed = {}
    f = csv.reader(open('%s.csv' % sid, 'rb'))
    f.next()
    for row in f:
        hashed[row[0]] = list(set(ast.literal_eval(row[1])))

    return hashed


sku = format_url()
shop = sku.keys()

for s, i in sku.items():
    # dir = build_directory("%s" % s)
    download_image(s, i)
    # picture_hashing(s, dir)

writer = csv.writer(open('%s_%s.csv' % (shop[0],shop[1]), 'wb'))
writer.writerow(['Shop_%s' % shop[0], 'Shop_%s' % shop[1], 'Difference_score'])

shop_a = get_hashed_string(shop[0])
shop_b = get_hashed_string(shop[1])
paired = []
start = time.time()
shop_b_original = dict(shop_b)
shop_b_popped = dict()
counter = 0
for i in shop_a:
    d_min = float("inf")
    # d_min = 20
    pair_b = 0
    count = 0
    for j in shop_b_original:
        d = item_similarity(shop_a[i], shop_b_original[j])
        count += 1
        # print count
        if d == 0:
            pair_b = j
            d_min = 0

            # Remove if matched
            shop_b_popped[j] = shop_b_original[j]
            del shop_b_original[j]

            break

        elif d < d_min:
            d_min = d
            pair_b = j

    # Check popped list if cannot find match in remaining list
    if d_min != 0:
        for j in shop_b_popped:
            d = item_similarity(shop_a[i], shop_b_popped[j])
            if d < d_min:
                pair_b = j
                d_min = 0

    writer.writerow([i, pair_b, d_min])
    counter = counter + 1
    print counter
print time.time() - start
