# -*- coding: utf-8 -*-
import scrapy
import logging
from bilibili.items import BilibiliItem
from bilibili.spiders.Directory import StoreDirectory
from bilibili.spiders.package_socket import send_socket
import os
from ffmpy3 import FFmpeg

class BilibiliSpider(scrapy.Spider):
    name = 'bilibili1'
    allowed_domains = ['www.bilibili.com']
    custom_settings = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) "
                                     "Chrome/41.0.2228.0 Safari/537.36",

                       'ITEM_PIPELINES': {'bilibili.pipelines.BiliPipeline': 1, },
                       'Referer': 'https://www.bilibili.com/video/av94003264?spm_id_from=333.851.b_626'
                                  '96c695f7265706f72745f64616e6365.27'
                       }

    def __init__(self, url=None, *args, **kwargs):
        super(BilibiliSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]

    def parse(self, response):

        final = self.get_video_url(response)
        logging.warning(response.headers)
        items = BilibiliItem()
        items['file_urls'] = [final]
        items_audio = BilibiliItem()
        items_audio['file_urls'] = [self.get_audio_url(response)]
        global k
        k = send_socket(12005, '正在下载文件', '正在合并文件')
        yield items
        next(k)
        yield items_audio

    def get_video_url(self, response):
        bil_1 = response.text.split('video/mp4')
        bil_2 = bil_1[0].split('http')
        raw_1 = bil_2[len(bil_2)-1]
        raw_2 = raw_1.split(']')
        raw_3 = raw_2[0].replace('\"', '')
        final = 'http' + raw_3
        return final

    def get_audio_url(self, response):
        global title
        title = response.xpath('//h1//span/text()').extract()[0]
        bil_1 = response.text.split('audio/mp4')
        bil_2 = bil_1[0].split('http')
        raw_1 = bil_2[len(bil_2)-1]
        raw_2 = raw_1.split(']')
        raw_3 = raw_2[0].replace('\"', '')
        final = 'http' + raw_3
        return final

    def closed(spider, reason):
        next(k)
        get_full()


def get_full():
    title_1 = title.replace(' ', '').replace('/', '').replace('|', '')
    if os.path.exists(StoreDirectory.file_path+'/' + title_1):
        print('已经存在')
        return
    os.chdir('./tomcat/')
    s = ''
    video_info = []
    for list1 in sorted(os.listdir('./')):
        if os.path.isfile(list1):
            video_info.append(list1)
    filename = StoreDirectory.file_path+"\\"+title_1+".mp4"
    print(filename)
    print(list1)
    ff = FFmpeg(inputs={video_info[0]: None, video_info[1]: None}, outputs={filename: '-vcodec copy -acodec copy'})
    print(ff.cmd)
    try:
        ff.run()
    finally:

        for list1 in os.listdir('./'):
            if os.path.isfile(list1):
                os.remove(list1)


