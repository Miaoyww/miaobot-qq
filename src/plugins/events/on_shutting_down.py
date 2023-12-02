import nonebot

driver = nonebot.get_driver()


@driver.on_shutdown
async def on_shutdown():
    pass
