import nonebot
from nonebot.adapters.qq import Adapter

nonebot.init()
driver = nonebot.get_driver()
driver.register_adapter(Adapter)
# 加载插件
# nonebot.load_plugins("src/basic_plugins")
nonebot.load_plugins("src/plugins")
nonebot.load_plugins("src/plugins/scripts")

if __name__ == "__main__":
    nonebot.run(app="__mp_main__:app")
