import nonebot
from nonebot import on_command, CommandSession


@on_command('usage', aliases=['食用方法', 'help', '使用说明', '使用方法', '说明'])
async def _(session: CommandSession):
    plugins = list(filter(lambda p: p.name, nonebot.get_loaded_plugins()))

    arg = session.current_arg_text.strip().lower()
    if not arg:
        await session.send(
            'kenia现在支持的命令有：\n\n' + '\n'.join(p.name for p in plugins if p.name))
        return

    for p in plugins:
        if p.name.lower() == arg:
            await session.send(p.usage)
