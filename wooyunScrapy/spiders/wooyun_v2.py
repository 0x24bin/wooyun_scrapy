#coding:utf-8
from wooyunScrapy.items import WooyunSpiderItem
import scrapy
class wooyunSpider(scrapy.spiders.Spider):
    name = 'newSpider'
    start_urls = ['http://www.wooyun.org/bugs/page/%d'%i for i in range(5111)]
    
    #----------------------------------------------------------------------
    def getItem(self,response):
        """get Item"""
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
    def parse(self, response):
        """解析带有好多漏洞的页面"""
        for i in response.xpath('/html/body/div[5]/table[3]/tbody/tr/td/a/@href")').extract():
            yield scrapy.Request('http://www.wooyun.org%s'%i,callback=self.getItem)
