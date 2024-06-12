import asyncio
import time

from loguru import logger
from pyrogram import Client
from bot.queue import HandlerQueue


async def cron_delete_handler(app: "Client", handler_delete_queue: "HandlerQueue"):
    handlers = []
    while True:
        try:
            handlers.append(handler_delete_queue.get_nowait())
        except asyncio.queues.QueueEmpty:
            break
    # logger.debug("cron_delete_handler已被激活")
    for handler_tuple in handlers:

        try:
            hd, group, second, st = handler_tuple
            delta = time.time() - st
            if delta > second:
                app.remove_handler(hd, group)
                logger.debug(f"{hd.callback.__name__} handler 已被移除")
            else:
                handler_delete_queue.put(hd, group, second, st)
                continue

        except Exception as e:
            logger.error(f'Remove Handler Error: {e}')
            continue
