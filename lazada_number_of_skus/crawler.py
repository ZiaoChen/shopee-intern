from selenium import webdriver
from selenium.webdriver import ChromeOptions
import pandas as pd
import time
import signal
from selenium.webdriver.common.action_chains import ActionChains
import csv


level2_excluding_list = [
    "Latest Tech in Town",
    "Lazada Gaming Zone",
    "Electronic Accessories",
    "Express Electronics",
    "Top",
    "Promotion",
    "Click For Taobao",
    "%",
    "Trends",
    "TREND",
    "brand",
    "Food Vouchers",
    "Build your own PC",
    "Daily tech essentials",
    "Taobao Collection",
    "New Lazada Pharmacy",
    "Official Store",
    "BEST SELLER",
    "New In!",
    "Free Shipping for Orders Above $20",
    "Promo",
    "PARTNER OFFERS"
]

lazada_url_sg = "https://www.lazada.sg"
lazada_url_id = "https://www.lazada.co.id"
lazada_url_my = "https://www.lazada.com.my"
options = ChromeOptions()
options.add_argument('--disable-popup-blocking')
options.add_experimental_option("prefs", {'profile.managed_default_content_settings.images': 2})


def in_excluding_list(name):
    """
    Check Whether the category is in the excluding list
    :param name:
    :return:
    """
    for exclude_cat in level2_excluding_list:
        if exclude_cat in name:
            return True
    return False


def get_level1(browser, country):
    """
    Get Level 1 Category
    :param browser:
    :return:
    """

    level1_list = browser.find_elements_by_class_name('l-main-navigation__item_style_default')
    if country == 'id':
        taobao = browser.find_element_by_class_name(
            'l-main-navigation__item_style_bold-orange').find_element_by_tag_name(
            'span').text.encode('utf-8')
        level1_text_list = []
        for level1 in level1_list:
            level1_text_list.append(level1.find_element_by_tag_name('span').text.encode('utf-8'))
        level1_text_list.append(taobao)

    elif country == 'my':
        level1_text_list = []
        for level1 in level1_list:
            level1_text_list.append(level1.find_element_by_tag_name('span').text.encode('utf-8'))
        level1_text_list = level1_text_list[:len(level1_text_list)-1]

    else:
        taobao = browser.find_element_by_class_name(
            'l-main-navigation__item_style_bold-orange').find_element_by_tag_name(
            'span').text.encode('utf-8')
        level1_text_list = [taobao]
        for level1 in level1_list:
            level1_text_list.append(level1.find_element_by_tag_name('span').text.encode('utf-8'))
    return level1_text_list


def get_count(browser, url):
    """
    Get Number of skus and number of reviews for a category
    :param browser:
    :param url:
    :return:
    """

    browser.get(url)
    prev_length = 200  # Should be greater than 120

    # Try to find the number of skus
    try:
        cat = browser.find_element_by_class_name('c-catalog-nav__item_highlighted')
        count = cat.find_element_by_tag_name('span').text.replace("(", "").replace(")", "")
    except:
        count = -1

    num_of_reviews = 0
    # if count != -1:
    page = 0

    # Try to get the maximum page available
    try:
        max_page = int(browser.find_element_by_class_name('c-paging__wrapper').find_elements_by_tag_name('a')[
                           -2].text)
    except:
        max_page = 1

    if count == -1:
        count = max_page*120

    while 1:
        page += 1
        try:
            review_list = browser.find_elements_by_class_name('c-product-card__review-num')
        except:
            break

        # No more skus or no sku has review
        if len(review_list) == 0 or page == max_page:
            break

        # Cannot sort by ratings
        if len(review_list) < 60 and prev_length < 60:
            return count, -1

        if page > 40:
            print page
            return count, num_of_reviews

        prev_length = len(review_list)

        # Sum all reviews
        for review in review_list:
            try:
                num_of_reviews += int(review.text.split(" ")[0].replace("(", ""))
            except:
                pass

        browser.get(url + "&page=%d" % (page + 1))
    print page
    return count, num_of_reviews


def get_level2_level3(browser, level1_text_list, country, writer):
    """
    Get level2 and level3 statistics
    :param browser:
    :param level1_text_list:
    :return:
    """
    if country == 'id':
        category_pane_list = browser.find_elements_by_class_name(
            'l-main-navigation__second-menu-item')


    elif country == 'my':
        category_pane_list = browser.find_elements_by_class_name(
            'l-main-navigation__second-menu-item')
        category_pane_list = category_pane_list[:len(category_pane_list)-1]
    else:
        category_pane_list = [browser.find_element_by_class_name(
            'l-main-navigation__second-menu-item')] + browser.find_elements_by_class_name(
            'l-main-navigation__second-menu-item')[3:]

    # complete_category_dict = {}
    level1_counter = 0
    count_browser = webdriver.Chrome("chromedriver", chrome_options=options)
    for level1 in level1_text_list:
        print "Getting %s ..." % level1
        columns = category_pane_list[level1_counter].find_elements_by_class_name('l-second-menu__column')
        level2 = "Default Level2"
        has_level3 = False
        # complete_category_dict[level1] = {}
        excluding_rest = False
        prev_cat_class = ""
        cat_class = ""
        cat_url = ""
        prev_cat_url = ""

        for column in columns:
            level2_and_level3 = column.find_elements_by_class_name('l-second-menu__item')
            for cat in level2_and_level3:
                cat_name = cat.find_element_by_tag_name('a').get_attribute('data-tracking-nav-sub')

                if in_excluding_list(cat_name):
                    excluding_rest = True  # Excluding the following category if this category is excluded
                    continue

                cat_url = cat.find_element_by_tag_name('a').get_attribute('href') + "/?itemperpage=120&sort=ratingdesc"
                cat_class = cat.get_attribute('class')
                print cat_name

                if "heading1" in cat_class:
                    if "heading1" in prev_cat_class:  # Two consecutive heading1, means previous heading1 need to be handled
                        # complete_category_dict[level1][level2] = get_count(count_browser, prev_cat_url)
                        count = get_count(count_browser, prev_cat_url)
                        writer.writerow([level1, level2, "", count[0], count[1]])
                    excluding_rest = False
                    level2 = cat_name.encode('utf-8')
                    # complete_category_dict[level1][level2] = {}
                    has_level3 = False
                elif "heading2" in cat_class:
                    has_level3 = True
                    level3 = cat_name.encode('utf-8')
                    try:
                        # complete_category_dict[level1][level2][level3] = get_count(count_browser, cat_url)
                        count = get_count(count_browser, cat_url)
                        writer.writerow([level1, level2, level3, count[0], count[1]])

                        # writer.close()
                    except:
                        # complete_category_dict[level1][level2] = get_count(count_browser, cat_url)
                        count = get_count(count_browser, cat_url)
                        writer.writerow([level1, level2, "", count[0], count[1]])
                else:
                    if not has_level3 and not excluding_rest:
                        level3 = cat_name
                        count = get_count(count_browser, cat_url)
                        writer.writerow([level1, level2, level3, count[0], count[1]])
                        # complete_category_dict[level1][level2][level3] = get_count(count_browser, cat_url)
                prev_cat_class = cat_class
                prev_cat_url = cat_url
        if "heading1" in cat_class:
            # complete_category_dict[level1][level2] = get_count(count_browser, cat_url)
            count = get_count(count_browser, cat_url)
            writer.writerow([level1, level2, "", count[0], count[1]])

        level1_counter += 1
    count_browser.quit()
    # return complete_category_dict


def get_taobao_collection(browser, url, writer):
    browser.get(url + '/taobao-collection/')
    # complete_dict["Taobao Collection"] = {}
    level2_browser = webdriver.Chrome("chromedriver", chrome_options=options)
    level3_browser = webdriver.Chrome("chromedriver", chrome_options=options)
    level2_cat_list = browser.find_element_by_class_name('c-catalog-nav__list').find_elements_by_tag_name('a')
    for level2 in level2_cat_list:
        level2_name = level2.text.encode('utf-8')
        level2_url = level2.get_attribute('href')
        level2_browser.get(level2_url)
        level3_cat_list = level2_browser.find_element_by_class_name('c-catalog-nav__list').find_elements_by_tag_name(
            'a')
        # complete_dict["Taobao Collection"][level2_name] = {}

        for level3 in level3_cat_list:
            level3_url = level3.get_attribute('href') + '&itemperpage=120&sort=ratingdesc'
            level3_name = level3.text.encode('utf-8')
            print level3_name
            count = get_count(level3_browser, level3_url)
            writer.writerow(["Taobao Collection", level2_name, level3_name, count[0], count[1]])
            # complete_dict["Taobao Collection"][level2_name][level3_name] = get_count(level3_browser, level3_url)

    level2_browser.quit()
    level3_browser.quit()
    # return complete_dict


def write_to_csv(all_dict, country):
    """
    Write the statistics to csv
    :param all_dict:
    :return:
    """

    with open('%s_result.csv' % country, 'wb') as file:
        writer = csv.writer(file)
        writer.writerow(["Level1", "Level2", "Level3", "Counts", "Reviews"])
        for level1 in all_dict:
            for level2 in all_dict[level1]:
                if type(all_dict[level1][level2]) == dict:
                    if all_dict[level1][level2]:
                        for level3 in all_dict[level1][level2]:
                            if int(all_dict[level1][level2][level3][0]) > 0:
                                writer.writerow([level1.encode('utf-8'), level2.encode('utf-8'), level3.encode('utf-8'),
                                                 all_dict[level1][level2][level3][0],
                                                 all_dict[level1][level2][level3][1]])
                else:
                    if int(all_dict[level1][level2][0]) > 0:
                        writer.writerow([level1, level2, "", all_dict[level1][level2][0], all_dict[level1][level2][1]])


def main():

    browser = webdriver.Chrome("chromedriver", chrome_options=options)
    country = raw_input("Please input the country code: ")
    if country == 'id':
        lazada_url = lazada_url_id

    elif country == 'my':
        lazada_url = lazada_url_my
    else:
        lazada_url = lazada_url_sg
    browser.get(lazada_url)

    print "Getting Level 1 Collections..."
    level1_text_list = get_level1(browser, country)
    print "Level 1 List Obtained !"

    with open('%s_result.csv' % country, 'wb') as file:
        writer = csv.writer(file)

        print "Getting Level 2 and level 3..."
        get_level2_level3(browser, level1_text_list, country, writer)
        if country == 'my' or country == 'ph':
            print "Getting Taobao Collection..."
            get_taobao_collection(browser, lazada_url, writer)

        print "All counts obtained"

        # print "Writing to csv..."
        # write_to_csv(complete_category_dict, country)
        browser.quit()



main()
