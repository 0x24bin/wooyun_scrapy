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
class text(scrapy.Item):
    text = scrapy.Field() #网页内容
    url = scrapy.Field() # 网页url
    title = scrapy.Field() # 网页的标题
class Item(scrapy.Item):
    title = scrapy.Field() #网页标题
    url = scrapy.Field() # 网站的链接
    text = scrapy.Field() #网页内容
    friend_url = scrapy.Field() # 友情链接
    back_type = scrapy.Field() # 网页后台技术
    ip = scrapy.Field() # 网站归属地
    sql_url = scrapy.Field() #网页内带=的链接
    action_url = scrapy.Field() # 带有action或者do
    cms = scrapy.Field() # 网页cms技术
