
## 使用代理

在不使用代理的情况下基本爬几十页的数据ip便会被ban掉，因此必须使用代理。在GitHub上找到一个还不错的代理项目，它其实也是使用爬虫爬免费代理站点的ip过来建立一个代理池，然后提供一个获取代理的接口，在自己的爬虫代码中通过接口去获取代理即可，试用了一下，感觉还不错。

我用redis做代理的cache，因此首先得确保安装服务，mac安装redis可参考[这篇文章](https://www.cnblogs.com/weiluoyan/p/7460466.html)

启动redis服务：`sudo /usr/local/bin/redis-server /usr/local/redis-4.0.2/etc/redis.conf`
查看redis日志：`tail -f /usr/local/redis-4.0.2/log-redis.log`

启动代理池服务：