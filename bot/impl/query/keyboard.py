#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: www
@Date: 2024/6/25 上午11:46
@Description: 
"""
import asyncio

from loguru import logger
from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from bot.config import CONFIG
from bot.utils import gen_key
from bot.impl.query.selector import ACCEPT_CACHE, SLAVE_REQ_CACHE, submit, ScriptSelector
from bot.impl.button import *
from utils.types.task import SlaveRequest
from utils.types.items import *

_LOCK = asyncio.Lock()


async def editkeybord_yes_or_no(_: Client, call: CallbackQuery):
    """
    反转✅和❌
    """
    le = len(Api.script)
    script_name = str(call.data)[le:]
    mode = 0 if "✅" in script_name else 1
    inline_keyboard = call.message.reply_markup.inline_keyboard
    for b_1 in inline_keyboard:
        for b in b_1:
            if b.text == script_name:
                b.text = b.text.replace("✅", "❌") if mode == 0 else b.text.replace("❌", "✅")
                b.callback_data = Api.script + b.text
                IKM2 = InlineKeyboardMarkup(inline_keyboard)
                await call.message.edit_text(call.message.text, reply_markup=IKM2)


async def editkeybord_reverse(_: Client, callback_query: CallbackQuery):
    """
    翻转所有涉及✅和❌ 的键
    """
    edit_mess = callback_query.message
    edit_text = edit_mess.text
    inline_keyboard = callback_query.message.reply_markup.inline_keyboard
    for b_1 in inline_keyboard:
        for b in b_1:
            if "❌" in b.text:
                b.text = b.text.replace("❌", "✅")
                b.callback_data = Api.script + b.text
            elif "✅" in b.text:
                b.text = b.text.replace("✅", "❌")
                b.callback_data = Api.script + b.text
    IKM = InlineKeyboardMarkup(inline_keyboard)
    await edit_mess.edit_text(edit_text, reply_markup=IKM)


async def select_page_ok(_: Client, call: CallbackQuery):
    msg_key = gen_key(call.message.reply_to_message)
    if msg_key and msg_key in ACCEPT_CACHE:
        msg_cache = ACCEPT_CACHE[msg_key]
        if not isinstance(msg_cache, dict):
            return
    else:
        msg_cache = {}
    current_page = None
    selected = set() if "selected" not in msg_cache else msg_cache.get("selected")
    locked = set() if "locked" not in msg_cache else msg_cache.get("locked")
    inline_keyboard = call.message.reply_markup.inline_keyboard
    page_row = None
    for b_1 in inline_keyboard:
        for b in b_1:
            if len(b.text) > 1 and b.text[0] == "✅":
                script_name = b.text[1:]
                selected.add(script_name)
            elif "/" in b.text and b.callback_data == "blank":
                page_row = b_1
                current_page = int(b.text.split("/")[0])
    if isinstance(current_page, int):
        locked.add(current_page)
    async with _LOCK:
        msg_cache["selected"] = selected
        msg_cache["locked"] = locked
        ACCEPT_CACHE[msg_key] = msg_cache
    board = [
        [InlineKeyboardButton(lang.selected, 'blank')],
        page_row,
        [Cancel(), OKButton()]
    ]
    IKM = InlineKeyboardMarkup(board)
    await call.message.edit_text(lang.selected_script + str(selected), reply_markup=IKM)


async def close(_: Client, call: CallbackQuery):
    await call.message.delete(revoke=True)


async def cancel(_: Client, call: CallbackQuery):
    await call.message.edit_text(lang.b_cancel2)


async def test_all(_app: Client, call: CallbackQuery):
    items = [s.name for s in CONFIG.scriptConfig.scripts]
    items = set(items)
    msg_key = gen_key(call.message.reply_to_message)
    if msg_key is None:
        return
    msg_cache = ACCEPT_CACHE.get(msg_key, {})
    selected = msg_cache.get("selected", set())
    selected.update(items)
    selected.add(TCPTest.name)
    selected.add(HTTPTest.name)
    selected.add(AvgSpeed.name)
    selected.add(MaxSpeed.name)
    selected.add(PerSecond.name)
    selected.add(UDPType.name)
    msg_cache["selected"] = selected
    ACCEPT_CACHE[msg_key] = msg_cache
    await ScriptSelector.accept(_app, call)

# async def script_ok(app: Client, call: CallbackQuery):
#     msg_key = gen_key(call.message.reply_to_message)
#     if msg_key is None:
#         return
#     await call.message.edit_text(lang.script_ok)
#     msg_cache = ACCEPT_CACHE.get(msg_key, {})
#     if not msg_cache or not isinstance(msg_cache, dict):
#         logger.warning(lang.cache_not_found)
#         return
#
#     slavereq = SLAVE_REQ_CACHE.pop(msg_key, SlaveRequest())
#     sort_str = msg_cache.get("sort", SortType.ORIGIN)
#     slave_name = msg_cache.get("slave", None)
#     selected = list(msg_cache.get("selected", set()))
#     if isinstance(slave_name, str):
#         for s in CONFIG.slaveConfig.slaves:
#             if s.comment == slave_name:
#                 slavereq.slave = s
#     slavereq.runtime.sort = sort_str
#     slavereq.merge_items(selected, CONFIG)
#     if slavereq.task.messageID and slavereq.task.chatID:
#         target = await app.get_messages(slavereq.task.chatID, slavereq.task.messageID)
#         await submit(app, target, slavereq)
