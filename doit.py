#!/usr/bin/env python

import os
import time
import pymongo

from mailer import *


cn = CrawlerNotifier()
connection = pymongo.Connection('localhost', 27017)
db = connection['test']
collection = db['ehealth_rate_params']

round_num = 1 
error_count = 0
request_count_limit = 10

rate_params = collection.find()

for rate_param in rate_params:
    rateparamid = rate_param['_id']
    gender = rate_param['gender']
    smoker = rate_param['smoker']
    year = rate_param['year']
    response = None
    request_count = 0
    while not response and request_count <= request_count_limit:
        request_count +=1
        output = os.popen('scrapy crawl ehealth -a gender=%s -a smoker=%s -a year=%d -a rateparamid=%s' % (gender, smoker, year, rateparamid)) 
        time.sleep(12)
        response = output.read()
        print 'scrapy crawl ehealth -a gender=%s -a smoker=%s -a year=%d, response: %s, round: %d' % (gender, smoker, year, response, round_num)

    if request_count > request_count_limit:
        cn.notify('error',round_num)
        error_count +=1

    round_num+=1

if error_count  == 0:
    cn.notify('success')
