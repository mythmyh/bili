import os
import sys
import scrapy.crawler as crawler
from twisted.internet import reactor
from multiprocessing import Process, Queue
from scrapy.crawler import CrawlerProcess
from bilibili.spiders.Directory import AbsDirectory
from scrapy import Selector
import re
from scrapy.http import  Request
from scrapy.utils.project import get_project_settings
import os
from bilibili.items import BilibiliItem
import scrapy
import inspect
import ctypes


class column1:
    str = ''


class BiliItemsSpider(scrapy.Spider):

    comprehensive = 'https://api.bilibili.com/x/web-interface/dynamic/region?ps=12&rid=1'
    games = 'https://api.bilibili.com/x/web-interface/dynamic/region?ps=12&rid=4'
    dance = 'https://api.bilibili.com/x/web-interface/dynamic/region?ps=12&rid=129'
    domensticmade = 'https://api.bilibili.com/x/web-interface/dynamic/region?ps=12&rid=168'
    whild_tech = 'https://api.bilibili.com/x/web-interface/dynamic/region?ps=12&rid=36'
    phone_pad = 'https://api.bilibili.com/x/web-interface/dynamic/region?ps=12&rid=188'
    delicious_food = 'https://api.bilibili.com/x/web-interface/dynamic/region?ps=12&rid=160'
    funny = 'https://api.bilibili.com/x/web-interface/dynamic/region?ps=12&rid=119'
    name = "bl_items"

    custom_settings = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) "
                                     "Chrome/41.0.2228.0 Safari/537.36",
                       'ITEM_PIPELINES': {'bilibili.pipes.FilesPipeline3': 1, }
                       }
    start_urls = ['https://api.bilibili.com/x/web-interface/dynamic/region?ps=12&rid=129']

    def __init__(self, column=r'dance', *args, **kwargs):
        super(BiliItemsSpider, self).__init__(*args, **kwargs)
        self.column = column
        self.text = None

    def parse(self, response):
        self.text = response.text
        global text
        text = self.text

        print(BiliItemsSpider.funny, '==--')
        if self.column != 'dance':
            item_urls = [BiliItemsSpider.games, BiliItemsSpider.funny, BiliItemsSpider.delicious_food,
                         BiliItemsSpider.phone_pad,
                         BiliItemsSpider.whild_tech, BiliItemsSpider.domensticmade, BiliItemsSpider.comprehensive]
            item_tags = ['game', 'funny', 'delicious_food', 'phone_pad', 'whild_tech', 'domensticmade', 'comprehensive']
            tags_urls = dict(zip(item_tags, item_urls))
            print('from whild_tech')

            yield  Request(url=tags_urls[self.column], callback=self.parse_2)

    def parse_2(self,response):
        global text
        text = response.text

    def closed(spider, reason):
        import json

        urls1, titles1, author_id1 = [], [], []
        json_list = json.loads(text)

        y = json_list['data']['archives']
        print(y[1]['owner'])
        for x in range(len(y) - 1):
            urls1.append('https://www.bilibili.com/video/' + y[x]['bvid'])
            titles1.append(y[x]['title'])
            author_id1.append(y[x]['owner']['mid'])


        print(urls1)
        print(titles1)
        print(author_id1)
        import socket
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        port = 9999
        client.connect((host, port))
        full_str = titles1 + urls1 + author_id1
        client.send(str(full_str).encode('utf-8'))


def run_spider(args):

    print(os.getcwd())
    process = CrawlerProcess(get_project_settings())
    process.crawl('bl_items', column=args)
    process.start(stop_after_crawl=True)  # the script will block here until the crawling is finished
    print(' STOP')
    import sys
    sys.exit(0)


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        sys.argv.append('dance')
    run_spider(sys.argv[1])
