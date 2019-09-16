import nonebot
from DB import *


async def report_games():
    bot = nonebot.get_bot()
    format = "%Y-%m-%d %H:%M:%S"
    db = connect()
    reply = []
    if report(db):
        reply.append("本月赛事有以下几场：")
        for i in report(db):
            games = ''
            games += "赛事名称：" + i["name"]
            games += "\n形式：" + i["format"]
            games += "\n时间：" + i["starttime"].strftime(format) + "至" + i["endtime"].strftime(format)
            games += "\nurl：" + i["url"]
            games += "\nid：" + str(i["id"])
            reply.append(games)
    else:
        pass
    return reply
