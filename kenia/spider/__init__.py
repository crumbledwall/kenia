import nonebot
from .ctftime_spider import *
from .ichunqiu_spider import *
from .xctf_spider import *


@nonebot.scheduler.scheduled_job('cron', day_of_week="sat", hour=20, timezone="Asia/Shanghai")
async def _():
    bot = nonebot.get_bot()
    await bot.send_private_msg(user_id=ME,
                               message=f'爬虫开始')
    ctftime_ctfs = ctfTime()
    xctf_ctfs = geturl()
    for ctftime, xctf in zip(ctftime_ctfs, xctf_ctfs):
        await get_ctftime(ctftime)
        await get_xctf(xctf)
    await get_ichunqiu()
    await bot.send_private_msg(user_id=ME,
                               message=f'爬虫结束')
