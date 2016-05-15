# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WooyunSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field() # 漏洞标题
    link = scrapy.Field() # 漏洞的url
    changhsang = scrapy.Field() # 厂商
    author = scrapy.Field() # 漏洞作者
    level = scrapy.Field() # 自评等级
    author_rank = scrapy.Field() # 自评rank
    submit_time = scrapy.Field() # 提交时间
    tags = scrapy.Field() # tag
    type_ = scrapy.Field() # 漏洞类型
    changshang_rank = scrapy.Field() # 厂商给的rank

class url(scrapy.Item):
    url =  scrapy.Field()
