

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
import scrapy


class ContentSpider(scrapy.Spider):

    name = "content2"
    start_urls = ['https://www.bilibili.com']
    custom_settings = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) "
                                     "Chrome/41.0.2228.0 Safari/537.36",
                       'ITEM_PIPELINES': {'bilibili.pipes.FilesPipeline3': 1, },
                       'DEFAULT_REQUEST_HEADERS': {'referer': 'https://www.bilibili.com',
                                                   "User-Agent":'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'


                                                   },

                       'cookies': [{'name': 'sid', 'value': '54wgdy76', 'path': '/', 'domain': '.bilibili.com', 'secure': False, 'httpOnly': False, 'expiry': 1627521516}, {'name': '_uuid', 'value': 'B70D3080-9A06-66CD-63B4-E330BCF93EB516665infoc', 'path': '/', 'domain': '.bilibili.com', 'secure': False, 'httpOnly': False, 'expiry': 1627521516}, {'name': 'buvid3', 'value': '5908C037-7BCD-44BF-A964-1A205AEB996B143095infoc', 'path': '/', 'domain': '.bilibili.com', 'secure': False, 'httpOnly': False, 'expiry': 1690593517}, {'name': 'DedeUserID', 'value': '250099903', 'path': '/', 'domain': '.bilibili.com', 'secure': False, 'httpOnly': False, 'expiry': 1611536525}, {'name': 'DedeUserID__ckMd5', 'value': '574780a5d0e84745', 'path': '/', 'domain': '.bilibili.com', 'secure': False, 'httpOnly': False, 'expiry': 1611536525}, {'name': 'SESSDATA', 'value': '970192fd%2C1611537525%2C83191*71', 'path': '/', 'domain': '.bilibili.com', 'secure': False, 'httpOnly': True, 'expiry': 1611536525}, {'name': 'bili_jct', 'value': 'f4b10c98d237b49079214119f7533f0a', 'path': '/', 'domain': '.bilibili.com', 'secure': False, 'httpOnly': False, 'expiry': 1611536525}, {'name': 'l', 'value': 'v', 'path': '/dynamic_svr/v1/dynamic_svr', 'domain': 'api.vc.bilibili.com', 'secure': False, 'httpOnly': False}]


                       }

    def __init__(self, up='', *args, **kwargs):
        super(ContentSpider, self).__init__(*args, **kwargs)
        self.up = up
        from selenium import webdriver
        import time
        ''' 
        driver = webdriver.Firefox()
        driver.get('https://passport.bilibili.com/login')
        driver.implicitly_wait(10)

        while True:
            time.sleep(5)
            if driver.current_url == 'https://www.bilibili.com/':
                print('loggin in')
                self.cookies = driver.get_cookies()
                break
        '''
        import json
        with open('bili.json', 'r') as f:
            k = json.load(f)
            self.cookies = k

    def parse(self, response):
        print(response.request.headers)
        print('ss r o b')
        #
        yield scrapy.Request('https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/dynamic_new?uid=25009990'
                             '3&type_list=268435455', cookies=self.cookies, callback=self.parse_2)

    def parse_2(self, response):
        import json

        print(response.text)

    def closed(spider, reason):
        pass


def run_spider(args):

    print(os.getcwd())
    process = CrawlerProcess(get_project_settings())
    process.crawl('content2', up=args)
    process.start(stop_after_crawl=True)  # the script will block here until the crawling is finished
    print('hello STOP')
    import sys
    sys.exit(0)


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        sys.argv.append('13215999')
    run_spider(sys.argv[1])











