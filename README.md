# Spider with Scrapy

## Description
Spider for the following site: ​ https://www.federalreserve.gov/start-job-search.htm​ that can be executed from command line, takes an input, returns all items and can accept the following arguments:

1. No argument
2. Keywords
3. Job category

```
$ scrapy crawl fed_reserve_jobs -a keywords="python" -a category="Security"
```

**Output** : Prints resulting jobs with job ID and job location

## Technologies used
1. Python3
2. Scrapy
3. scrapy-splash
4. Lua Script

## Steps to Run the Project

1. Install python3, Install pip:
```
    sudo apt-get install -y python3-pip
```
2. Install Scrapy, scrapy-splash  
```
    pip install Scrapy
```  
```
    pip install scrapy-splash
```
3. Install Lua Script : <https://www.lua.org/download.html>
4. Install Docker  
   Start Splash instance  
```
    docker run -p 8050:8050 scrapinghub/splash
```
5. Clone or download the github repository - <https://github.com/panchaltej/Spider_with_Scrapy>
6. Run using below command from the cloned directory where scrapy.cfg file is present:
```
    $ scrapy crawl fed_reserve_jobs -a keywords="python" -a category="Security"
```
