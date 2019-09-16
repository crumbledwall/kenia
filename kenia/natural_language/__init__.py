from aiocqhttp.message import escape
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from .keywords import *
from nonebot.typing import *

__plugin_name__ = '闲聊(彩蛋慢慢挖掘)：\n  ping\n'


@on_command('natural')
async def natural(session: CommandSession):
    message = session.state.get('message')  # 命令参数留空
    reply = await call_keywords(session, message)
    if reply:
        await session.send(reply)


@on_natural_language(only_to_me=False)  # 不需要命令符
async def _(session: NLPSession):
    return IntentCommand(60.0, 'natural', args={'message': session.msg_text})
    # 置信度60，权重低于查询等命令
