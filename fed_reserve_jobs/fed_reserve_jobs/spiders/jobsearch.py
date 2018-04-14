# -*- coding: utf-8 -*-
import scrapy
import scrapy_splash
import json

class JobsearchSpider(scrapy.Spider):
    name = 'fed_reserve_jobs'
    allowed_domains = ['www.federalreserve.gov','frbog.taleo.net']
    start_urls = ['http://www.federalreserve.gov/start-job-search.htm']

    def parse(self, response):
        yield(scrapy_splash.SplashRequest("https://frbog.taleo.net/careersection/1/moresearch.ftl?lang=en&portal=101430233", callback = self.parse_iframe))
    
    def parse_iframe(self, response):
      
        script = """
                function main(splash)
                    local url = splash.args.url
                    assert(splash:go(url))
                    assert(splash:wait(0.5))

                    assert(splash:runjs('document.getElementById("advancedSearchInterface.keywordInput").value = "business"'))
                    assert(splash:runjs('document.getElementById("advancedSearchFooterInterface.searchAction").click()'))
                    assert(splash:wait(0.5))

                    -- return result as a JSON object
                    return {
                        html = splash:html()
                    }
                end
                """
        url = "https://frbog.taleo.net/careersection/1/moresearch.ftl?lang=en&portal=101430233"

        yield scrapy.Request(url, self.parse_result, meta={
            'splash': {
                'args': {'lua_source': script},
                'magic_response':False,
                'endpoint': 'execute',
            }
        })
            

    def parse_result(self, response):
        json_data = json.loads(response.body_as_unicode())
        data_html = scrapy.Selector(text=json_data["html"], type="html")
        JOBPOSTS = data_html.xpath('//span[@class="titlelink"]')
        for jobpost in JOBPOSTS:
            JOBTITLE_SELECTOR = 'span a ::text'
            yield {
                'name' : jobpost.css(JOBTITLE_SELECTOR).extract()
            }