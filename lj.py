#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author;Tsukasa

import time
import json
from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup
import re # re模块为高级字符串处理提供了正则表达式工具
import pandas as pd
import pymongo
from saveMysql import connectdb, createtable, insertdb, querydb, updatedb, closedb
from delrepeat import remove_repeat


def generate_allurl(user_in_nub, user_in_city):  # 生成url
    url = 'http://' + user_in_city + '.lianjia.com/ershoufang/xihu/pg{}/'
    for url_next in range(1, int(user_in_nub)):
        print(url.format(url_next) + " start!")
        yield url.format(url_next)


def get_allurl(generate_allurl):  # 分析url解析出每一页的详细url
    get_url = requests.get(generate_allurl, 'lxml')
    if get_url.status_code == 200:
        re_set = re.compile('<li.*?class="clear">.*?<a.*?class="img.*?".*?href="(.*?)"')
        re_get = re.findall(re_set, get_url.text)
        return re_get


def open_url(re_get):  # 分析详细url获取所需信息
    res = requests.get(re_get)
    if res.status_code == 200:
        info = {}
        soup = BeautifulSoup(res.text, 'lxml')
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
        print(info['标题'])
        return info

def update_to_MongoDB(one_page):  # update储存到MongoDB
    if db[Mongo_TABLE].update({'链家编号': one_page['链家编号']}, {'$set': one_page}, True): #去重复
        print('储存MongoDB 成功!')
        return True
    return False

def pandas_to_xlsx(info):  # 储存到xlsx
    pd_look = pd.DataFrame(info)
    pd_look.to_excel('链家二手房.xlsx', sheet_name='链家二手房')


def writer_to_text(list):  # 储存到text
    with open('lj-origin-'+time.strftime('%Y-%m-%d',time.localtime(time.time()))+'.txt', 'a', encoding='utf-8')as f:
        f.write(json.dumps(list, ensure_ascii=False) + '\n')
        f.close()


def main(url):
    writer_to_text(open_url(url))    #储存到text文件

# 每个模块都有一个__name__属性，当其值是'__main__'时，表明该模块自身在运行，否则是被引入
if __name__ == '__main__':
    user_in_city = input('输入爬取城市：')
    user_in_nub = input('输入爬取页数：')
    pool = Pool()
    for i in generate_allurl(user_in_nub, user_in_city):
        pool.map(main, [url for url in get_allurl(i)])   # results=pool.map(爬取函数，网址列表) 固定用法

    remove_repeat('lj-origin-'+time.strftime('%Y-%m-%d',time.localtime(time.time()))+'.txt')