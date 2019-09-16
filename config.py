from nonebot.default_config import *
from datetime import timedelta
import json

SESSION_RUN_TIMEOUT = timedelta(seconds=5)
SUPERUSERS = {3095823730}
ME = 3095823730
COMMAND_START = {''}
HOST = "mysql"
NICKNAME = {'%'}  # 命令标志符
DBNAME = "ctf"
USER = "******"
PASSWD = "******"
GROUP = [818441085]  # 比赛播报 -> 快乐计组
BLACKLIST = []
with open('keywords.json', 'r') as words:
    KEYWORDS = json.load(words)
