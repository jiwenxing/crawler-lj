# crawler-lj

a simple crawler demo by python3, whitch can fetch second-hand house data of specialized city from lianjia website, and persist them in mysql for analysis. 
 

## how

1. use the ddl.sql to create tables, modify the database connection config in mysqlop.py
2. run lj.py to output a txt file whitch store the data fetch from lianjia website
3. run mysqlop.py to persist the data into mysql
4. do your analysis


## todo

- schedule task & automatically
- analysis way
- data visualization

## references

- [python3 爬虫教学之爬取链家二手房](https://www.cnblogs.com/Tsukasa/p/6799968.html)