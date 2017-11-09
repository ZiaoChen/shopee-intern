from selenium import webdriver
from selenium.webdriver import ChromeOptions
import pandas as pd
import time
import signal
from selenium.webdriver.common.action_chains import ActionChains
import csv

level1_excluding_list = [
    "Official Store",
    "Express Digital"
]

level2_excluding_list = [
    "Latest Tech in Town",
    "Lazada Gaming Zone",
    "Electronic Accessories",
    "Express Electronics",
    "Top ",
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
    "Best Seller",
    "New In!"
]

lazada_url = "https://www.lazada.sg"
options = ChromeOptions()
options.add_argument('--disable-popup-blocking')
options.add_experimental_option("prefs", {'profile.managed_default_content_settings.images': 2})


def in_excluding_list(name):
    for exclude_cat in level2_excluding_list:
        if exclude_cat in name:
            return True
    return False


def get_level1(browser):
    taobao = browser.find_element_by_class_name('l-main-navigation__item_style_bold-orange').find_elements_by_tag_name('span').text
    level1_list = browser.find_elements_by_class_name('l-main-navigation__item_style_default')
    level1_text_list = [taobao]
    for level1 in level1_list:
        level1_text_list.append(level1.find_element_by_tag_name('span').text)
    return level1_text_list


def get_count(browser, url):
    browser.get(url)
    prev_length = 200
    try:
        cat = browser.find_element_by_class_name('c-catalog-nav__item_highlighted')
        count = cat.find_element_by_tag_name('span').text.replace("(", "").replace(")", "")
    except:
        count = -1
    num_of_reviews = 0
    if count != -1:
        page = 0
        max_page = int(browser.find_element_by_class_name('c-paging__wrapper').find_elements_by_tag_name('a')[
                           -2].text)

        while 1:
            page += 1
            try:
                review_list = browser.find_elements_by_class_name('c-product-card__review-num')
            except:
                break
            if len(review_list) == 0 or page == max_page:
                break

            if len(review_list) < 120 and prev_length < 120:
                return count, -1

            prev_length = len(review_list)
            for review in review_list:
                try:
                    num_of_reviews += int(review.text.split(" ")[0].replace("(", ""))
                except:
                    pass

            browser.get(url + "&page=%d" % (page + 1))

        print page
    return count, num_of_reviews


def get_level2_level3(browser, level1_text_list):
    category_pane_list = browser.find_elements_by_class_name('l-main-navigation__second-menu-item')[3:]
    complete_category_dict = {}
    level1_counter = 0
    count_browser = webdriver.Chrome("chromedriver", chrome_options=options)
    for level1 in level1_text_list:
        print "Getting %s ..." % level1
        columns = category_pane_list[level1_counter].find_elements_by_class_name('l-second-menu__column')
        # has_level3 = False
        # try:
        #     category_pane_list[level1_counter].find_element_by_class_name('l-second-menu__item_style_heading2')
        #     has_level3 = True
        # except:
        #     pass
        level2 = "Default Level2"
        has_level3 = False
        complete_category_dict[level1] = {}
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
                    excluding_rest = True
                    continue

                cat_url = cat.find_element_by_tag_name('a').get_attribute('href') + "/?itemperpage=120&sort=ratingdesc"
                cat_class = cat.get_attribute('class')
                print cat_name
                if "heading1" in cat_class:
                    if "heading1" in prev_cat_class:
                        print prev_cat_url
                        complete_category_dict[level1][level2] = get_count(count_browser, prev_cat_url)
                    excluding_rest = False
                    level2 = cat_name
                    complete_category_dict[level1][level2] = {}
                    has_level3 = False
                elif "heading2" in cat_class:
                    has_level3 = True
                    level3 = cat_name
                    complete_category_dict[level1][level2][level3] = get_count(count_browser, cat_url)
                else:
                    if not has_level3 and not excluding_rest:
                        level3 = cat_name
                        complete_category_dict[level1][level2][level3] = get_count(count_browser, cat_url)
                prev_cat_class = cat_class
                prev_cat_url = cat_url
        if "heading1" in cat_class:
            complete_category_dict[level1][level2] = get_count(count_browser, cat_url)

        level1_counter += 1
    count_browser.quit()
    return complete_category_dict


def write_to_csv(all_dict):
    with open('result.csv', 'wb') as file:
        writer = csv.writer(file)
        writer.writerow(["Level1", "Level2", "Level3", "Counts", "Reviews"])
        for level1 in all_dict:
            for level2 in all_dict[level1]:
                if type(all_dict[level1][level2]) == dict:
                    if all_dict[level1][level2]:
                        for level3 in all_dict[level1][level2]:
                            if int(all_dict[level1][level2][level3][0]) > 0:
                                writer.writerow([level1, level2, level3, all_dict[level1][level2][level3][0],
                                                 all_dict[level1][level2][level3][1]])
                else:
                    if int(all_dict[level1][level2][0]) > 0:
                        writer.writerow([level1, level2, "", all_dict[level1][level2][0], all_dict[level1][level2][1]])


def main():
    browser = webdriver.Chrome("chromedriver", chrome_options=options)
    browser.get(lazada_url)

    print "Getting Level 1 Collections..."
    level1_text_list = get_level1(browser)
    print "Level 1 List Obtained !"

    print "Getting Level 2 and level 3..."
    complete_category_dict = get_level2_level3(browser, level1_text_list)
    print complete_category_dict
    print "All counts obtained"

    print "Writing to csv..."
    write_to_csv(complete_category_dict)
    browser.quit()


main()
