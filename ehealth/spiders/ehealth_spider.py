from scrapy.spider import BaseSpider
from scrapy.http import *
from scrapy.selector import HtmlXPathSelector
import time
import datetime
from ehealth.items import EhealthItem
from scrapy.mail import MailSender
from scrapy.conf import settings
import pymongo

class EhealthSpider(BaseSpider):
    name = "ehealth"
    allowed_domains = ["www.ehealthinsurance.com"]
    start_urls = [
    "http://www.ehealthinsurance.com/individual-family-health-insurance"   
    ]
    rates_url = ''
    request_count = 0

    def __init__(self, gender, year, smoker, rateparamid):
        self.gender = gender
        self.year = year
        self.smoker = smoker
        self.rateparamid = rateparamid
        self.datetime = datetime.datetime.utcnow()

    def parse(self, response):
        formdata = {
                    'census.requestEffectiveDate':'10/15/2012',
                    'census.primary.gender':self.gender,
                    'census.zipCode':'32952',
                    'census.primary.month':'10',
                    'census.primary.day':'29',
                    'census.primary.year':self.year,
                    'census.primary.tobacco':self.smoker,
                    'census.primary.student':'false'
        }

        return [FormRequest.from_response(response,
                formnumber = 1,
                formdata = formdata,
                callback = self.get_rates_url)]

    def get_rates_url(self, response):
        hxs = HtmlXPathSelector(response)
        noscripts = hxs.select('//noscript')
        url = noscripts[0].select('meta/@content').extract()
        url = 'http://' + self.allowed_domains[0]  + url[0][6:]
        self.rates_url = url
        return Request(url = self.rates_url, callback=self.get_rates)

    def get_rates(self, response):
        connection = pymongo.Connection(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        collection = db[settings['MONGODB_COLLECTION']]
        hxs = HtmlXPathSelector(response)
        planbundle = hxs.select('//form[contains(@id,"compareForm")]')
        plans = planbundle[0].select('div[contains(@class, "plan-unit")]')
        items = []
        for plan in plans:
            item = EhealthItem()
            planname = plan.select('.//a[contains(@class,"primary")]/text()').extract()
            plancost = plan.select('.//div[contains(@id, "monthly-cost")]/span/text()').extract()
            plancompany = plan.select('.//img[contains(@class,"planlogo_bdr")]/@title').extract()
            item['plancompany'] = plancompany[0]
            item['planname'] = planname[0]
            item['plancost'] = plancost[0]
             
            coinsurance = plan.select('.//div[contains(@class,"plan-info-list")]/ul/li[position()=3]/div/text()').extract()
            plan_details = plan.select('.//div[contains(@class,"plan-info-list")]/ul/li/div/div/text()').extract()
            item['plantype'] = plan_details[0]
            item['deductible'] = plan_details[1]
            item['officevisit'] = plan_details[2]
            item['rateparamid'] = self.rateparamid
            item['datetime'] = self.datetime
            item['coinsurance'] = coinsurance[1]
            collection.insert(dict(item))

            items.append(item)

        if not not items:
            print 'success'
