# -*- coding: utf-8 -*-

# Scrapy settings for wish_crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'wish_crawler'

SPIDER_MODULES = ['wish_crawler.spiders']
NEWSPIDER_MODULE = 'wish_crawler.spiders'
LOG_LEVEL = 'INFO'
FEED_EXPORT_ENCODING = 'utf-8'
FEED_EXPORTERS = {
    'csv': 'wish_crawler.spiders.csv_item_exporter.WishCsvItemExporter',
}

FIELDS_TO_EXPORT = [
    'name',
    'url',
    'rating',
    'rating_count',
    'seller',
    'seller_rating',
    'img_1',
    'img_2',
    'img_3',
    'img_4',
    'img_5',
    'img_6',
    'img_7',
    'img_8',
    'img_9',
    'id',
    'total_inventory',
    'num_bought',
    'brand',
    'description',
    'v1_price',
    'v1_price_discount',
    'v1_min_fullfillment_time',
    'v1_max_fullfillment_time',
    'v1_inventory',
    'v1_size',
    'v1_color',
    'v1_shipping_fee',
    'v2_price',
    'v2_price_discount',
    'v2_min_fullfillment_time',
    'v2_max_fullfillment_time',
    'v2_inventory',
    'v2_size',
    'v2_color',
    'v2_shipping_fee',
    'v3_price',
    'v3_price_discount',
    'v3_min_fullfillment_time',
    'v3_max_fullfillment_time',
    'v3_inventory',
    'v3_size',
    'v3_color',
    'v3_shipping_fee',
    'v4_price',
    'v4_price_discount',
    'v4_min_fullfillment_time',
    'v4_max_fullfillment_time',
    'v4_inventory',
    'v4_size',
    'v4_color',
    'v4_shipping_fee',
    'v5_price',
    'v5_price_discount',
    'v5_min_fullfillment_time',
    'v5_max_fullfillment_time',
    'v5_inventory',
    'v5_size',
    'v5_color',
    'v5_shipping_fee',
    'v6_price',
    'v6_price_discount',
    'v6_min_fullfillment_time',
    'v6_max_fullfillment_time',
    'v6_inventory',
    'v6_size',
    'v6_color',
    'v6_shipping_fee',

    'v7_price',
    'v7_price_discount',
    'v7_min_fullfillment_time',
    'v7_max_fullfillment_time',
    'v7_inventory',
    'v7_size',
    'v7_color',
    'v7_shipping_fee',

    'v8_price',
    'v8_price_discount',
    'v8_min_fullfillment_time',
    'v8_max_fullfillment_time',
    'v8_inventory',
    'v8_size',
    'v8_color',
    'v8_shipping_fee',

    'v9_price',
    'v9_price_discount',
    'v9_min_fullfillment_time',
    'v9_max_fullfillment_time',
    'v9_inventory',
    'v9_size',
    'v9_color',
    'v9_shipping_fee',

    'v10_price',
    'v10_price_discount',
    'v10_min_fullfillment_time',
    'v10_max_fullfillment_time',
    'v10_inventory',
    'v10_size',
    'v10_color',
    'v10_shipping_fee',

    'v11_price',
    'v11_price_discount',
    'v11_min_fullfillment_time',
    'v11_max_fullfillment_time',
    'v11_inventory',
    'v11_size',
    'v11_color',
    'v11_shipping_fee',

    'v12_price',
    'v12_price_discount',
    'v12_min_fullfillment_time',
    'v12_max_fullfillment_time',
    'v12_inventory',
    'v12_size',
    'v12_color',
    'v12_shipping_fee',

    'v13_price',
    'v13_price_discount',
    'v13_min_fullfillment_time',
    'v13_max_fullfillment_time',
    'v13_inventory',
    'v13_size',
    'v13_color',
    'v13_shipping_fee',

    'v14_price',
    'v14_price_discount',
    'v14_min_fullfillment_time',
    'v14_max_fullfillment_time',
    'v14_inventory',
    'v14_size',
    'v14_color',
    'v14_shipping_fee',

    'v15_price',
    'v15_price_discount',
    'v15_min_fullfillment_time',
    'v15_max_fullfillment_time',
    'v15_inventory',
    'v15_size',
    'v15_color',
    'v15_shipping_fee'
]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'wish_crawler (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'wish_crawler.middlewares.WishCrawlerSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'wish_crawler.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'wish_crawler.pipelines.WishCrawlerPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
