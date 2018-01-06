#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Tsukasa
# update: Jverson

import time
import json
from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup
import re   
from delrepeat import remove_repeat
from mysqlop import save_or_update
import os, sys
import logging

FILE_NAME_DATA = "lj-crawler-data.txt"
FILE_NAME_LOG = "crawler.log"

def generate_allurl(city_code, area_code):  # 生成url
    url = 'http://' + city_code + '.lianjia.com/ershoufang/'+ area_code + '/pg{}/'
    url_first_page = 'http://' + city_code + '.lianjia.com/ershoufang/'+ area_code + '/'
    page_num = get_page_num(url_first_page)
    for url_next in range(1, page_num):
        print(url.format(url_next) + " start!")
        yield url.format(url_next)


def get_page_num(url_first_page):
    res = requests.get(url_first_page)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'lxml')
        page_arr = soup.select('.total.fl')
        total_num = int(re.findall(r"\d+\.?\d*", page_arr[0].text)[0])
        page_num = round(total_num/30)
        print("total houses of this area is %d, total page number is %d" % (total_num, page_num))
        return page_num
    return 0


def get_allurl(generate_allurl):  # 分析url解析出每一页的详细url
    get_url = requests.get(generate_allurl, 'lxml')
    if get_url.status_code == 200:
        re_set = re.compile('<li.*?class="clear">.*?<a.*?class="img.*?".*?href="(.*?)"')
        re_get = re.findall(re_set, get_url.text)
        return re_get

def get_proxy():
    return requests.get("http://0.0.0.0:5010/get/").content

def delete_proxy(proxy):
    requests.get("http://0.0.0.0:5010/delete/?proxy={}".format(proxy))

def open_url(re_get):  
    res = None
    while res is None or res.status_code != 200:
        try:
            proxy = get_proxy()
            res = requests.get(re_get, timeout=2, proxies={"http": "http://{}".format(proxy)})
        except:
            print("Unexpected error: %s, proxy: %s" % (sys.exc_info()[0], proxy))
            delete_proxy(proxy)
            continue
    
    if res.status_code == 200:
        info = {}
        soup = BeautifulSoup(res.text, 'lxml')
        try:
            info['标题'] = soup.select('.main')[0].text
            info['总价'] = soup.select('.total')[0].text + '万'
            info['每平方售价'] = soup.select('.unitPriceValue')[0].text
            info['参考总价'] = soup.select('.taxtext')[0].text
            info['建造时间'] = soup.select('.subInfo')[2].text
            info['小区名称'] = soup.select('.info')[0].text
            info['所在区'] = soup.select('.info a')[0].text
            info['所在街道'] = soup.select('.info a')[1].text
            info['链家编号'] = str(re_get)[34:].rsplit('.html')[0] #https://hz.lianjia.com/ershoufang/103101839020.html
            info['链接'] = str(re_get)
            info['区代码'] = str(re_get)[34:].rsplit('.html')[0]
            info['城市'] =  str(re_get)[8:].rsplit(".")[0]
            for i in soup.select('.base li'):
                i = str(i)
                if '</span>' in i or len(i) > 0:
                    key, value = (i.split('</span>'))
                    info[key[24:]] = value.rsplit('</li>')[0]
            for i in soup.select('.transaction li'):
                i = str(i)
                if '</span>' in i and len(i) > 0 and '抵押信息' not in i:
                    key, value = (i.split('</span>'))
                    info[key[24:]] = value.rsplit('</li>')[0]
        except:
            print("Unexpected error: %s, info: %s" % (sys.exc_info()[0], info))
            return None
        else:
            print(info['标题'])
            return info


def writer_to_text(list):
    if list is not None:
          with open(FILE_NAME_DATA, 'a', encoding='utf-8')as f:
              f.write(json.dumps(list, ensure_ascii=False) + '\n')
              f.close()  
    


def main(url):
    writer_to_text(open_url(url))    

def run():
    # remove temp file
    if os.path.exists(FILE_NAME_DATA):
        os.remove(FILE_NAME_DATA)

    # city_code = input('输入爬取城市代码：')
    # area_code = input('输入爬取区域代码：')
    city_code = 'hz'
    # db_server = input('输入要连接的数据库：') #local for my mac, remote for the server
    db_server = 'local'
    # 自定义只抓取感兴趣的区域
    area_code_set = {'xiasha', 'shangcheng', 'xihu', 'jianggan', 'gongshu', 'binjiang', 'xiacheng'}
    
    logging.basicConfig(filename=FILE_NAME_LOG, filemode="a", level=logging.ERROR)
    logging.error('>>>>>>>>>> task begin @ %s >>>>>>>>>>' % (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())))
    start = time.time()
    
    for area_code in area_code_set:
        logging.error('the area %s begin at %s' % (area_code, time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())))
        pool = Pool(10)
        for i in generate_allurl(city_code, area_code):
            pool.map(main, [url for url in get_allurl(i)])   # results=pool.map(爬取函数，网址列表) 固定用法
        logging.error('the area %s end at %s' % (area_code, time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())))
    
    save_or_update(FILE_NAME_DATA, db_server)
    
    end = time.time()
    print("task takes %d minutes in total" % ((end - start)/60))
    logging.error("task takes %d minutes in total" % ((end - start)/60))
    logging.error('<<<<<<<<<< task over @ %s <<<<<<<<<<' % (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())))





if __name__ == '__main__':
    run()

