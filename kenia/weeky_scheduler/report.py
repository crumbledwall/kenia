from datetime import datetime
import nonebot
import pytz
from DB import *


async def report_games():
    bot = nonebot.get_bot()
    format = "%Y-%m-%d %H:%M:%S"
    db = connect()
    if report(db):
        for id in GROUP:
            await bot.send_group_msg(group_id=id,
                                 message="每周赛事播报\n本月赛事有以下几场：")
            for i in report(db):
                games = ''
                games += "赛事名称：" + i["name"]
                games += "\n形式：" + i["format"]
                games += "\n时间：" + i["starttime"].strftime(format) + "至" + i["endtime"].strftime(format)
                games += "\nurl：" + i["url"]
                games += "\nid：" + str(i["id"])
                await bot.send_group_msg(group_id=id,
                                     message=games)
