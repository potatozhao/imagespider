# -*- coding: UTF-8 –*-
import redis
import wgetter

def image_download(image_goto_db,image_visited_db,flag_db,image_path):
    """ this is a function to download image from web.
    
	ArgS:
	    image_goto_db:the datebase of image's url which will be download.
        image_visited_db:the adtebase of image's url which is downloaded.
        flag_db:还有多少张图片需要下载，当flag_db=0时，不再下载图片。当flag_db值为-1时无限下载
            flag_db一般存储在数据库中。
        image_path:图片下载地址
    Return:
        no return
    Raise：
        no error
    """
    image_url = 0
    if flag_db == 0:
        return 0


if __name__ == "__main__":
    client =  redis.StrictRedis(host='localhost', port=6379)
    client.setnx('foo','0')
    client.decr('foo')
    #client.delete('foo')
    print int(client.get('foo'))