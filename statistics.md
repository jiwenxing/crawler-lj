
这件事情的最终目的还是想从二手房的一些宏观的统计数据上分析整体的走势，因此设计一些合理的科学的统计指标并且随着时间的推移观察指标的变化很有意义。下面是当前想到的一些指标，后面还会不断补充。

## 数据统计指标

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

这个指标一定程度上能反映卖家的心理预期，可以适当排除一些调价幅度过大（大于50）且挂牌时间超过半年的业主，感觉这部分业主不诚心卖，有扰乱市场之嫌

统计口径：

```sql
select date_format(now(),'%y-%m-%d') as time,count(id) as house_num,avg(price_diff),avg(total_square), avg(TIMESTAMPDIFF(DAY,sale_date,now())) as avg_sale_days from lj_house where abs(price_diff)>0 and abs(price_diff)<50 and TIMESTAMPDIFF(DAY,sale_date,now())<180;
```

统计结果：

```
+----------+-----------+-----------------+-------------------+---------------+
| time     | house_num | avg(price_diff) | avg(total_square) | avg_sale_days |
+----------+-----------+-----------------+-------------------+---------------+
| 17-11-26 |       317 |         -5.1767 |           88.1767 |       55.4700 |
+----------+-----------+-----------------+-------------------+---------------+
```
