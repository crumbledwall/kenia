# kenia

基于coolq的python框架nonebot开发

使用三个容器桥接互联，selenium容器和coolq容器间使用反向websocket通讯，selenium容器运行kenia主程序，并且请求mysql容器下的数据库

#### 启动命令:

```shell
docker network create -d bridge bluebot
docker run -it -d --name selenium --restart unless-stopped -w /usr/workspace -v $(pwd)/:/usr/workspace --network bluebot crumbledwall/selenium 
docker run -ti -d --name coolq -p 9000:9000 -p 5700:5700 -v      ~/source/coolq:/home/user/coolq -e CQHTTP_SERVE_DATA_FILES=yes -e VNC_PASSWD=******** --restart unless-stopped --network bluebot crumbledwall/qqbot
docker run --name mysql --restart unless-stopped -e MYSQL_ROOT_PASSWORD=******* -d --network bluebot crumbledwall/mysql
```

启动后按照[nonebot文档](https://none.rclab.tk/guide/installation.html)的说明配置反向websocket链接，指向selenium容器，一般是`172.17.0.*`，然后在config.py里设置mysql的数据即可

#### 目录结构：

```shell
╭─kenia
├── bluebot
│   ├── change
│   │   ├── change.py
│   │   └── __init__.py
│   ├── daily_scheduler
│   │   ├── __init__.py
│   │   ├── remind.py
│   │   └── urge.py
│   ├── __init__.py
│   ├── natural_language
│   │   ├── __init__.py
│   │   └── keywords.py
│   ├── report
│   │   ├── __init__.py
│   │   └── report_ctf.py
│   ├── request_handler
│   │   └── __init__.py
│   ├── spider
│   │   ├── ctftime_spider.py
│   │   ├── ichunqiu_spider.py
│   │   ├── __init__.py
│   │   └── xctf_spider.py
│   └── weeky_scheduler
│       ├── __init__.py
│       └── report.py
├── bluebot.py
├── config.py
├── DB.py
├── keywords.json
└── README.md

```

#### keywords.json

语料文件的逻辑如下

* 每个主题下有多个列表，先遍历search，存在关键词继续后面的操作;

* 第二步，如果存在ignore继续遍历ignore，如果搜到ignore中的词，不予回复;

* 第三步，如果存在modify则便利modify，存在列中的修饰词才会回复，否则不予回复

* 最后从reply中随机取一个回复

* ban为true的话会禁言10分钟 

```json
{
  "DragQueen": {
    "search": ["女装","小裙子"],
    "modify": false,
    "ignore": ["算了","别"],
    "reply": ["协会DS，请","是女装大佬！(警觉"],
    "ban": false
  },
  "Association": {
    "search": ["协会","安协"],
    "modify": ["去","走"],
    "ignore": false,
    "reply": ["协会的地址是一教北 300b，如果不是太早或太晚基本都有人在，进去后找个地方坐下来学习就行"],
    "ban": false
  }
}
```

#### 建库语句

```sql
CREATE DATABASE ctf;
CREATE TABLE `game` (
  `name` varchar(1000) DEFAULT NULL,
  `format` varchar(1000) DEFAULT NULL,
  `platform` varchar(1000) DEFAULT NULL,
  `status` int(4) DEFAULT 0,
  `id` int(4) NOT NULL AUTO_INCREMENT,
  `starttime` datetime DEFAULT NULL,
  `endtime` datetime DEFAULT NULL,
  `url` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
```

