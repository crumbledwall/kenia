from DB import *
import nonebot


async def urge_games():
    bot = nonebot.get_bot()
    db = connect()
    if urge(db):
        for i in urge(db):
            for id in GROUP:  # 遍历config中设定的GROUP
                await bot.send_group_msg(group_id=id,
                                         message=i + "当前状态为“每日提醒”，记得报名")
