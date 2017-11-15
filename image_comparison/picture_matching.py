import csv
from collections import defaultdict
from PIL import Image
import imagehash
import ast
import Levenshtein
import time
import Queue
from io import BytesIO
import grequests
import threading
from collections import OrderedDict

input_file_path = 'input/input2.csv'
q = Queue.Queue()

counter = 0
dict_header = ['username', 'item_shopid', 'item_itemid', 'item_name', 'item_description', 'parent_sku', 'item_images',
               'item_price', 'item_stock', 'item_brand', 'item_shipping', 'item_cat', 'weight']


def format_url():
    sku = defaultdict(dict)
    fin = csv.DictReader(open("Input/input2.csv"))
    for row in fin:
        url = "http://f.shopee.com.my/file/"
        images = [url + x for x in row['item_images'].split(",")]
        sku[row['item_shopid']][row['item_itemid']] = images
    return sku


def get_image(plist):
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
    return result


def get_image_parallel(iid, plist):
    global q
    global counter
    result = []
    result_dict = {}

    rs = (grequests.get(u) for u in plist)
    rs_list = grequests.map(rs)
    for rs in rs_list:
        while 1:
            try:
                image = Image.open(BytesIO(rs.content))
                hash = str(imagehash.average_hash(image))
                result.append(hash)
                break
            except:
                print rs.url
                print "Try Again"
                time.sleep(2)
    counter = counter + 1
    print counter
    result_dict[iid] = result
    q.put(result_dict)


def download_image(sid, url, parallel=False):
    global q

    h = {}
    writer = csv.writer(open('%s.csv' % sid, 'wb'))
    writer.writerow(['Product ID', 'Hash Value'])
    threads = []
    counter = 0
    for iid, plist in url.items():
        # start = time.time()
        if not parallel:
            counter = counter + 1
            print counter
            image = get_image(plist)
            if image:
                h[iid] = image
        else:
            threads.append(threading.Thread(target=get_image_parallel, args=(iid, plist)))
            if (len(threads) == 50):
                for thread in threads:
                    thread.start()
                for thread in threads:
                    thread.join()
                threads = []
                while q.qsize():
                    image_dict = q.get()
                    if image_dict:
                        h.update(image_dict)
    if threads:
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        while q.qsize():
            image_dict = q.get()
            if image_dict:
                h.update(image_dict)

    for k, v in h.items():
        writer.writerow([k, v])


def item_similarity(a, b):
    # result = 100
    num_of_zero = 0
    if len(a) > len(b):
        c = a
        a = b
        b = c

    b_temp = b[:]
    for i in a:
        d_min = float("inf")
        for j in b_temp:
            d = Levenshtein.distance(i, j)
            if d < d_min:
                d_min = d
        if d_min == 0:
            num_of_zero += 1
    if num_of_zero > 1:
        return True
    else:
        return False


def get_hashed_string(sid):
    hashed = {}
    f = csv.reader(open('%s.csv' % sid, 'rb'))
    f.next()
    for row in f:
        hashed[row[0]] = list(sorted(set(ast.literal_eval(row[1]))))

    # return OrderedDict(sorted(hashed.items(), key=lambda t: len(str(sorted(t[1])))))
    return hashed


def get_item_id_image(sid, file, dup_list):
    sku = defaultdict(dict)

    for row in file:
        if row['item_shopid'] == sid and row["parent_sku"] not in dup_list:
            sku[row['item_itemid']] = list(sorted(set(row['item_images'].split(','))))
    return sku


def get_item_id_image_url(sid, file, dup_list):
    sku = defaultdict(dict)
    url = "http://f.shopee.com.my/file/"
    for row in file:
        if row['item_shopid'] == sid and row["parent_sku"] not in dup_list:
            images = [url + x for x in row['item_images'].split(",")]
            sku[row['item_itemid']] = list(sorted(set(images)))
    return sku


def product_match(shop_a, shop_b, writer):
    shop_b_original = dict(shop_b)
    not_match_list = []
    for i in shop_a:
        d_min = float("inf")
        count = 0
        for j in shop_b_original:
            d = item_similarity(shop_a[i], shop_b_original[j])
            count += 1
            if d:
                d_min = 0
                print "Find at %d" % count
                break
        if d_min != 0:
            not_match_list.append(i)
    return not_match_list


def remove_duplicate(shop):
    image_str_list = []
    for itemid, image_list in shop.items():
        item_image_str = str(sorted(image_list))
        if item_image_str in image_str_list:
            del shop[itemid]
        else:
            image_str_list.append(item_image_str)
    return shop


def get_duplicate_parent_sku_list(sid1, sid2, file):
    duplicate_parent_sku_list = set()
    parent_sku_list = set()
    for row in file:
        if row["item_shopid"] == sid1 and row["parent_sku"]:
            parent_sku_list.add(row["parent_sku"])

    for row in file:
        if row["item_shopid"] == sid2 and row["parent_sku"] in parent_sku_list:
            duplicate_parent_sku_list.add(row["parent_sku"])
    print "Number of Duplicate Skus: %d" % len(duplicate_parent_sku_list)
    return list(duplicate_parent_sku_list)


def get_shop_id(file):
    shop_id_list = set()
    for row in file:
        shop_id_list.add(row["item_shopid"])
    return list(shop_id_list)


start = time.time()
file = list(csv.DictReader(open(input_file_path)))
shop_id_list = get_shop_id(file)
writer = csv.DictWriter(open('Result.csv', 'wb'), fieldnames=dict_header)

dup_list = get_duplicate_parent_sku_list(shop_id_list[0], shop_id_list[1], file)

shop_a = get_item_id_image(shop_id_list[0], file, dup_list)
shop_b = get_item_id_image(shop_id_list[1], file, dup_list)

# if len(shop_a) < len(shop_b):
#     temp = shop_a
#     shop_a = shop_b
#     shop_b = temp
#     temp = shop_id_list[0]
#     shop_id_list[0] = shop_id_list[1]
#     shop_id_list[1] = temp

writer.writeheader()
shop_b = remove_duplicate(shop_b)
not_match_list = product_match(shop_a, shop_b, writer)
for row in file:
    if row["item_itemid"] in not_match_list:
        writer.writerow(row)
print "The program takes: %s" % str(time.time() - start)
