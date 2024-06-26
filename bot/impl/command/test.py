#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: koipy-org
@Date: 2024/6/16 下午8:09
@Description: 
"""

from loguru import logger
from pyrogram import Client
from pyrogram.types import Message

from bot.utils import gen_key

from bot.impl.task import process, SlaveRequest
from bot.impl.query.selector import SLAVE_REQ_CACHE


async def task_handler(app: "Client", message: "Message"):
    msg_key = gen_key(message)
    if msg_key not in SLAVE_REQ_CACHE:
        slavereq = SlaveRequest()
        SLAVE_REQ_CACHE[msg_key] = slavereq
    else:
        slavereq = SLAVE_REQ_CACHE.get(msg_key, None)
        if slavereq is None:
            logger.error("can not get the latest slavereq. ")
    await process(app, message, slavereq)
