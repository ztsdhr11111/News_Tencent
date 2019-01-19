# -*- coding: utf-8 -*-
import scrapy
from ..items import NewsTctItem

class NewsTctSpider(scrapy.Spider):
    name = 'news_tct'
    # allowed_domains = ['t.com']
    start_urls = ['https://www.qq.com/map/']

    def parse(self, response):
        links = response.xpath('//*[@id="0"]/div[@class="bd"]/dl[2]//a/@href').extract()
        for i in range(len(links)):
            if 'jjj.qq.com' in links[i]:
                links[i] = self.structure_url(links[i])
                yield scrapy.Request(links[i], callback=self.hb_parse)

    def structure_url(self, url):
        # http: // hb.jjj.qq.com / c / 2018list_1.htm
        url = url + 'c/2018list_1.htm'
        return url

    def hb_parse(self, response):
        links = response.xpath('//div[@class="newsitem"]/a/@href').extract()
        for i in range(len(links)):
            links[i] = response.request.url.split('c/20')[0] + links[i]
            yield scrapy.Request(links[i], callback=self.jjj_parse)

    def jjj_parse(self, response):
        item = NewsTctItem()
        item['title'] = response.xpath('//h1/text()').extract_first()
        item['content'] = ''.join(response.xpath('//div[@id="Cnt-Main-Article-QQ"]//p/text()').extract())
        item['pub_date'] = response.xpath('//span[@class="a_time"]/text()').extract_first()
        yield item

