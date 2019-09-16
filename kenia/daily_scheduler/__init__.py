import nonebot
from aiocqhttp.exceptions import Error as CQHttpError
from .remind import *
from .urge import *


@nonebot.scheduler.scheduled_job('cron', hour='8', timezone="Asia/Shanghai")
async def _():
    try:
        await remind_games()
        await urge_games()
    except CQHttpError:
        pass
