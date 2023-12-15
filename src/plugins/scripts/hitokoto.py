import json
from enum import Enum

from aiohttp import *
from nonebot import on_command
from nonebot.adapters.qq import Bot, Event, Message, MessageSegment
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata
from pydantic import BaseModel

from src.service import logger, PluginType


class HitokotoType(Enum):
    animation = "a"  # 动画
    comic = "b"  # 漫画
    gaming = "c"  # 游戏
    literature = "d"  # 文学
    original = "e"  # 原创
    internet = "f"  # 来自网络
    other = "g"  # 其他
    film = "h"  # 影视
    poetry = "i"  # 诗词
    netease = "j"  # 网易云
    philosophy = "k"  # 哲学
    witty = "l"  # 抖机灵


class Hitokoto(BaseModel):
    id: int
    uuid: str
    hitokoto: str
    type: str
    source: str
    source_who: str
    creator: str
    creator_uid: int
    reviewer: int
    commit_from: str
    created_at: str
    length: int


_url = "https://v1.hitokoto.cn"

hitokoto = on_command("hitok", priority=5, block=True)
__plugin_meta__ = PluginMetadata(
    name='一言',
    description='获取一言',
    usage='''使用方法: /hitok ''',
    extra={"type": PluginType.NORMAL_PLUGIN, "command": "hitok"}
)


@hitokoto.handle()
async def _(bot: Bot, event: Event, arg: Message = CommandArg()):
    logger.auto(__plugin_meta__, event)
    async with ClientSession(timeout=ClientTimeout(total=10)) as session:
        async with session.get(url=f"https://v1.hitokoto.cn") as response:
            response_body: dict = json.loads(await response.text())
            response_body.update(
                {"source": response_body.get("from") if response_body.get("from") is not None else "",
                 "source_who": response_body.get("from_who") if response_body.get("from_who") is not None else ""})
            hitokoto_ = Hitokoto(**response_body)
            result = f'"{hitokoto_.hitokoto}“\n\t ' \
                     f'—— {hitokoto_.source_who} {f"「{hitokoto_.source}」" if hitokoto_.source != "" and hitokoto_.source else ""}'
            logger.debug(f"已获取到一言内容: {result}", command=__plugin_meta__.name, user_id=event.get_user_id())
            await bot.send(event,
                           message=MessageSegment.text(result))
            logger.success("调用成功", command=__plugin_meta__.name)
