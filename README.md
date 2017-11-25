# crawler-lj

a simple crawler demo by python3, whitch can fetch second-hand house data of specialized city from lianjia website, and persist them in mysql for analysis. 
 

## how

1. use the ddl.sql to create tables, modify the database connection config in mysqlop.py    
```python
db = pymysql.Connect(
            host='192.168.192.125',
            port=3358,
            user='root',
            passwd='123456',
            db='test',
            charset='utf8'
        )
```

2. run lj.py to fetch data from lianjia website and persist them into mysql    
you need to input the city code and area code that you want to fetch, for example, if 'hz' and 'xihu' were typed in means you will fetch data from `https://hz.lianjia.com/ershoufang/xihu/`

3. do your analysis


## todo

- schedule task & automatically
- data visualization

## references

- [Python爬虫代理IP池(proxy pool)](https://github.com/jhao104/proxy_pool)
- [python3 爬虫教学之爬取链家二手房](https://www.cnblogs.com/Tsukasa/p/6799968.html)