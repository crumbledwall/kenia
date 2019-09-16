import nonebot
from os import path
import config
import json

if __name__ == '__main__':
    nonebot.init(config)
    nonebot.load_builtin_plugins()
    nonebot.load_plugins(
        path.join(path.dirname(__file__), "kenia"), "kenia"
    )
    nonebot.run(host='0.0.0.0', port=8080)  # 类flask
