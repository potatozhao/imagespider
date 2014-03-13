#!/usr/bin/env python2
# -*- coding: UTF-8 –*-

from bs4 import BeautifulSoup
from optparse import OptionParser
import urlparse2
import urllib2
import redis
import threading
import os
import time
import logging

import revise_wgetter

class Base(object):
    u"""22mm 小爬虫基类 ."""

    def __init__(self, url, image_max_num, thread_num, file_path):
        u"""初始化爬虫
        Args:
            image_max_num :
            thread_num :
            file_path :
        """
        self.url = url
        self.image_max_num = image_max_num
        self.thread_num = thread_num
        self.file_path = file_path
        self.client = redis.StrictRedis(host='localhost', port=6379)

        self.img_url_pattern = []
        self.url_pattern = []
        logging.basicConfig(filename=os.path.join(os.getcwd(), 'log.txt'),
                                          level=logging.WARNING, filemode='w',
                                          format='%(asctime)s - %(levelname)s: %(message)s')

    def startspider(self):
        u"""爬虫开始函数"""
        self.redis_prepare()
        self.check_file_path()
        self.thread_control()
        while int(self.client.get('image_max_num')) is not 0:
            pass
        #self.client.flushall()

    def redis_prepare(self):
        u"""redis 内存数据库准备工作."""
        self.client.setnx('image_max_num', self.image_max_num)
        self.client.lpush('web_url_goto', self.url)
        self.client.sadd('web_url_visited', self.url)
        self.client.sadd('image_url_visited', self.url)
        self.client.setnx('image_downloaded_num', 0)

    def thread_control(self):
        u"""线程控制.
              根据thread_num开启对应线程以进行解析、爬取、下载
        """
        for i in xrange(self.thread_num):
            threading.Thread(target=self._extract_url, args=(), name='url_tread').start()
            threading.Thread(target=self.download, args=(), name='download_thread').start()


    def check_file_path(self):
        u"""判断存储目录是否存在，如果不存在则创建目录."""

        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path)
            return 0
        else:
            return 1

    def _extract_url(self):
        u"""根据网址进行链接解析.

        Args:
            url: 待分析网页网址

        Returns:
            本链接网页内的同域名网址列表
        """
        while int(self.client.get('image_max_num')) is not 0:
            if self.client.llen('web_url_goto') is 0:
                time.sleep(1)
            else:
                url = self.client.rpop('web_url_goto')
                try:
                    html = urllib2.urlopen(url).read()
                except:
                    logging.warning("url cant open: %s" % url)
                    continue
                domain = urlparse2.urlparse(url).netloc
                web_url_list = self._extract_web_url(html, url, domain)
                image_url_list = self._extract_img_url(html, domain)
                for web_url in web_url_list:
                    if int(self.client.sismember('web_url_visited', web_url)) is 0:
                        self.client.sadd('web_url_visited', web_url)
                        self.client.lpush('web_url_goto', web_url)
                for image_url in image_url_list:
                    if int(self.client.sismember('image_url_visited', image_url)) is 0:
                        self.client.sadd('image_url_visited', image_url)
                        self.client.lpush('image_url_goto', image_url)
                        logging.info("%s--->%s" % (url, image_url))

    def _extract_web_url(self, html, url, domain):
        u"""从html内容中解析出同域名网址列表.

        Args:
            html: 待解析的内容
            url: 爬取页面的地址
            domain: 当前网站域名

        Return:
            html内容中的同域名网址

        """

        url_list = []
        content = BeautifulSoup(html).findAll('a')
        for item in content:
            href = item.get('href')
            ans = urlparse2.urljoin(url, href)
            ans_netloc = urlparse2.urlparse(ans).netloc
            if domain == ans_netloc:
                url_list.append(ans)
        return url_list

    def _extract_img_url(self, html, domain):
        u"""从html内容中解析出同域名图片列表.

        Args:
            html: 待解析的内容
            domain: 当前网站域名

        Return:
            html内容中的同域名图片网址列表
        """

        image_div = BeautifulSoup(html).find(id="box-inner")
        image_url_list = []
        if image_div is not None:
            image_script = None
            for div_children in image_div.children:
                if div_children.name == "script":
                    image_script = div_children.string
            image_url = image_script.split('"')[1]
            urls = image_url.split('big')
            image_url = urls[0]+'pic'+urls[1]
            image_url_list.append(image_url)
        return image_url_list

    def download(self):
        u"""下载对应的文件.

        Args:
            url: 下载链接

        Return:
            下载文件名称，若下载不成功，则返回None
        """
        while int(self.client.get('image_max_num')) is not 0:
            if self.client.llen('image_url_goto') is 0:
                time.sleep(1)
            else:
                if int(self.client.get('image_max_num')) is -1:
                    image_url = self.client.rpop('image_url_goto')
                    self.client.incr('image_downloaded_num')
                    try:
                        revise_wgetter.download(image_url, int(self.client.get('image_downloaded_num')), self.file_path)
                    except:
                        self.client.incr('image_max_num')
                        logging.warning('download error:%s' % image_url)


                else:
                    self.client.decr('image_max_num')
                    image_url = self.client.rpop('image_url_goto')
                    self.client.incr('image_downloaded_num')
                    try:
                        revise_wgetter.download(image_url, int(self.client.get('image_downloaded_num')), self.file_path)
                    except:
                        self.client.incr('image_max_num')
                        logging.warning('download error:%s' % image_url)

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-o", "--thread", dest="thread_num", default='10', type='int', help="thread_num")
    parser.add_option("-f", "--file_path", dest="file_path", help="write report to FILE", metavar="./pics",
                      default='./pics')
    parser.add_option("-i", "--image_max_num", dest="image_max_num", help="image max download num", default=-1,
                      type="int")
    options, args = parser.parse_args()
    if len(args) > 0:
        url = args[0]
        thread_num = options.thread_num
        file_path = options.file_path
        image_max_num = options.image_max_num
        spider = Base(url, image_max_num, thread_num, file_path)
        spider.startspider()
        print "爬取结束"
    else:
        print "error:please put in the right url"
