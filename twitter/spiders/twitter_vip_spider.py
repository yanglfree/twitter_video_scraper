# -*- coding: utf-8 -*-
import scrapy


class TwitterVipSpiderSpider(scrapy.Spider):
    name = 'twitter_vip_spider'
    allowed_domains = ['https://twitter.com/home']
    start_urls = ['http://https://twitter.com/home/']

    def parse(self, response):
        pass


    def start_requests(response):
        

