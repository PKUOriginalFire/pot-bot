import nonebot

# from nonebot.adapters.console import Adapter
from nonebot.adapters.onebot.v11 import Adapter

nonebot.init(driver="~fastapi", _env_file=".env")
driver = nonebot.get_driver()
driver.register_adapter(Adapter)
nonebot.load_builtin_plugins()
nonebot.load_plugin("pot.plugins.pot")
nonebot.load_plugin("pot.plugins.dessert")
nonebot.load_plugin("pot.plugins.scheduler")
nonebot.load_plugin("nonebot_plugin_status")

app = nonebot.get_asgi()


@app.get("/ping")
async def pong():
    return {"pong": "pong"}


if __name__ == "__main__":
    nonebot.run(host="0.0.0.0", port=8080)
