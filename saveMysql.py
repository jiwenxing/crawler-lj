#!/usr/bin/python3

import json
import pymysql
import re

def connectdb():
    # print('连接到mysql服务器...')
    # 连接数据库
    db = pymysql.Connect(
        host='192.168.192.125',
        port=3358,
        user='root',
        passwd='123456',
        db='test',
        charset='utf8'
    )
     
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
     
    # 使用 execute()  方法执行 SQL 查询 
    cursor.execute("SELECT VERSION()")
     
    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchone()
     
    # print ("Database version : %s " % data)
     
    # print('连接上了!')
    return db

def createtable(db):
    cursor = db.cursor()

    cursor.execute("DROP TABLE IF EXISTS lj_house")
    sql = """CREATE TABLE lj_house( 
        id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT COMMENT '主键',
        house_id BIGINT COMMENT '备案编号',
        house_url_id BIGINT COMMENT '链家编号',
        total_price int COMMENT '总价',
        unit_price int COMMENT '单价',
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
        price_update_times int DEFAULT 0 COMMENT '调价次数',
        link VARCHAR(200) COMMENT '链接',
        created_date DATETIME COMMENT '创建时间',
        modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间')ENGINE = InnoDB COMMENT 'lj' DEFAULT CHARSET=utf8;"""

    cursor.execute(sql)
    print('创建表成功!')

def insertdb(db, info):
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()

    # SQL 插入语句
    # 插入数据
    # info = {"标题": "户型正气，不沿马路，带花园，适宜居住", "总价": "183万", "每平方售价": "31112元/平米", "参考总价": "首付55万 税费13.8万(仅供参考) ", "建造时间": "未知年建", "小区名称": "三墩街100号小区", "所在区域": "西湖:三墩", "链家编号": "103101836069", "链接": "https://hz.lianjia.com/ershoufang/103101836069.html", "房屋户型": "3室1厅1厨1卫", "所在楼层": "中楼层 (共5层)", "建筑面积": "58.82㎡", "户型结构": "平层", "套内面积": "1㎡", "建筑类型": "", "房屋朝向": "南 北", "建筑结构": "未知结构", "装修情况": "简装", "梯户比例": "一梯两户", "配备电梯": "暂无数据", "产权年限": "70年", "挂牌时间": "2017-10-21", "交易权属": "商品房", "上次交易": "2000-07-17", "房屋用途": "普通住宅", "房屋年限": "满五年", "产权所属": "共有", "房本备件": "已上传房本照片", "房源编码": "170717332568"}
    sql = """INSERT INTO 
        lj_house (house_id, house_url_id, total_price, unit_price, total_square, area, street, city, community, build_time, house_style, floor, sale_date, decoration, hold_time, price_update_times, link, created_date) 
        VALUES ( '%d', '%d', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s', now() )"""
    data = (int(info.get("房源编码", "0")), int(info.get("链家编号", "0")), info.get("总价", "0"), info.get("每平方售价", "0"), info.get("建筑面积", "0"), info.get("所在区", "未知"), info.get("所在街道", "未知"), info.get("城市", "未知"), info.get("小区名称", "未知"), info.get("建造时间", "0000-00-00"), info.get("房屋户型", "未知"), info.get("所在楼层", "未知"), info.get("挂牌时间", "0000-00-00"), info.get("装修情况", "未知"), info.get("房屋年限", "未知"), 0, info["链接"])
    # try:
    # 执行sql语句
    cursor.execute(sql % data)
    # print('成功插入', cursor.rowcount, '条数据')
    # 提交到数据库执行
    db.commit()
    # except:
    #     # Rollback in case there is any error
    #     print('插入数据失败!') 
    #     db.rollback()

def querydb(db, info):
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()

    # SQL 查询语句
    #sql = "SELECT * FROM Student \
    #    WHERE Grade > '%d'" % (80)
    sql = "SELECT * FROM lj_house WHERE house_url_id = '%d'" % (int(info.get("链家编号", "0")))
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    for row in results:
        # print("already in database, houseId: %s, Price: %s" % (ID, Price)) 
        ID = row[2]
        Price = int(row[3])
        # 打印结果
        currentPrice = round(float(re.findall(r"\d+\.?\d*",info.get("总价", "0"))[0])) #通过正则提取其中的数字
        if Price != currentPrice:
            print("houseId: %s, yestoday: %d, today: %d, diff: %d" % (ID, Price, currentPrice, currentPrice - Price))
        #     print("price not change")
        # else:
            
            
        break

def deletedb(db):
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()

    # SQL 删除语句
    sql = "DELETE FROM Student WHERE Grade = '%d'" % (100)

    try:
       # 执行SQL语句
       cursor.execute(sql)
       # 提交修改
       db.commit()
    except:
        print('删除数据失败!')
        # 发生错误时回滚
        db.rollback()

def updatedb(db):
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()

    # SQL 更新语句
    sql = "UPDATE Student SET Grade = Grade + 3 WHERE ID = '%s'" % ('003')

    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        print('更新数据失败!')
        # 发生错误时回滚
        db.rollback()

def closedb(db):
    db.close()

def main():
    db = connectdb()    # 连接MySQL数据库
    
    # f = open("lj-data-2017-11-15.txt", "r", encoding='UTF-8')
    # for line in f.readlines(): 
    #     line = line.strip() 
    #     if not len(line) or line.startswith('#'):       #判断是否是空行或注释行 
    #         continue                                   
    #     info = json.loads(line)
    #     insertdb(db, info)        # 插入数据
    #     print("插入数据库成功: " + info["标题"])

    f = open("lj-data-2017-11-17.txt", "r", encoding='UTF-8')
    for line in f.readlines(): 
        line = line.strip() 
        if not len(line) or line.startswith('#'):       #判断是否是空行或注释行 
            continue                                   
        info = json.loads(line)
        # print("update begin..." + info["标题"])
        querydb(db, info)        # 插入数据
        

    
    f.close()

   

    # createtable(db)     # 创建表
    # insertdb(db)        # 插入数据

    # print '\n插入数据后:'
    # querydb(db) 
    # deletedb(db)        # 删除数据
    # print '\n删除数据后:'
    # querydb(db)
    # updatedb(db)        # 更新数据
    # print '\n更新数据后:'
    # querydb(db)

    closedb(db)         # 关闭数据库

if __name__ == '__main__':
    main()
    