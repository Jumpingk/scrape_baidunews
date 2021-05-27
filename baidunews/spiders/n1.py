import scrapy
import re
from tqdm import tqdm
from scrapy.http import Request
from baidunews.items import BaidunewsItem

class N1Spider(scrapy.Spider):
    name = 'n1'
    allowed_domains = ['baidu.com']
    start_urls = ['http://news.baidu.com/widget?id=civilnews&ajax=json']
    ids = ['TechNews', 'SportNews', 'PicWall', 'MilitaryNews', 'LocalNews', 'LadyNews', 'InternetNews', 'InternationalNews', 'HealthNews', 'FinanceNews', 'EnterNews', 'DiscoveryNews']
    urls = []
    for i in range(0, len(ids)):
        urls.append('http://news.baidu.com/widget?id=' + ids[i] + '&ajax=json')

    def parse(self, response):
        html = response.body.decode('utf-8')
        url1 = re.compile('"url":"(.*?)"').findall(html)
        url2 = re.compile('"m_url":"(.*?)"').findall(html)
        if len(url1) == 0:
            url = url2
        else:
            url = url1
        deal_urls = []
        for u in url:
            deal_urls.append(u.replace('\\', ''))
        for j in tqdm(range(0, len(deal_urls)), desc='Processing'):
            yield Request(url=deal_urls[j], callback=self.next)
        for i in range(0, len(self.urls)):
            yield Request(url=self.urls[i], callback=self.parse)
    
    def next(self, response):
        item = BaidunewsItem()
        item['title'] = response.xpath('/html/head/title/text()').extract()
        item['link'] = response.url
        item['content'] = response.body.decode('utf-8')
        yield item
        

