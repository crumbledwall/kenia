from DB import *
import re


async def change_ctf(ctf: str) -> str:
    dic = {
        "已报名": 2,
        "忽略": 3,
        "每天提醒": 1,
        "默认": 0
    }
    command_group = re.search(r"(.*)\|(.*)", ctf)
    db = connect()
    if command_group.group(1) in dic:  # 支持状态和比赛信息的检测逻辑
        name = change(db, command_group.group(2), dic[command_group.group(1)])
        if name:
            return f'{name}的状态修改完毕'
        else:
            return "未找到该比赛信息"
    else:
        return "不支持该状态"
