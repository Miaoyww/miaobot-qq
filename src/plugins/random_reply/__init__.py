from nonebot.plugin import PluginMetadata, on_message

from src.service.plugin_type import PluginType
from .data_source import *

__plugin_meta__ = PluginMetadata(
    name='随机回复',
    description='随机回复一句话~',
    usage='''当你at bot并且回复一些话的时候，它可能会随机回复你()''',
    extra={"type": PluginType.FUNCTION_PLUGIN}
)

reply = on_message(priority=50)


@reply.handle()
async def _(bot: Bot, evt: MessageEvent, only_text=False, times=3):
    text = str(evt.get_message())
    nickname = evt.get_event_name()
    user_id = evt.get_user_id()
    result = await get_reply_result(text, only_text=only_text)
    if times == 0:
        await bot.send(evt, message=MessageSegment.text(
            "啊哦，大脑宕机了。。"))
        return
    if result is not None:
        logger.info(f"USER {user_id}|{nickname} 发送了 {text} 其回复是 {result} ")
        if type(result) is Message:
            for item in result:
                try:
                    await bot.send(evt, message=item)
                except ActionFailed:
                    logger.error(f"回复操作失败，正在尝试第{4 - times}次")
                    await _(bot, evt, only_text=True, times=times - 1)
                    return
        else:
            await bot.send(evt, message=result)
    else:
        return
