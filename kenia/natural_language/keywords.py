import jieba
from config import *
import random
from nonebot import *



async def call_keywords(session, text: str) -> str:
    bot = get_bot()  # 获取主动调用cqhttp接口的对象
    if session.ctx['user_id'] in BLACKLIST:  # 应对营销号的黑名单
        await bot.set_group_ban(user_id=session.ctx['user_id'],
                                group_id=session.ctx['group_id'], duration=30 * 30)
    for topic in KEYWORDS.values():
        if topic["modify"]:  # 有修饰检测列表
            for words in topic["search"]:
                if words in jieba.cut(text, cut_all=False):
                    for ignore in topic["ignore"]:
                        if text.find(ignore) != -1:  # 找到忽略词自动跳过
                            return None
                        else:
                            for modifiers in topic["modify"]:
                                if modifiers in jieba.cut(text, cut_all=False):
                                    if topic["ban"]:
                                        await bot.set_group_ban(user_id=session.ctx['user_id'],
                                                                group_id=session.ctx['group_id'], duration=10*10)
                                    return random.choice(topic["reply"])
                                else:
                                    continue
                else:
                    continue
        else:  # 无修饰检测列表
            for words in topic["search"]:
                if words in jieba.cut(text, cut_all=False):
                    for ignore in topic["ignore"]:
                        if text.find(ignore) != -1:
                            return None
                        else:
                            if topic["ban"]:
                                await bot.set_group_ban(user_id=session.ctx['user_id'],
                                                        group_id=session.ctx['group_id'], duration=10 * 10)
                            return random.choice(topic["reply"])
