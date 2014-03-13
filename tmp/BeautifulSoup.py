# -*- coding: UTF-8 –*-
from bs4 import BeautifulSoup
import urlparse2
import urllib2
import wgetter
import re
import pdb
def web_url_tosave(url,html, domain):
    url_list = []
    content = BeautifulSoup(html).findAll('a')
    for item in content:
        href = item.get('href')
        ans = urlparse2.urljoin(url,href)
        ans_netloc = urlparse2.urlparse(ans).netloc
        if domain == ans_netloc:
            url_list.append(ans)
    print  url_list

def image_url_tosave(html):
    image_div= BeautifulSoup(html).find(id="box-inner")
    if image_div != None:
        image_script = None
        for div_children in image_div.children:
            if div_children.name == "script":
                 image_script = div_children.string
        image_url = image_script.split('"')[1]
        urls = image_url.split('big')
        image_url = urls[0]+'pic'+urls[1]
        wgetter.download(image_url)


def grabHref(url, domain):
    html = urllib2.urlopen(url).read()
    html = unicode(html, 'gb2312', 'ignore').encode('utf-8', 'ignore')
    #web_url_tosave(url,html,domain)
    image_url_tosave(html)




def main():
    url = "http://www.22mm.cc/mm/qingliang/PiaHaidCCPPademb.html"
    grabHref(url,"www.22mm.cc")
if __name__=="__main__":
    #main()
    wgetter.download(
        'http://jyimg1.meimei22.com/pic/jingyan/2014-3-10/1/%E6%9E%81%E5%93%81%E5%86%85%E8%A1%A3%E7%BE%8E%E5%A5%B3%E5%A6%A9%E5%AA%9A%E7%85%A71.jpg',
        './pics')