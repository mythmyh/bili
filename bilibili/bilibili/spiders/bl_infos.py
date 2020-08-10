
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
import json
import scrapy
from bilibili.items import BilibiliItem


class Bl_InfoSpider(scrapy.Spider):

    name = "bl_info"
    start_urls = ['https://www.acfun.cn/']
    custom_settings = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) "
                                     "Chrome/41.0.2228.0 Safari/537.36",
                       'ITEM_PIPELINES': {'bilibili.pipes.FilesPipeline3': 1, }
                       }

    def __init__(self, url2='https://www.acfun.cn/v/ac14110187', *args, **kwargs):
        super(Bl_InfoSpider, self).__init__(*args, **kwargs)

        self.start_urls = [url2]

    def parse(self, response):
        items = BilibiliItem()
        items['file_urls'] = ['https://api.bilibili.com/x/web-interface/dynamic/region?ps=12&rid=160']
        yield items

    def closed(spider, reason):
        def parse_bl_urls(files):
            with open(files, 'r') as f:
                urls, titles, author_id = [], [], []
                json_list = json.load(f)
                y = json_list['data']['archives']
                for x in range(len(y) - 1):
                    urls.append('https://www.bilibili.com/video/' + y[x]['bvid'])
                    titles.append(y[x]['title'])
                    author_id.append(y[x]['owner']['mid'])
            return urls, titles, author_id
        directory = os.getcwd()+'/tomcat/full'
        files = os.listdir(directory)
        full = directory+'/'+files[0]
        urls1, titles1, author_id1 = parse_bl_urls(full)
        print(urls1)
        print(titles1)
        print(author_id1)


def run_spider(args):

    print(os.getcwd())
    process = CrawlerProcess(get_project_settings())

    # process第二个参数为要在__init__里传入的参数名
    process.crawl('bl_info', url2=args)
    process.start(stop_after_crawl=True)  # the script will block here until the crawling is finished
    import sys
    sys.exit(0)


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        sys.argv.append('https://www.acfun.cn/v/ac14134110')
    run_spider(sys.argv[1])
