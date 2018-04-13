# -*- coding: utf-8 -*-
import scrapy
import scrapy_splash

class JobsearchSpider(scrapy.Spider):
    name = 'fed_reserve_jobs'
    allowed_domains = ['www.federalreserve.gov','frbog.taleo.net']
    start_urls = ['http://www.federalreserve.gov/start-job-search.htm']

    def parse(self, response):
        yield(scrapy_splash.SplashRequest("https://frbog.taleo.net/careersection/1/moresearch.ftl?lang=en&portal=101430233", callback = self.parse_iframe))
    
    def parse_iframe(self, response):
        JOBPOST_SELECTOR = '.titlelink'
        for jobpost in response.css(JOBPOST_SELECTOR):
            JOBTITLE_SELECTOR = 'span a ::text'
            yield {
              'name' : jobpost.css(JOBTITLE_SELECTOR).extract()
            }
      

