import json
import re
import time
from decimal import Decimal
from urllib import request

import aiohttp
from aiohttp import ClientTimeout
from nonebot import on_command
from nonebot.adapters.qq import *
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata
from pydantic import BaseModel

from src.service import logger
from src.service.plugin_type import PluginType

biliCard = on_command("biliCard", block=True, priority=1)

__plugin_meta__ = PluginMetadata(
    name='bili视频卡片',
    description='获取Bilibili视频的详情信息',
    usage='''使用方法: .biliCard <Bvid>|<Aid>''',
    extra={"type": PluginType.NORMAL_PLUGIN, "command": "biliCard"}
)


class BiliData(BaseModel):
    title: str
    bvid: str
    cover_url: str
    upload_time: str
    duration: str
    desc: str
    view: int
    danmu: int
    like: int
    coin: int
    share: int
    favorite: int
    owner: str
    owner_face: str


@biliCard.handle()
async def _handle(bot: Bot, event: Event, arg: Message = CommandArg()):
    user_id = event.get_user_id()
    logger.auto(__plugin_meta__, event)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
        "Referer": "https://www.bilibili.com/",
        "Accept": "application/json;charset=UTF-8"

    }
    input_arg = arg.extract_plain_text()
    matched_b23tv = re.findall("(?<=b23.tv/)\w*", input_arg)
    if len(matched_b23tv) == 1:
        input_arg = request.urlopen(f"https://b23.tv/{matched_b23tv[0]}").geturl()
    matched_acode = re.search("av(\d{1,12})|BV(1[A-Za-z0-9]{2}4.1.7[A-Za-z0-9]{2})", input_arg)
    if matched_acode is None:
        return

    if matched_acode[0][0:2] == "BV":
        aid = bv2av(matched_acode[0])
    else:
        aid = matched_acode[0].replace("av", "")

    logger.debug(f"得到aid: {aid}", user_id=user_id)
    response_body: dict
    try:
        async with aiohttp.ClientSession(timeout=ClientTimeout(total=10)) as session:
            async with session.get(f"http://api.bilibili.com/x/web-interface/view?aid={aid}",
                                   headers=headers) as response:
                response_body = json.loads(
                    await response.text())["data"]
    except KeyError:
        logger.error("Bv/Av不存在", user_id=user_id, command=__plugin_meta__.name)
        await bot.send_group_msg(event, message=MessageSegment.text("你输入的Bv/Av不存在~"))
        return
    except ClientTimeout:
        logger.error("请求超时", user_id=user_id, command=__plugin_meta__.name)
        await bot.send_group_msg(event, message=MessageSegment.text("请求超时了, 若尝试多次后无效请联系管理员~"))
        return
    video_info = {
        "title": response_body["title"],
        "bvid": response_body["bvid"],
        "cover_url": response_body["pic"],
        "upload_time": time.strftime("%Y/%m/%d %H:%M", time.localtime(response_body["pubdate"])),
        "duration": f"{response_body['duration'] // 60}:{response_body['duration'] - response_body['duration'] // 60 * 60}",
        "desc": f"{response_body['desc']}",
        "view": response_body["stat"]["view"],
        "danmu": response_body["stat"]["danmaku"],
        "like": response_body["stat"]["like"],
        "coin": response_body["stat"]["coin"],
        "share": response_body["stat"]["share"],
        "favorite": response_body["stat"]["favorite"],
        "owner": f"{response_body['owner']['name']}",
        "owner_face": f"{response_body['owner']['face']}"
    }
    data = BiliData(**video_info)
    logger.debug(f"视频大略信息: \n标题: {video_info['title']}\n作者: {video_info['owner']}",
                 user_id=user_id,
                 command=__plugin_meta__.name)
    async with aiohttp.ClientSession() as session:
        async with session.get(data.cover_url, headers=headers) as response:
            img_data = await response.content.read()
            logger.debug("图像准备完成, 准备发送", user_id=user_id, command=__plugin_meta__.name)

    if len(data.desc.split("\n")) > 5:
        if len(data.desc.split("\n")) > 5:
            logger.debug("简介过长, 准备取前5行", user_id=user_id, command=__plugin_meta__.name)
            data.desc = "\n".join(data.desc.split("\n")[:5])
            data.desc += "...\n  (由于简介过长, 已截取前5行)"
    detail_text = f"{Decimal(data.view / 10000).quantize(Decimal('0.0')) if data.view > 10000 else data.view}" \
                  f"{'w' if data.view > 10000 else ''}次观看 · " \
                  f"{Decimal(data.like / 10000).quantize(Decimal('0.0')) if data.like > 10000 else data.like}" \
                  f"{'w' if data.like > 10000 else ''}点赞 · " \
                  f"{Decimal(data.coin / 10000).quantize(Decimal('0.0')) if data.coin > 10000 else data.coin}" \
                  f"{'w' if data.coin > 10000 else ''}硬币 · " \
                  f"{Decimal(data.favorite / 10000).quantize(Decimal('0.0')) if data.favorite > 10000 else data.favorite}" \
                  f"{'w' if data.favorite > 10000 else ''}收藏"
    text = f"————标题———— \n{data.title}\n" \
           f"————UP主———— \n{data.owner} ({data.upload_time}上传 -时长: {data.duration})\n" \
           f"————信息———— \n{detail_text}\n" \
        #  f"————简介———— \n{data.desc if data.desc != '' else f'来自NyaTri的消息: ——暂无简介哦~'}"

    image_message = MessageSegment.file_image(img_data)
    text_message = MessageSegment.text(text)
    await bot.send(event=event, message=(image_message + text_message))
    logger.success("发送成功", command=__plugin_meta__.name)


def bv2av(x):
    table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'  # 码表
    tr = {}  # 反查码表
    # 初始化反查码表
    for i in range(58):
        tr[table[i]] = i
    s = [11, 10, 3, 8, 4, 6]  # 位置编码表
    XOR = 177451812  # 固定异或值
    ADD = 8728348608  # 固定加法值
    r = 0
    for i in range(6):
        r += tr[x[s[i]]] * 58 ** i
    return (r - ADD) ^ XOR
