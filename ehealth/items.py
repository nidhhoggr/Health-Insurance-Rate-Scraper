# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class EhealthItem(Item):
    plancompany = Field()
    planname    = Field()
    plantype    = Field()
    plancost    = Field()
    deductible  = Field()
    officevisit = Field()
    plan_details = Field()
    coinsurance = Field()
    rateparamid = Field()   
    datetime = Field()
