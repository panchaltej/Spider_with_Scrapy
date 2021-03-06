# -*- coding: utf-8 -*-
import scrapy
import scrapy_splash
import json

class JobsearchSpider(scrapy.Spider):
    name = 'fed_reserve_jobs'
    
    def __init__(self, keywords=None, category=None, *args, **kwargs):
        super(JobsearchSpider, self).__init__(*args, **kwargs)
        self.keywords = keywords
        self.category = category
        self.allowed_domains = ['www.federalreserve.gov','frbog.taleo.net']
        self.start_urls = ['http://www.federalreserve.gov/start-job-search.htm']
        

    def parse(self, response):
        #Sending request to the iframe
        yield(scrapy_splash.SplashRequest("https://frbog.taleo.net/careersection/1/moresearch.ftl?lang=en&portal=101430233", callback = self.parse_iframe))
    
    def parse_iframe(self, response):
        keywords = self.keywords
        category = self.category
        #script to be run with search criteria
        script = """
                function main(splash)
                    local url = splash.args.url
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
        #extracting html from the json response
        data_html = scrapy.Selector(text=json_data["html"], type="html")
        JOBPOSTS = data_html.xpath('//div[@class="iconcontentpanel"]')
        matched_jobs = {}

        for jobpost in JOBPOSTS:
            JOBTITLE_SELECTOR = 'div div div div h3 span a ::text' # selects div containing job
            JOBLOC_SELECTOR = '.morelocation span ::text' # selects span containing job location
            JOBID_SELECTOR = '.text ::text' # selects element containing jobid 
            job = jobpost.css(JOBTITLE_SELECTOR).extract_first() + " - " + jobpost.css(JOBID_SELECTOR).extract_first()
            matched_jobs[job] = jobpost.css(JOBLOC_SELECTOR).extract_first()

        #print result
        print()            
        print("====================Search Result-Jobs====================")
        print()  
        for job, location in matched_jobs.items():
            print(job, " - ", location)
        print("==========================================================")
        print()
            