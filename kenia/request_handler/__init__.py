from nonebot import on_request, RequestSession
from nonebot import on_notice, NoticeSession


@on_notice('group_increase')  # 加群欢迎
async def _(session: NoticeSession):
    await session.send('欢迎加入Vidar_Team 2019新生群～')


@on_request('group')  # 加群自动通过
async def _(session: RequestSession):
    await session.approve()
    return
