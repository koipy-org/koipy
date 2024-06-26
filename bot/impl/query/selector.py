#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: www
@Date: 2024/6/23 下午6:10
@Description: 
"""
import asyncio
from copy import deepcopy
from typing import List, Union

from loguru import logger
from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, CallbackQuery, InlineKeyboardButton
from pyrogram.handlers import CallbackQueryHandler
from pyrogram.errors import RPCError

from bot.impl.button import *
from bot.config import CONFIG, lang
from bot.init import app
from bot.myfilters.filters import prefix_filter, message as msg_flt
from bot.utils import gen_key
from bot.queue import handler_delete_queue
from bot.backend import miaospeed_client
from utils.types.config import SortType, MiaoSpeedSlave
from utils.types.task import SlaveRequest

SELECTOR_HANDLER_GROUP = 3
ACCEPT_CACHE = {}
SLAVE_REQ_CACHE = {}


def page_frame(pageprefix: str, contentprefix: str, content: List[str], split: str = ':', page: int = 1, row: int = 5,
               column: int = 1) -> list:
    """
    翻页框架，返回一个内联键盘列表：[若干行的内容按钮,(上一页、页数预览、下一页）按钮]
    pageprefix: 页面回调数据的前缀字符串
    contentprefix: 具体翻页内容的回调数据的前缀字符串
    """
    max_page = int(len(content) / (row * column)) + 1
    pre_page_text = page - 1 if page - 1 > 0 else 1
    next_page_text = page + 1 if page < max_page else max_page
    pre_page = IKB(lang.page1, callback_data=f'{pageprefix}{pre_page_text}')
    next_page = IKB(lang.page2, callback_data=f'{pageprefix}{next_page_text}')
    preview = IKB(f'{page}/{max_page}', callback_data='blank')

    if page > max_page:
        logger.error("Page Error.")
        return []
    if page == 1:
        pre_page.text = '        '
        pre_page.callback_data = 'blank'

    if page == max_page:
        next_page.text = '        '
        next_page.callback_data = 'blank'
        content_keyboard = []
        temp_row = []
        for i, c in enumerate(content[(max_page - 1) * row * column:]):
            if i % column == 0 and i != 0:
                content_keyboard.append(deepcopy(temp_row))
                temp_row.clear()
            temp_row.append(IKB(c, f'{contentprefix}{split}{c}'))
        content_keyboard.append(deepcopy(temp_row))
    else:
        content_keyboard = []
        temp_row = []
        for i, c in enumerate(content[(page - 1) * row * column:page * row * column]):
            if i % column == 0 and i != 0:
                content_keyboard.append(deepcopy(temp_row))
                temp_row.clear()
            temp_row.append(IKB(c, f'{contentprefix}{split}{c}'))
        content_keyboard.append(deepcopy(temp_row))
    content_keyboard.append([pre_page, preview, next_page])
    return content_keyboard


async def submit(_app: "Client", message: "Message", slavereq: SlaveRequest):
    botmsg = await message.reply(lang.submit, quote=True)
    if slavereq.error:
        await botmsg.edit_text(slavereq.error)
    elif slavereq.ready():
        slavereq.task.botMsgID = botmsg.id
        slavereq.task.botMsgChatID = botmsg.chat.id
        if isinstance(slavereq.slave, MiaoSpeedSlave):
            slavereq.slave.invoker = _app.me.id
        await miaospeed_client(_app, slavereq)
        # import pprint
        # slavereq.items = []
        # pprint.pprint(slavereq)
    else:
        await botmsg.edit_text(lang.submit2)


class BaseSelector:
    """
    bot按钮翻页选择器
    """
    page_api: str = None
    content_api: str = None
    bot_msg: "Message" = None
    _handler_cache = None
    _lock = threading.Lock()

    def __init__(self, data: List[str], page_api: str, content_api: str, msg: "Message" = None, chat_id: int = None,
                 split: str = '', page: int = 1, row: int = 5, column: int = 1):
        """

        :param data:
        :param page_api:
        :param content_api:
        :param msg: 如果指定,则会回复那条消息
        :param chat_id: 如果msg未指定，则指定chat_id，这两者互斥
        """
        self.page_api = page_api
        self.content_api = content_api
        self.msg = msg
        self.chat_id = chat_id if self.msg is None else self.msg.chat.id
        self.split = split
        self.page = page
        self.row = row
        self.column = column
        if self.chat_id is None and self.msg is None:
            raise ValueError("No chat_id or msg parameter found. ")
        self.content = []
        if isinstance(data, list):
            self.content = data
        self.result = None
        self.queue = asyncio.Queue(1)

    async def send(self, text: str, IKM: InlineKeyboardMarkup = None, **kwargs):
        kwargs.update({"reply_markup": IKM})
        if self.bot_msg and isinstance(self.bot_msg, Message):
            self.bot_msg = await self.bot_msg.edit_text(text, **kwargs)
        else:
            if self.msg:
                quote = kwargs.pop("quote", True)
                self.bot_msg = await self.msg.reply(text, quote=quote, **kwargs)
            elif self.chat_id:
                self.bot_msg = await app.send_message(self.chat_id, text, **kwargs)

    async def build(self):
        raise NotImplementedError

    @classmethod
    async def accept(cls, _app: Client, call: CallbackQuery):
        raise NotImplementedError

    async def update(self):
        raise NotImplementedError

    @classmethod
    def clean(cls):
        try:
            with cls._lock:
                if cls._handler_cache:
                    for _h in cls._handler_cache:
                        app.dispatcher.groups[SELECTOR_HANDLER_GROUP].remove(_h)
                    cls._handler_cache.clear()
        except Exception as e:
            logger.error(str(e))


class ScriptSelector(BaseSelector):
    page_api: str = Api.script_page
    content_api: str = Api.script
    split: str = ""
    _handler_cache = None

    def __init__(self, msg: "Message" = None, chat_id: int = None):
        self._handler_cache = []
        self.content = ["✅" + s.name for s in CONFIG.scriptConfig.scripts]
        self.row = 5
        self.column = 2
        super().__init__(self.content, self.page_api, self.content_api, msg, chat_id, row=self.row, column=self.column)

    async def build(self):
        await self.update()

        async def handler_closure_2(_, call: Union[CallbackQuery, Message]):
            try:
                self.page = 1 if isinstance(call, Message) else int(call.data[len(self.page_api):])
            except IndexError:
                self.page = 1
            await self.update()

        call_handler2 = CallbackQueryHandler(handler_closure_2,
                                             filters=prefix_filter(self.page_api) & msg_flt(gen_key(self.bot_msg)))
        app.add_handler(call_handler2, SELECTOR_HANDLER_GROUP)
        handler_delete_queue.put(call_handler2, SELECTOR_HANDLER_GROUP, 600)
        return self

    async def update(self):
        if self.bot_msg is not None:
            self.bot_msg = await app.get_messages(self.bot_msg.chat.id, self.bot_msg.id)
        msg_key = gen_key(self.msg)
        locked = None
        board = page_frame(self.page_api, self.content_api, self.content, self.split, self.page, self.row, self.column)
        if msg_key and msg_key in ACCEPT_CACHE:
            msg_cache: dict = ACCEPT_CACHE[msg_key]
            locked = msg_cache.get("locked", set())

        if isinstance(locked, set) and self.page in locked:
            board = [board[-1]]
            board.insert(0, [InlineKeyboardButton(lang.selected, 'blank')])
            board.append([Cancel(), OKButton()])
        else:
            board.insert(0, [OKPage()])
            board.extend([
                [TestAll(), Alive()],
                [Cancel(), Reverse()],
                [OKButton()]
            ])

        IKM = InlineKeyboardMarkup(board)
        send_text = lang.script_select if self.bot_msg is None else self.bot_msg.text
        await self.send(send_text, IKM)

    @classmethod
    async def accept(cls, _app: Client, call: CallbackQuery):
        msg_key = gen_key(call.message.reply_to_message)
        if msg_key is None:
            return
        # await call.message.edit_text(lang.script_ok)

        msg_cache = ACCEPT_CACHE.get(msg_key, {})
        if not msg_cache or not isinstance(msg_cache, dict):
            logger.warning(lang.cache_not_found)
            return

        slavereq = SLAVE_REQ_CACHE.pop(msg_key, SlaveRequest())
        sort_str = msg_cache.get("sort", SortType.ORIGIN)
        slave_name = msg_cache.get("slave", None)
        selected = list(msg_cache.get("selected", set()))
        if isinstance(slave_name, str):
            for s in CONFIG.slaveConfig.slaves:
                if s.comment == slave_name:
                    slavereq.slave = s
        slavereq.runtime.sort = sort_str
        slavereq.merge_items(selected, CONFIG)
        if slavereq.task.messageID and slavereq.task.chatID:
            target = await app.get_messages(slavereq.task.chatID, slavereq.task.messageID)
            await call.message.delete(revoke=True)
            await submit(app, target, slavereq)


class SortSelector(BaseSelector):
    page_api: str = ""
    content_api: str = Api.sort
    split: str = ""
    _handler_cache = None

    def __init__(self, msg: "Message" = None, chat_id: int = None):
        self._handler_cache = []
        super().__init__([], self.page_api, self.content_api, msg, chat_id)

    async def update(self):
        board = [[SortOrigin()], [SortRHttp(), SortHttp()], [SortAvgSpeed(), SortAvgRSpeed()],
                 [SortMaxSpeed(), SortMaxRSpeed()], [Close()]]
        IKM = InlineKeyboardMarkup(board)
        await self.send(lang.sort_select, IKM)

    async def build(self):
        await self.update()
        return self

    @classmethod
    async def next(cls, selector: ScriptSelector):
        cls.clean()
        await selector.build()

    @classmethod
    async def accept(cls, _app: Client, call: CallbackQuery):
        """
        接受从tg前端的值
        :return: str
        """
        le = len(cls.content_api) + len(cls.split)
        msg_key = gen_key(call.message.reply_to_message)
        msg_cache = ACCEPT_CACHE.get(msg_key, {})

        sort_str = str(call.data)[le:]
        sort_str_parser = {
            "origin": "订阅原序",
            "rhttp": "HTTP降序",
            "http": "HTTP升序",
            "aspeed": "平均速度升序",
            "arspeed": "平均速度降序",
            "mspeed": "最大速度升序",
            "mrspeed": "最大速度降序",
        }
        sort_str = str(sort_str)
        sort_str = sort_str_parser.get(sort_str, None)
        msg_cache['sort'] = sort_str
        ACCEPT_CACHE[msg_key] = msg_cache
        selector = ScriptSelector(call.message.reply_to_message, call.message.chat.id)
        selector.bot_msg = call.message
        await cls.next(selector)


class SlaveSelector(BaseSelector):
    page_api: str = Api.slave_page
    content_api: str = Api.slave_content
    split: str = "?comment="
    _handler_cache = None

    def __init__(self, data: List[str], msg: "Message" = None, chat_id: int = None, split: str = '', page: int = 1,
                 row: int = 5, column: int = 1):
        self._handler_cache = []
        split = self.split or split
        super().__init__(data, Api.slave_page, Api.slave_content, msg, chat_id, split, page, row, column)

    @classmethod
    async def next(cls, selector: SortSelector):
        cls.clean()
        await selector.build()

    async def build(self):
        """
        将翻页框架应用到
        """
        await self.update()

        async def handler_closure_2(_, call: Union[CallbackQuery, Message]):
            try:
                self.page = 1 if isinstance(call, Message) else int(call.data[len(self.page_api):])
            except IndexError:
                self.page = 1
            await self.update()

        call_handler2 = CallbackQueryHandler(handler_closure_2,
                                             filters=prefix_filter(self.page_api) & msg_flt(gen_key(self.bot_msg)))
        app.add_handler(call_handler2, SELECTOR_HANDLER_GROUP)
        if self._handler_cache is None:
            self._handler_cache = []
        self._handler_cache.append(call_handler2)
        return self

    async def update(self):
        board = page_frame(self.page_api, self.content_api, self.content, self.split, self.page, self.row, self.column)
        board.append([Close()])
        IKM = InlineKeyboardMarkup(board)
        await self.send(lang.slave_select, IKM)

    @classmethod
    async def accept(cls, _app: Client, call: CallbackQuery):
        """
        接受从tg前端的值
        :return: str
        """
        le = len(cls.content_api) + len(cls.split)
        msg_key = gen_key(call.message.reply_to_message)
        msg_cache = ACCEPT_CACHE.get(msg_key, {})
        msg_cache['slave'] = str(call.data)[le:]
        ACCEPT_CACHE[msg_key] = msg_cache
        try:
            # await call.message.delete(revoke=True)
            sort_selector = SortSelector(call.message.reply_to_message, call.message.chat.id)
            sort_selector.bot_msg = call.message
            await cls.next(sort_selector)
        except RPCError as e:
            logger.error(str(e))
