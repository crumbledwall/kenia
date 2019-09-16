from nonebot import on_command, CommandSession
from nonebot.permission import *
from .change import *

__plugin_name__ = '修改ctf的状态(需要管理员权限)：\n  修改 已报名|[id]\n  修改 忽略|[id]\n  修改 每天提醒|[id]\n'
__plugin_usage__ = r"""
修改ctf的状态：
  修改 已报名|[id]
  修改 忽略|[id]
  修改 每天提醒|[id]
"""


@on_command('change', aliases=('修改',), permission=GROUP_ADMIN)
async def change(session: CommandSession):
    ctf = session.get('ctf')
    change_id = await change_ctf(ctf)
    await session.send(change_id)


@change.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    command_group = re.search(r"(.*)\|(.*)", stripped_arg)
    if session.is_first_run:  # id的检测逻辑
        if not command_group:
            session.finish("命令格式错误，请重新输入")
        if not command_group.group(2):
            session.finish('要修改的CTF名不能为空，请重新输入')
        if re.match(r"^[0-9]*$", command_group.group(2)):
            if len(command_group.group(2)) > 4:
                session.finish("id长度是有限制的")
            else:
                session.state['ctf'] = command_group.group(0)
                return
        else:
            session.finish("hacker get out")
