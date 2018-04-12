# -*- coding: utf-8 -*-
import scrapy


class JobsearchSpider(scrapy.Spider):
    name = 'fed_reserve_jobs'
    allowed_domains = ['www.federalreserve.gov','frbog.taleo.net']
    start_urls = ['http://www.federalreserve.gov/start-job-search.htm']

    def parse(self, response):
        pass

