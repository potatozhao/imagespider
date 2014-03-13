# imagespider

使用BeautifulSoup,urlparse2,redis,以及稍微改动的wgetter模块实现的一个针对22mm.cc的图片爬虫。

网页解析使用BeautifulSoup，url处理使用urlparse2，任务通道redis内存数据库，也可使用redis扩展为分布式爬取，下载使用wgetter

这个工程是余弦给我的一道题目，它包含一个针对http://www.22mm.cc/网站的spider，将网站中美女大图爬取下来。

使用redis实现任务通道，redis中存储了未爬取网页地址，已爬取网页地址，未下载图片地址，已下载图片地址，图片下载数量，图片未下载数量等。


# 相关依赖

* BeautifulSoup4

用于从网页中解析出所需要的URL。相比其他的解析库，其函数简单，编码转换能力强

* urlparse2

对URL进行处理

* redis

内存式数据库，主要用于存储爬虫队列，实现判断，可以直接在此基础上扩展成分布式爬虫。


# 模块重用

* redis pipelines模块

* wgetter模块

* 网址爬模块

# 不可重用组件：

图片下载地址分析系统。不同的网站需要对图片下载地址分析系统做不同修改，以保证能够正确的分析出需要下载图片的网址

# 使用方法：

1. 安装相关库BeautifulSoup

2. 安装redis

3. 安装urlparse2

4. 启动redis sever

# 注意
每次任务结束后请清空redis server
