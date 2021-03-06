# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
from pymongo import MongoClient
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
import sys
reload( sys )
sys.setdefaultencoding('utf-8')

class WooyunscrapyPipeline(object):
    def __init__(self):
        self.file = codecs.open("out.json",'wb',encoding="utf-8")
#         self.file = codecs.open("out.json",'wb')
    def process_item(self, item,spider):
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(line)
        return item
    def spider_closed(self, spider):
        self.file.close()
########################################################################
class MongoDBPipeline:
    """"""
    #----------------------------------------------------------------------
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
            log.msg("Question added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
        return item