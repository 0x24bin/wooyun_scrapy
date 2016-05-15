#!/usr/bin/env python
#coding:utf-8
"""
  Author:  FIHT --<>
  Purpose: 
  Created: 2016年05月09日
"""
from wooyunScrapy.items import WooyunSpiderItem
import scrapy
########################################################################
class wooyunSpider(scrapy.spiders.Spider):
    """乌云爬虫"""
    name = 'wooyunSpider'
    allowed_domains = ['wooyun.org']
    start_urls = ['http://www.wooyun.org/corps/page/%d'%i for i in range(43,44)]
    #----------------------------------------------------------------------
    def fuck_method(self,response):
        """给定一个带有好多漏洞的网页,返回有rank的和已经忽略的漏洞"""
        for i in response.xpath('/html/body/div[5]/table[2]/tbody/tr'):
            status = i.xpath('th[2]/a/text()').extract()[0].encode('utf-8')
            if status=='已公开' or status=='已忽略':
                yield scrapy.Request('http://www.wooyun.org'+i.xpath('td/a/@href').extract()[0],callback=self.get_info)
    #----------------------------------------------------------------------
    def get_info(self,response):
        """给一个漏洞链接返回你需要的东西"""
        content = response.xpath('//body/div[5]')[0] # 所有的信息都在content里面了
        # 我感兴趣的东西 1-> 漏洞标题 2->漏洞作者 3->漏洞厂商 4->漏洞作者 5->提交时间 6->公开时间 7->漏洞类型 8->自评rank 9->厂商实际给的rank
        item = WooyunSpiderItem()
        item['link'] = content.xpath('h3/a/@href')[0].extract()
        item['title'] = content.xpath('h3[2]/text()')[0].extract()[7:].strip()
        item['changhsang'] = content.xpath('h3[3]/a/text()').extract()[0].strip()
        item['author'] = content.xpath('h3[4]/a/text()').extract()[0].strip()
        item['level'] = content.xpath('h3[8]/text()').extract()[0][7:]
        item['type_'] = content.xpath('h3[7]/text()').extract()[0][7:]
        item['submit_time'] = content.xpath('h3[5]/text()').extract()[0][7:]
        item['author_rank'] = content.xpath('h3[9]/text()').extract()[0][7:].strip()
        item['changshang_rank'] = content.xpath('div[4]/p[2]/text()').extract()[0][7:]
        if (len(item)>2): # 大于2,肯定是被忽略的漏洞,把rank置为0
            item['changshang_rank'] = '0'
        # for i in item:
            # item[i] = item[i].encode('utf-8')
        return item
    #----------------------------------------------------------------------
    def get_url(self,response):
        """给了厂商链接你去把每个漏洞都访问一遍"""
        i=response.xpath("/html/body/div[5]/p[5]/text()")[0]
        page_num = i.extract().split(' ')[3]
        for i in range(int(page_num)):
            if 'page' in response.url: #证明是已经带了pagenum的
                #yield scrapy.Request(response.url[0:url.rfind('/')]+'/%d'%i)
                print '即将抓取',(response.url[0:url.rfind('/')]+'/%d'%i).encode('utf-8')
                yield scrapy.Request(response.url[0:url.rfind('/')]+'/%d'%i,callback=self.fuck_method)
            else: #没有带pagenum
                #yield scrapy.Request(response.url+'/%d'%i)
                #print '即将抓取',(response.url+'/page/%d'%i).encode('utf-8')
                yield scrapy.Request(response.url+'/page/%d'%i,callback=self.fuck_method)
    #----------------------------------------------------------------------
    def parse(self, response):
        """给一个response,找出里面的东西,以及下一步要干什么"""
        # 不惜一切代价找到 厂商名称 网址 注册时间
        # 然后第再写一个爬虫把所有的厂商的漏洞细节爬取下来
        all = response.xpath('//tr/td[2]/a/@href')
        for i in all:
            if i!='http://':
                yield scrapy.Request('http://wooyun.org'+i.extract().encode('utf-8'),callback=self.get_url)
                #print('http://wooyun.org/'+i.extract().encode('utf-8'))
            else:
                continue

