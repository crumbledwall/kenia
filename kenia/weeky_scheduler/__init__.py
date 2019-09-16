import nonebot
from aiocqhttp.exceptions import Error as CQHttpError
from .report import *


@nonebot.scheduler.scheduled_job('cron',day_of_week="mon",hour='7',timezone="Asia/Shanghai")
async def _():
    try:
        await report_games()
    except CQHttpError:
        pass
