import asyncio
import time
from pyrogram.handlers.handler import Handler


class HandlerQueue(asyncio.Queue):
    def __init__(self):
        """
        消息处理的队列
        """
        super().__init__()

    def put(self, h: "Handler", group: int = 3, second: int = 10, submit_time: float = None) -> None:
        """
        h:  from pyrogram.handlers.handler import Handler
        group: handler所在的组别
        second: 设定多少秒后删除
        """
        if isinstance(h, Handler) and isinstance(group, int) and isinstance(second, int):
            submit_time = time.time() if submit_time is None else submit_time
            super().put_nowait((h, group, second, submit_time))



