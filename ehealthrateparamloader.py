import os
import time
import datetime
import pymongo

connection = pymongo.Connection('localhost', 27017)
db = connection['test']
collection = db['ehealth_rate_params']

now = datetime.datetime.now()

genders = ["MALE","FEMALE"] 
start_year = now.year - 60
smoking_options = ['true','false']    

datetime = datetime.datetime.utcnow()

#remove the existing documents?
collection.remove({})

for gender in genders:
    for smoker in smoking_options:
        for year in range(start_year, start_year + 40, 10):
            params = {
                      'gender':gender,
                      'smoker':smoker,
                      'year':year,
                      'datetime':datetime
                     }
            
            collection.insert(params)
 
            
            
