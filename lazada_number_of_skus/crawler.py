from selenium import webdriver
from selenium.webdriver import ChromeOptions
import csv

# Please put all level2 and level3 categories that do not need to crawl
# To change level 1 category, please change get_level1 and get_leve2_level3 function
level2_excluding_list = [
    "Latest Tech in Town",
    "Lazada Gaming Zone",
    "Electronic Accessories",
    "Express Electronics",
    "Top",
    "TOP",
    "Promotion",
    "Click For Taobao",
    "%",
    "Trends",
    "TREND",
    "brand",
    "BRAND",
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
    "PARTNER OFFERS",
    "below RM",
    "RM",
    "Buying Guide"
]

# Lazada url
lazada_url_sg = "https://www.lazada.sg"
lazada_url_id = "https://www.lazada.co.id"
lazada_url_my = "https://www.lazada.com.my"
lazada_url_ph = "https://www.lazada.com.ph"

# Disable image for Chrome
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
    Get Level 1 Category Name
    :param browser:
    :return:
    """

    level1_list = browser.find_elements_by_class_name('l-main-navigation__item_style_default')
    if country == 'id':

        # Tabao Collection is at the last tab
        taobao = browser.find_element_by_class_name(
            'l-main-navigation__item_style_bold-orange').find_element_by_tag_name(
            'span').text.encode('utf-8')
        level1_text_list = []
        for level1 in level1_list:
            level1_text_list.append(level1.find_element_by_tag_name('span').text.encode('utf-8'))
        level1_text_list.append(taobao)

    elif country == 'my':

        # Last tab does not need to be crawled
        level1_text_list = []
        for level1 in level1_list:
            level1_text_list.append(level1.find_element_by_tag_name('span').text.encode('utf-8'))
        level1_text_list = level1_text_list[:len(level1_text_list) - 1]
        level1_text_list = []

    elif country == 'sg':

        # Taobao collection is at first tab
        taobao = browser.find_element_by_class_name(
            'l-main-navigation__item_style_bold-orange').find_element_by_tag_name(
            'span').text.encode('utf-8')
        level1_text_list = [taobao]
        for level1 in level1_list:
            level1_text_list.append(level1.find_element_by_tag_name('span').text.encode('utf-8'))
    else:  # ph
        level1_text_list = []
        for level1 in level1_list:
            level1_text_list.append(level1.find_element_by_tag_name('span').text.encode('utf-8'))
    return level1_text_list


def get_count(browser, url, crawl_review=True):
    """
    Get Number of skus and number of reviews for a category
    :param browser:
    :param url:
    :return:
    """

    browser.get(url)
    prev_length = 200  # number of skus with reviews at last page, Should be greater than 120

    # Try to find the number of skus
    try:
        cat = browser.find_element_by_class_name('c-catalog-nav__item_highlighted')
        count = cat.find_element_by_tag_name('span').text.replace("(", "").replace(")", "")
    except:
        count = -1

    num_of_reviews = 0
    page = 0

    # Try to get the maximum page available
    try:
        max_page = int(browser.find_element_by_class_name('c-paging__wrapper').find_elements_by_tag_name('a')[
                           -2].text)
    except:
        max_page = 1

    # Use maximum page number to guess total number of skus
    if count == -1:
        count = max_page * 120

    if crawl_review:
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
            # When both current page and previous page has less than 120 skus with reviews
            if len(review_list) < 60 and prev_length < 60:
                return count, -1

            # Get maximum 40 pages
            if page > 40:
                return count, num_of_reviews

            prev_length = len(review_list)

            # Sum all reviews
            for review in review_list:
                try:
                    num_of_reviews += int(review.text.split(" ")[0].replace("(", ""))
                except:
                    pass

            # Go to next page
            browser.get(url + "&page=%d" % (page + 1))
        print page
    return count, num_of_reviews


def get_level2_level3(browser, level1_text_list, country, writer, crawl_review=True):
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

        # Exclude the last category
        category_pane_list = category_pane_list[:len(category_pane_list) - 1]

    elif country == 'sg':

        # Retain the first category (taobao collection)
        # Exclude the second and third tab
        category_pane_list = [browser.find_element_by_class_name(
            'l-main-navigation__second-menu-item')] + browser.find_elements_by_class_name(
            'l-main-navigation__second-menu-item')[3:]
    else:  # ph

        # Exclude the first tab
        category_pane_list = browser.find_elements_by_class_name(
            'l-main-navigation__second-menu-item')[1:]

    level1_counter = 0
    count_browser = webdriver.Chrome("chromedriver", chrome_options=options)
    for level1 in level1_text_list:
        print "Getting %s ..." % level1
        columns = category_pane_list[level1_counter].find_elements_by_class_name('l-second-menu__column')
        level2 = "Default Level2"
        has_level3 = False
        excluding_rest = False
        prev_cat_class = ""
        cat_class = ""
        cat_url = ""
        prev_cat_url = ""

        for column in columns:
            level2_and_level3 = column.find_elements_by_class_name('l-second-menu__item')
            for cat in level2_and_level3:
                cat_name = cat.find_element_by_tag_name('a').get_attribute('data-tracking-nav-sub').encode('utf-8')

                if in_excluding_list(cat_name):
                    excluding_rest = True  # Excluding the following category if this category is excluded
                    continue

                cat_url = cat.find_element_by_tag_name('a').get_attribute('href') + "/?itemperpage=120&sort=ratingdesc"
                cat_class = cat.get_attribute('class')
                print cat_name

                if "heading1" in cat_class:
                    if "heading1" in prev_cat_class:  # Two consecutive heading1, means previous heading1 need to be handled
                        count = get_count(count_browser, prev_cat_url, crawl_review)
                        writer.writerow([level1, level2, "", count[0], count[1]])
                    excluding_rest = False
                    level2 = cat_name
                    has_level3 = False
                elif "heading2" in cat_class:
                    has_level3 = True
                    level3 = cat_name
                    count = get_count(count_browser, cat_url, crawl_review)
                    writer.writerow([level1, level2, level3, count[0], count[1]])

                else:
                    if not has_level3 and not excluding_rest:
                        level3 = cat_name
                        count = get_count(count_browser, cat_url,crawl_review)
                        writer.writerow([level1, level2, level3, count[0], count[1]])
                prev_cat_class = cat_class
                prev_cat_url = cat_url

        # In case the last category is a level 2 category
        if "heading1" in cat_class:
            count = get_count(count_browser, cat_url, crawl_review)
            writer.writerow([level1, level2, "", count[0], count[1]])

        level1_counter += 1
    count_browser.quit()


def get_taobao_collection(browser, url, writer, crawl_review):
    browser.get(url + '/taobao-collection/')
    level2_browser = webdriver.Chrome("chromedriver", chrome_options=options)
    level3_browser = webdriver.Chrome("chromedriver", chrome_options=options)
    try:
        browser.find_element_by_class_name('c-catalog-nav__more-link').click()
    except:
        pass

    level2_cat_list = browser.find_element_by_class_name('c-catalog-nav__list').find_elements_by_tag_name('a')
    for level2 in level2_cat_list:
        level2_name = level2.text.encode('utf-8')
        level2_url = level2.get_attribute('href')
        level2_browser.get(level2_url)
        try:
            level2_browser.find_element_by_class_name('c-catalog-nav__more-link').click()
        except:
            pass
        level3_cat_list = level2_browser.find_element_by_class_name('c-catalog-nav__list').find_elements_by_tag_name(
            'a')

        for level3 in level3_cat_list:
            level3_url = level3.get_attribute('href') + '&itemperpage=120&sort=ratingdesc'
            level3_name = level3.text.encode('utf-8')
            print level3_name
            count = get_count(level3_browser, level3_url, crawl_review)
            writer.writerow(["Taobao Collection", level2_name, level3_name, count[0], count[1]])

    level2_browser.quit()
    level3_browser.quit()


def main():
    browser = webdriver.Chrome("chromedriver", chrome_options=options)
    country = raw_input("Please input the country code: ")
    crawl_review = raw_input("Please choose to crawl review or not (1 or 0): ")
    if crawl_review == "1":
        crawl_review = True
    else:
        crawl_review = False

    if country == 'id':
        lazada_url = lazada_url_id

    elif country == 'my':
        lazada_url = lazada_url_my
    elif country == 'sg':
        lazada_url = lazada_url_sg
    else:
        lazada_url = lazada_url_ph
    browser.get(lazada_url)

    print "Getting Level 1 Collections..."
    level1_text_list = get_level1(browser, country)
    print "Level 1 List Obtained !"

    with open('%s_result.csv' % country, 'wb') as file:
        writer = csv.writer(file)
        print "Getting Level 2 and level 3..."
        get_level2_level3(browser, level1_text_list, country, writer, crawl_review)
        if country == 'my' or country == 'ph':
            print "Getting Taobao Collection..."
            get_taobao_collection(browser, lazada_url, writer, crawl_review)
        print "All counts obtained"
        browser.quit()
        file.close()

main()
