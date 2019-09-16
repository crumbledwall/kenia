from nonebot import on_command, CommandSession


from .report_ctf import *

__plugin_name__ = '查询一个月之内的ctf赛事：\n  %查询ctf\n  %查询本月ctf'
__plugin_usage__ = r"""
一月之内ctf查询命令

输入：
查询ctf
查询本月ctf
"""


@on_command('queryctf', aliases=("查询ctf", "查询本月ctf"))
async def ctf(session: CommandSession):
    city = session.state.get('ctf')
    ctf_report = await report_games()
    for i in ctf_report:
        await session.send(i)

