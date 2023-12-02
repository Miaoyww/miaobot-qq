import asyncio
from nonebot import on_message
from nonebot.plugin import PluginMetadata
from nonebot.adapters.qq import *
from nonebot.rule import to_me

from src.service.plugin_type import PluginType
from .data_source import *

__plugin_meta__ = PluginMetadata(
    name='随机回复',
    description='随机回复一句话~',
    usage='''当你at bot并且回复一些话的时候，它可能会随机回复你()''',
    extra={"type": PluginType.FUNCTION_PLUGIN}
)

reply = on_message(rule=to_me())


@reply.handle()
async def _(bot: Bot, evt: MessageEvent):
    text = str(evt.get_message())
    nickname = evt.get_event_name()
    user_id = evt.get_user_id()
    result = await get_reply_result(text)
    if result is not None:
        logger.info(f"USER {user_id}|{nickname} 发送了 {text} 其回复是 {result} ")
        if type(result) is Message:
            for item in result:
                await bot.send(item)
        else:
            await bot.send(result)
    else:
        return

