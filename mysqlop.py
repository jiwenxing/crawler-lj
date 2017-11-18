#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author:Jverson

import json
import pymysql
import re
import time


def connect_server(server):
    db = None
    if server == "local":  # 连接mac本机数据库
         db = pymysql.Connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='jiwenxing',
            db='test',
            charset='utf8'
        )
    else:  # 连接测试机数据库
        db = pymysql.Connect(
            host='192.168.192.125',
            port=3358,
            user='root',
            passwd='123456',
            db='test',
            charset='utf8'
        )
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()
    print ("Mysql connect successfully, version : %s " % data)
    return db


# create table
def create_table(db):
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS lj_house")
    sql = """CREATE TABLE lj_house( 
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT COMMENT '主键',
    house_id BIGINT COMMENT '备案编号',
    house_url_id BIGINT COMMENT '链家编号',
    total_price int COMMENT '总价',
    unit_price int COMMENT '单价',
    price_diff int DEFAULT 0 COMMENT '调价差值',
    price_update_times int DEFAULT 0 COMMENT '调价次数',
    total_square int COMMENT '总面积',
    area VARCHAR(50) COMMENT '所在区',
    street VARCHAR(20) COMMENT '所在街道',
    city VARCHAR(20) COMMENT '所在城市',
    community VARCHAR(100) COMMENT '小区名称',
    build_time VARCHAR(50) COMMENT '建造年代',
    house_style VARCHAR(50) COMMENT '户型',
    floor VARCHAR(20) COMMENT '楼层',
    sale_date DATETIME COMMENT '挂牌时间',
    decoration VARCHAR(50) COMMENT '装修情况',
    hold_time VARCHAR(50) COMMENT '房屋年限（是否满五）',
    link VARCHAR(200) COMMENT '链接',
    created_date DATETIME COMMENT '创建时间',
    modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间')
    ENGINE = InnoDB COMMENT 'lj' DEFAULT CHARSET=utf8;"""
    
    cursor.execute(sql)
    print('table created!')

# 插入单条数据
def insert_data(db, info):
    cursor = db.cursor()
    # info = {"标题": "户型正气，不沿马路，带花园，适宜居住", "总价": "183万", "每平方售价": "31112元/平米", "参考总价": "首付55万 税费13.8万(仅供参考) ", "建造时间": "未知年建", "小区名称": "三墩街100号小区", "所在区域": "西湖:三墩", "链家编号": "103101836069", "链接": "https://hz.lianjia.com/ershoufang/103101836069.html", "房屋户型": "3室1厅1厨1卫", "所在楼层": "中楼层 (共5层)", "建筑面积": "58.82㎡", "户型结构": "平层", "套内面积": "1㎡", "建筑类型": "", "房屋朝向": "南 北", "建筑结构": "未知结构", "装修情况": "简装", "梯户比例": "一梯两户", "配备电梯": "暂无数据", "产权年限": "70年", "挂牌时间": "2017-10-21", "交易权属": "商品房", "上次交易": "2000-07-17", "房屋用途": "普通住宅", "房屋年限": "满五年", "产权所属": "共有", "房本备件": "已上传房本照片", "房源编码": "170717332568"}
    sql = """INSERT INTO 
        lj_house (house_id, house_url_id, total_price, unit_price, total_square, area, street, city, community, build_time, house_style, floor, sale_date, decoration, hold_time, price_update_times, link, created_date) 
        VALUES ( '%d', '%d', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s', now() )"""
    data = (int(info.get("房源编码", "0")), int(info.get("链家编号", "0")), re.findall(r"\d+\.?\d*",info.get("总价", "0"))[0], re.findall(r"\d+\.?\d*",info.get("每平方售价", "0"))[0], re.findall(r"\d+\.?\d*",info.get("建筑面积", "0"))[0], info.get("所在区", "未知"), info.get("所在街道", "未知"), info.get("城市", "未知"), info.get("小区名称", "未知"), info.get("建造时间", "0000-00-00"), info.get("房屋户型", "未知"), info.get("所在楼层", "未知"), info.get("挂牌时间", "0000-00-00"), info.get("装修情况", "未知"), info.get("房屋年限", "未知"), 0, info["链接"])
    cursor.execute(sql % data)
    db.commit()

def calculate_diff(db, info):
    cursor = db.cursor()
    sql = "SELECT * FROM lj_house WHERE house_url_id = '%d'" % (int(info.get("链家编号", "0")))
    cursor.execute(sql)
    row = cursor.fetchone()
    if row:
        ID = row[2]
        Price = int(row[3])
        diffRecord = int(row[5])
        currentPrice = round(float(re.findall(r"\d+\.?\d*",info.get("总价", "0"))[0])) #通过正则提取其中的数字
        if Price != currentPrice:
            diff = currentPrice - Price
            print("houseId: %s, before: %d, now: %d, diff: %d" % (ID, Price, currentPrice, diff))
            if diffRecord == diff:
                return 0
            return diff  # total price changed
        else:
            return 0 # no change
    return 9999 # no record
    

def existsdb(db, info):
    cursor = db.cursor()
    sql = "SELECT * FROM lj_house WHERE house_url_id = '%d'" % (int(info.get("链家编号", "0")))
    cursor.execute(sql)
    results = cursor.fetchall()
    if results:
        return True
    return False

def deletedb(db, info):
    cursor = db.cursor()
    sql = "DELETE FROM lj_house WHERE house_url_id = '%d'" % (int(info.get("链家编号", "0")))
    cursor.execute(sql)
    db.commit()

def update_data(db, info, diff):
    cursor = db.cursor()
    sql = "UPDATE lj_house SET price_update_times = price_update_times + 1, price_diff = '%d' WHERE house_url_id = '%d'" % (int(diff), int(info.get("链家编号", "0")))
    cursor.execute(sql)
    db.commit()

def closedb(db):
    db.close()

def save_or_update(fileName):
    db = connect_server("remote") 
    f = open(fileName, "r", encoding = 'UTF-8')

    insertNum = 0
    updateNum = 0
    for line in f.readlines(): 
        line = line.strip() 
        if not len(line) or line.startswith('#'): 
            continue                                   
        info = json.loads(line)
        print(info["标题"])
        diff = calculate_diff(db, info)
        print("price diff: %d" % diff)
        if diff == 9999:
            print("insert begin")
            insert_data(db, info)
            insertNum += 1
        elif diff != 0:
            print("update begin")
            update_data(db, info, diff)
            updateNum += 1

    print("total insert data: %d" % insertNum)
    print("total update data: %d" % updateNum)

    f.close()
    closedb(db) 


def main():
    # db = connect_server("local") 
    db = connect_server("remote") 
    
    # f = open("lj-uniq-2017-11-15.txt", "r", encoding='UTF-8')
    # for line in f.readlines(): 
    #     line = line.strip() 
    #     if not len(line) or line.startswith('#'):       #判断是否是空行或注释行 
    #         continue                                   
    #     info = json.loads(line)
    #     insert_data(db, info)        # 插入数据
    #     print("插入数据库成功: " + info["标题"])

    
    # f = open("lj-uniq-2017-11-18.txt", "r", encoding='UTF-8')
    # for line in f.readlines(): 
    #     line = line.strip() 
    #     if not len(line) or line.startswith('#'): 
    #         continue                                   
    #     info = json.loads(line)
    #     calculate_diff(db, info) 
        
    # f.close()

   
    f = open("lj-uniq-" + time.strftime('%Y-%m-%d',time.localtime(time.time())) + '.txt', "r", encoding = 'UTF-8')
    insertNum = 0
    updateNum = 0
    for line in f.readlines(): 
        line = line.strip() 
        if not len(line) or line.startswith('#'): 
            continue                                   
        info = json.loads(line)
        print(info["标题"])
        diff = calculate_diff(db, info)
        print("price diff: %d" % diff)
        if diff == 9999:
            print("insert begin")
            insert_data(db, info)
            insertNum += 1
        elif diff != 0:
            print("update begin")
            update_data(db, info, diff)
            updateNum += 1

    print("total insert data: %d" % insertNum)
    print("total update data: %d" % updateNum)
    f.close()



    closedb(db)     

if __name__ == '__main__':
    main()
    