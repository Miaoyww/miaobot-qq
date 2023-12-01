from pathlib import Path
from nonebot import get_driver
from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    proxy: str = ""


config = Config.parse_obj(get_driver().config)
