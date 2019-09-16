import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import nonebot
import pytz
from aiocqhttp.exceptions import Error as CQHttpError
from DB import *

header = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/74.0.3729.131",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
}


def ctfTime():  # 获取比赛详情页
    url = "https://ctftime.org/event/list/upcoming"
    msg = requests.request("get", url, headers=header)
    soup = BeautifulSoup(msg.text, "lxml")
    ar = soup.find_all('a')
    ctfs = []

    for i in ar:
        search = re.search(r"/event/\d{1,5}", str(i))
        if search:
            ctfs.append("https://ctftime.org{0}.ics".format(search.group()))
    return ctfs


def TimeFormat(TimeString):
    TimeGroup = re.search(r"(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})(\d{2})", TimeString)
    time = "{0}-{1}-{2} {3}:{4}:{5}".format(TimeGroup.group(1), TimeGroup.group(2), TimeGroup.group(3),
                                            TimeGroup.group(4),
                                            TimeGroup.group(5), TimeGroup.group(6))
    return time


async def get_ctftime(i):  # 获取比赛详情
    db = connect()
    bot = nonebot.get_bot()
    reqs = requests.request("get", i, headers=header)
    li = reqs.text.split("\n")
    send = {"platform": "ctftime"}
    for i in li:
        if i.find("DESCRIPTION") >= 0:
            send.update(name=i[12:])
        elif i.find("URL") >= 0:
            send.update(url=i[4:])
        elif i.find("DTSTART") >= 0:
            send.update(start_time=TimeFormat(i[8:]))
        elif i.find("DTEND") >= 0:
            send.update(end_time=TimeFormat(i[6:]))
        elif i.find("SUMMARY") >= 0:
            send.update(format=re.search(r".*\((.*)\)$", i).group(1))
        else:
            continue
    if insert(db, send) == True:
        await bot.send_private_msg(user_id=ME, message="增加")
