from nonebot import on_command
from nonebot.adapters.qq import *
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata

from src.service import logger
from src.service.plugin_type import PluginType

cat = on_command("httpcat", block=True, priority=5)

__plugin_meta__ = PluginMetadata(
    name='httpcat',
    description='随机获取一只猫猫~',
    usage='''使用方法: .httpcat''',
    extra={"type": PluginType.NORMAL_PLUGIN, "command": "httpcat"}
)


@cat.handle()
async def _(bot: Bot, ev: Event, arg: Message = CommandArg()):
    logger.auto(__plugin_meta__, ev)
    if (code := arg.extract_plain_text()).isdigit():
        await bot.send(event=ev, message=MessageSegment.image(f"https://http.cat/{code}"))
    else:
        await bot.send(event=ev, message=MessageSegment.image("https://http.cat/404"))
