import requests
from bs4 import BeautifulSoup
import re
import nonebot
from aiocqhttp.exceptions import Error as CQHttpError
from DB import *

header = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/74.0.3729.131",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
}


def time_format(time):
    timetext = re.search(
        r"(\d{4})年(\d{1,2})月(\d{1,2})日\s(\d{2}):(\d{2})——(\d{4})年(\d{1,2})月(\d{1,2})日\s(\d{2}):(\d{2})",
        time)
    return {"start_time": "{0}-{1}-{2} {3}:{4}:{5}".format(timetext.group(1), timetext.group(2),
                                                           timetext.group(3),
                                                           timetext.group(4), timetext.group(5), "00"),
            "end_time": "{0}-{1}-{2} {3}:{4}:{5}".format(timetext.group(6), timetext.group(7),
                                                         timetext.group(8),
                                                         timetext.group(9), timetext.group(10), "00")
            }


def geturl():
    url = "https://www.xctf.org.cn/ctfs/recently/"
    reqs = requests.request("get", url, headers=header)
    msg = reqs.text

    soup = BeautifulSoup(msg, "lxml")
    ar = soup.find_all('a')
    ctfs = []

    for i in ar:
        search = re.search(r"/ctfs/detail/\d{1,5}", str(i))
        if search:
            ctfs.append("https://www.xctf.org.cn/{0}".format(search.group()))
    return ctfs


async def get_xctf(i):
    db = connect()
    try:
        send = {"platform": "xctf"}
        bot = nonebot.get_bot()
        reqs = requests.request("get", i, headers=header)
        msg = reqs.text
        soup = BeautifulSoup(msg, "lxml")
        name = soup.find('h3').get_text()
        msg = soup.find("div", class_="col-md-9 pad30L").find_all("dd")
        send.update({"name": name})
        for element, i in enumerate(msg):
            if element == 1:
                send.update(format=i.text)
            elif element == 6:
                send.update(url=i.text)
            elif element == 7:
                send.update(time_format(i.text))
            else:
                continue
        if insert(db, send) == True:
            await bot.send_private_msg(user_id=ME, message="增加")

    except CQHttpError:
        pass



