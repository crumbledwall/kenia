from datetime import datetime

import MySQLdb

from config import *


def connect():
    db = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWD, db=DBNAME, charset='utf8')
    return db


def insert(database, dir):
    query = database.cursor(MySQLdb.cursors.DictCursor)
    query.execute("select id from game where name=%s and platform=%s", (dir["name"], dir["platform"]))
    if query.fetchone():
        return False  # 跳过已插入的比赛
    elif not query.fetchone():

        query.execute("select id,platform from game where url=%s and starttime=%s and endtime=%s",
                      (dir["url"], dir["start_time"], dir["end_time"]))
        getone = query.fetchone()
        if getone is None:
            query.execute(
                "insert into game(name,starttime,endtime,url,format,platform) values(%s,%s,%s,%s,%s,%s);", (
                    dir['name'], dir['start_time'], dir['end_time'], dir['url'], dir['format'], dir['platform']))
            database.commit()
            return True

        else:
            # 同时满足“url相同，起止时间相同，平台不同”的比赛视为同一比赛，相同比赛以ctftime为准，ctftime无数据时保留，默认
            if getone["platform"] != dir["platform"] and dir["platform"] == "ctftime":

                query.execute(
                    "update game set name=%s,starttime=%s,endtime=%s,url=%s,format=%s,platform=%s where id =%s", (
                        dir['name'], dir['start_time'], dir['end_time'], dir['url'], dir['format'], dir['platform'],
                        getone["id"]))
                database.commit()
                return True
            # 同一平台忽略“url相同，起止时间相同”的检测
            elif getone["platform"] == dir["platform"]:

                query.execute(
                    "insert into game(name,starttime,endtime,url,format,platform) values(%s,%s,%s,%s,%s,%s);", (
                        dir['name'], dir['start_time'], dir['end_time'], dir['url'], dir['format'],
                        dir['platform']))
                database.commit()
                return True

            else:
                return False


    else:
        return False


def change(database, id, status):
    query = database.cursor(MySQLdb.cursors.DictCursor)
    query.execute("update game set status=%s where id =%s", (status, id))
    database.commit()
    query.execute("select name from game where id=%s", (id,))
    r = query.fetchone()
    if r:
        return r["name"]
    else:
        return False


def remind(database):
    remind = []
    query = database.cursor(MySQLdb.cursors.DictCursor)
    query.execute("select name,starttime,status,id from game")
    for i in query.fetchall():  # 比赛前一天提醒，选取距播报时间0-48小时、且日期差一天的比赛
        if i["starttime"].day -datetime.now().day==1  and 0 <= (i["starttime"] - datetime.now()).days <= 1   and i["status"] != 3:
            remind.append("{0}(id:{1})".format(i["name"], i["id"]))
        else:
            pass
    return remind


def report(database):
    report = []  # 查询当月ctf所用方法
    query = database.cursor(MySQLdb.cursors.DictCursor)
    query.execute("select id,starttime,status from game")
    for i in query.fetchall():
        day = (i["starttime"] - datetime.now()).days
        if 0 <= day < 30 and i["status"] != 3:
            query.execute("select name,starttime,endtime,url,format,id from game where id =%s", (i["id"],))
            report.append(query.fetchone())
        else:
            pass
    return report


def urge(database):
    urge = []  # 每日提醒催命状态的比赛
    query = database.cursor(MySQLdb.cursors.DictCursor)
    query.execute("select name,starttime,status,id from game")
    for i in query.fetchall():
        if (i["starttime"] - datetime.now()).days > 0 and i["status"] == 1:
            urge.append("{0}(id:{1})".format(i["name"], i["id"]))
        else:
            pass
    return urge
