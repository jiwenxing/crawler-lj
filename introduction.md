先大概记录一下，后期再整理

在不使用代理的情况下基本爬几十页的数据ip便会被ban掉，因此必须使用代理。在GitHub上找到一个还不错的代理项目，它其实也是使用爬虫爬免费代理站点的ip过来建立一个代理池，然后提供一个获取代理的接口，在自己的爬虫代码中通过接口去获取代理即可，试用了一下，感觉还不错。

我用redis做代理的cache，因此首先得确保安装服务，mac安装redis可参考[这篇文章](https://www.cnblogs.com/weiluoyan/p/7460466.html)

下载代理程序：`git clone https://github.com/jiwenxing/proxy_pool.git`

启动redis服务：`sudo /usr/local/bin/redis-server /usr/local/redis-4.0.2/etc/redis.conf`
查看redis日志：`tail -f /usr/local/redis-4.0.2/log-redis.log`

启动代理池服务：在`proxy_pool`目录下执行`python Run/main.py`
启动爬虫：在`crawler-lj`目录下执行`python lj.py`

执行的关键日志会记录在日志文件`crawler.log`中
爬取得数据会存入数据库，同时也会存放在`lj-crawler-data.txt`文件中，下次执行前会删除


## 数据统计口径

### 均价（平均房价/平均面积）

这个指标无法准确判断调价的走势，因为每次都有新房源插入，算是一个比较宏观粗略的统计，一定程度上反映单价均价的走势，排除了一些不感兴趣的豪宅（没钱）

统计口径：
 
```sql
select date_format(now(),'%y-%m-%d') as time,count(id) as house_num, avg(total_price), avg(total_square), avg(total_price+price_diff)/avg(total_square) as cur_avg_price from lj_house where total_price<800 and total_square<200;
```

统计结果：

```
+----------+-----------+------------------+-------------------+---------------+
| time     | house_num | avg(total_price) | avg(total_square) | cur_avg_price |
+----------+-----------+------------------+-------------------+---------------+
| 17-11-26 |      6522 |         336.8329 |           88.9405 |    3.78517765 |
+----------+-----------+------------------+-------------------+---------------+
```

### 调价均值（只统计调过价的房子）

这个指标一定程度上能反映卖家的心理预期，可以适当排除一些调价幅度过大（大于50）且挂牌时间超过100天的业主，感觉这部分业主不诚心卖，有扰乱市场之嫌

统计口径：

```sql
select date_format(now(),'%y-%m-%d') as time,count(id) as house_num,avg(price_diff),avg(total_square), avg(TIMESTAMPDIFF(DAY,sale_date,now())) as avg_sale_days from lj_house where abs(price_diff)>0 and abs(price_diff)<50 and TIMESTAMPDIFF(DAY,sale_date,now())<100;
```

统计结果：

```
+----------+-----------+-----------------+-------------------+---------------+
| time     | house_num | avg(price_diff) | avg(total_square) | avg_sale_days |
+----------+-----------+-----------------+-------------------+---------------+
| 17-11-26 |       270 |         -6.1704 |           85.2296 |       43.5963 |
+----------+-----------+-----------------+-------------------+---------------+
```
