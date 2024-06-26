#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: koipy-org
@Date: 2024/6/17 下午12:25
@Description: 
"""
from pyrogram import Client
from pyrogram.types import Message
from utils.cleaner import ArgCleaner, parse_url, parse_site, parse_command_option, ClashCleaner
from utils.types.task import SlaveRequest
from utils.collector import SubCollector
from bot.config import CONFIG, lang
from bot.check import get_id
from bot.impl.query.selector import SlaveSelector
from bot.init import app


async def process(_: "Client", message: "Message", slavereq: SlaveRequest):
    tgargs = ArgCleaner.getarg(str(message.text))
    target = message.reply_to_message if message.reply_to_message else message
    maybe_url = tgargs[1] if len(tgargs) > 1 else target.text if target.id != message.id else ""
    cmd_opt = parse_command_option(tgargs[0])
    include_text = cmd_opt["include"] if "include" in cmd_opt else tgargs[2] if len(tgargs) > 2 else ''
    exclude_text = cmd_opt["exclude"] if "exclude" in cmd_opt else tgargs[3] if len(tgargs) > 3 else ''
    slavereq.runtime = CONFIG.runtime
    slavereq.runtime.includeFilter = include_text
    slavereq.runtime.excludeFilter = exclude_text
    slavereq.task.messageID = target.id
    slavereq.task.chatID = target.chat.id
    if not slavereq.task.url:
        a_url = parse_url(maybe_url, CONFIG.slaveConfig)
        if not a_url:
            await message.reply(lang.parse_url_err)
            return
        slavereq.task.url = a_url
    if not slavereq.task.name:
        site = parse_site(slavereq.task.url)
        if not site:
            await message.reply(lang.parse_task_name)
            return
        slavereq.task.name = site
    if not slavereq.task.creator:
        slavereq.task.creator = get_id(target)
    await need_slave(message, slavereq)
    app.loop.create_task(need_sub(message, slavereq))


async def need_slave(message: Message, slavereq: SlaveRequest):
    if slavereq.slave is None:
        if CONFIG.slaveConfig.slaves:
            slave_comment_list = [s.comment for s in CONFIG.slaveConfig.slaves if not s.hidden]
            await SlaveSelector(slave_comment_list, message).build()
        else:
            await message.reply(lang.slave_not_found)


async def need_sub(_: Message, slavereq: SlaveRequest):
    if not slavereq.task.url:
        return
    subcoll = SubCollector(slavereq.task.url, CONFIG)
    maybe_data = await subcoll.get_sub_config(proxy=CONFIG.network.httpProxy)
    if isinstance(maybe_data, bool):
        slavereq.error = f"{lang.subget_err} {slavereq.task.name}"
        return
    clashcleaner = ClashCleaner(maybe_data)
    clashcleaner.node_filter(slavereq.runtime.includeFilter, slavereq.runtime.excludeFilter)
    nodes = clashcleaner.get_proxies()
    if isinstance(nodes, list):
        slavereq.proxies = nodes




