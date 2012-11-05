# Scrapy settings for ehealth project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'ehealth'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['ehealth.spiders']
NEWSPIDER_MODULE = 'ehealth.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
DOWNLOAD_DELAY = 3
COOKIES_ENABLED = True
COOKIES_DEBUG = False
LOG_ENABLED = False
MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'test'
MONGODB_COLLECTION = 'ehealthrates'
MONGODB_UNIQ_KEY = ''
