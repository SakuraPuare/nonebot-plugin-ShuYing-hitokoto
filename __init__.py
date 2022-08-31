from typing import Union

import httpx
from nonebot import on_startswith, logger
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, PrivateMessageEvent

m = on_startswith(('一言', 'hitokoto'))


@m.handle()
async def hitokoto(bot: Bot, event: Union[GroupMessageEvent, PrivateMessageEvent]) -> None:
	url = 'https://v1.hitokoto.cn/?charset=utf-8&encode=json&c=d&c=i'
	async with httpx.AsyncClient() as client:
		res = await client.get(url)
		if res.is_error:
			logger.error("[hitokoto] 获取一言失败")
			return
		else:
			decoded = res.json()
			writer = f" ——  来自{decoded['from_who'] if decoded['from_who'] is not None else ''}" \
			         + f"{'的' if decoded['from_who'] is not None and decoded['from'] is not None else ''}" \
			         + f"{decoded['from'] if decoded['from'] is not None else ''}"
			length = len(decoded['hitokoto']) - len(writer)
			text = f"""\"{decoded['hitokoto']}\"\n\
{''.join(['    ' for _ in range(length)]) + writer if length > 0 else writer}"""
			await m.finish(message=text)
