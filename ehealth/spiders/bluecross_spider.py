from scrapy.spider import BaseSpider
from scrapy.http import *
from scrapy.selector import HtmlXPathSelector
import time
from ehealth.items import EhealthItem

class BluecrossSpider(BaseSpider):
    name = "bluecross"
    allowed_domains = ["consumerdirect.bcbsfl.com"]
    start_urls = [
    "http://consumerdirect.bcbsfl.com/cws/shopping/info"   
    ]

    def parse(self, response):
        return [FormRequest.from_response(response,
                   formnumber = 4,
                   formdata = {
                       'keycode':'8339',
                       'medicare_eligible':'no',
                       'dependents[0][relationship]':'A',
                       'dependents[0][gender]':'M',
                       'dependents[0][dateofbirth][date]':'10/29/1988',
                       'dependents[0][zipcode]':'32952',
                       'dependents[0][county]':'5',
                       'dependents[0][tobacco]':'N',
                       'op':'View All Available Plans'
                   },
                   callback = self.get_rates)]

    def get_rates(self, response):
        hxs = HtmlXPathSelector(response)
        plans = hxs.select('//table[contains(@class,"views-table")]/tbody/tr')
        items = []
        for plan in plans:
            item = EhealthItem()
            planname = plan.select('.//td[contains(@class,"views-field-title")]/span/a/text()').extract()
            plantype= plan.select('.//td[contains(@class, "views-field-field-type-of-plan")]/text()').extract()
            deductible= plan.select('.//td[contains(@class, "views-field-deductible")]/text()').extract()
            plancost = plan.select('.//td[contains(@class, "views-field-premium")]/div[contains(@class,"price")]/text()').extract()
            
            item['planname'] = planname[0]
            item['plantype'] = plantype[0]
            item['deductible'] = deductible[0]
            item['plancost'] = plancost[0]
            items.append(item)
        print items        
        
