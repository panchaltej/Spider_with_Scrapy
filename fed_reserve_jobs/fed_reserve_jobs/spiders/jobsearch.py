# -*- coding: utf-8 -*-
import scrapy
import scrapy_splash
import json
import sys

class JobsearchSpider(scrapy.Spider):
    name = 'fed_reserve_jobs'
    # allowed_domains = ['www.federalreserve.gov','frbog.taleo.net']
    # start_urls = ['http://www.federalreserve.gov/start-job-search.htm']
    
    def __init__(self, keywords=None, category=None, *args, **kwargs):
        super(JobsearchSpider, self).__init__(*args, **kwargs)
        self.keywords = keywords
        self.category = category
        self.allowed_domains = ['www.federalreserve.gov','frbog.taleo.net']
        self.start_urls = ['http://www.federalreserve.gov/start-job-search.htm']
        

    def parse(self, response):
        yield(scrapy_splash.SplashRequest("https://frbog.taleo.net/careersection/1/moresearch.ftl?lang=en&portal=101430233", callback = self.parse_iframe))
    
    def parse_iframe(self, response):
        keywords = self.keywords
        category = self.category
        script = """
                function main(splash)
                    local url = splash.args.url
                    -- local keyword = process.argv[2]
                    assert(splash:go(url))

                    assert(splash:runjs('document.getElementById("advancedSearchInterface.keywordInput").value = "%s"'))
                    assert(splash:wait(0.25))
                    assert(splash:runjs('var cats = document.getElementById("advancedSearchInterface.jobfield1L1"), cat, i; for(i = 0; i < cats.length; i++) {cat = cats[i]; if (cat.text.toLowerCase() == "%s") {cats.value = cat.value;}}'))
                    assert(splash:wait(0.25))                    
                    assert(splash:runjs('if ("createEvent" in document) {var evt = document.createEvent("HTMLEvents");evt.initEvent("change", false, true);document.getElementById("advancedSearchInterface.jobfield1L1").dispatchEvent(evt);}else document.getElementById("advancedSearchInterface.jobfield1L1").fireEvent("onchange");'))
                    assert(splash:wait(0.25))
                    assert(splash:runjs('document.getElementById("advancedSearchFooterInterface.searchAction").click()'))
                    assert(splash:wait(0.5))

                    -- return result as a JSON object
                    return {
                        html = splash:html()
                    }
                end
                """
        url = "https://frbog.taleo.net/careersection/1/moresearch.ftl?lang=en&portal=101430233"
        script_exec = script % (keywords if (keywords != None) else "", category.lower() if (category != None) else "")
        yield scrapy.Request(url, self.parse_result, meta={
            'splash': {
                'args': {'lua_source': script_exec},
                'magic_response':False,
                'endpoint': 'execute',
            }
        })
            

    def parse_result(self, response):
        json_data = json.loads(response.body_as_unicode())
        data_html = scrapy.Selector(text=json_data["html"], type="html")
        JOBPOSTS = data_html.xpath('//span[@class="titlelink"]')
        matched_jobs = []
        for jobpost in JOBPOSTS:
            JOBTITLE_SELECTOR = 'span a ::text'
            matched_jobs.append(jobpost.css(JOBTITLE_SELECTOR).extract_first())
        print()            
        print("====================Search Result-Jobs====================")
        for job in matched_jobs:
            print(job)
        print("==========================================================")
        print()
            