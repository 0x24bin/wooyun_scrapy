import scrapy
from bs4 import BeautifulSoup
########################################################################
class test(scrapy.spiders.Spider):
    """"""
    name = 'test1'
    start_urls = ['http://localhost/index1.html']
    #----------------------------------------------------------------------
    def parse(self,response):
        """get Item"""
        url = response.xpath("/html/body/a[1]/@href").extract()[0]
        yield scrapy.Request(url)
        