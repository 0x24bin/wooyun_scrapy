#coding:utf-8
import scrapy
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from wooyunScrapy.items import url
########################################################################
class GetSql(scrapy.spiders.Spider):
    """本地的=带上url输出 不是本地的= 直接输出"""
    name = 'subDomain'
    file_name = './targets'
    start_urls = []
    for i in open(file_name).readlines():
        if 'http' in i:
            start_urls.append(i.strip('\n'))
        else:
            start_urls.append('http://%s'%i.strip('\n'))
    #start_urls = ['http://www.sdu.edu.cn']
    #----------------------------------------------------------------------
    def is_struts(self,url):
        """"""
        if '.action' in url or '.do' in url and '.doc' not in url:
            if 'php' not in url and 'asp' not in url:
                return True
        return False
    #----------------------------------------------------------------------
    def parse(self,response):
        """还是找struts命令执行比较靠谱"""
        for i in BeautifulSoup(response.body,'lxml').findAll('a'):
            if i.has_attr('href'):
                i = i['href']
                if self.is_struts(i):
                    if 'http' in i:
                        item = url()
                        item['url'] = i
                        return item
                    else:
                        item = url()
                        item['url'] = "%s/%s"%(response.url,i)
                        return item
#----------------------------------------------------------------------
    def parse1__(self,respnse):
        """用来找sql注入的解析器,实际效果并不理想...不要这个了"""
        first_time = 1
        
        for i in BeautifulSoup(respnse.body,'lxml').findAll('a'):
            if i.has_attr('href'):
                href = i['href']
                if '=' in href:
                    local_link = not 'http' in href
                    if local_link and first_time:
                        print("%s/%s"%(respnse.url,href))
                        item = url()
                        item['url'] = "%s/%s"%(respnse.url,href)
                        yield item
                        #print("%s/%s"%(respnse.url,href),file=self.file_toSave)
                        first_time = 0
                    elif not local_link:
                        item = url()
                        item['url'] = i['href']
                        yield item
                        print(i['href'])
                        #print(i['href'],file=self.file_toSave)
        #print(return_value)