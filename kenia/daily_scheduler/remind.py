from DB import *
import nonebot


async def remind_games():
    bot = nonebot.get_bot()
    db = connect()
    if remind(db):
        for i in remind(db):
            for id in GROUP:  # 遍历config中设定的GROUP
                await bot.send_group_msg(group_id=id,
                                         message=i + "即将开始，记得参加")
