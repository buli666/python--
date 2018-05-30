# -*- coding:utf-8 -*-
from grab import Grab
import logging
from bs4 import BeautifulSoup
import os
import re
import sys
import json
import traceback
import time
import requests

reload(sys)
sys.setdefaultencoding('utf-8')

# logging.basicConfig(level=logging.DEBUG)
g = Grab()
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
}
r = requests
head_data = {
    'headers':headers,
    'timeout':5
}
g.setup(headers=headers)
g.setup(timeout=300, connect_timeout=300)
# 下载文件的存放目录
dir = "E:/usr/toutiao"

def handles(filename,source_url):
    s = r.get(source_url,headers=headers,timeout=5)
    soup = BeautifulSoup(s.content,'lxml')
    image = str(soup).split("gallery: JSON.parse(\"")[-1].split("siblingList:")[0].replace("\"),","").strip().replace("\\","")
    # http://p3.pstatp.com/origin/pgc-image/1526828215301b1faba9cff
    image_list = json.loads(image,encoding='utf-8')
    image_lists = image_list['sub_images']
    for ig in image_lists:
        img_ = ig['url']
        img = str(img_) + ".jpg"
        g.go(img)
        filenames = "/" + filename + "/" + str(img).split("/")[-1]
        if not os.path.exists(dir):
            os.mkdir(dir)
        if not os.path.exists(dir + filenames):
            g.doc.save(dir + filenames)
        print "downloads:::" + img

def get_json(contents):
    for con in contents:
        # 小图
        thumb = con['image_url']
        thumb = "http:" + thumb
        # 小图片列表
        img_list = con['image_list']
        # 标题
        filename = con['title']
        # url
        source_url_ = con['source_url']
        source_url_ = str(source_url_).replace("item/","i")
        source_url = "https://www.toutiao.com" + source_url_
        handles(filename, source_url)



if __name__ == '__main__':
    file = open("c.txt")
    ex = file.readlines()
    for e in ex:
        print e
        s = r.get(e,headers=headers,timeout=5)
        content = json.loads(s.content,encoding='utf-8')
        contents = content['data']
        print contents
        get_json(contents)





