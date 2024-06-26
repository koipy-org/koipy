#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: www
@Date: 2024/6/23 下午7:16
@Description: 
"""
import threading

from pyrogram.types import InlineKeyboardButton as IKB
from bot.config import lang
from bot.api import Api


class AtomicButton(IKB):
    _instance = None
    _lock: threading.Lock = threading.Lock()
    _text: str = None
    _callback_data = None

    def __new__(cls, *args, **kwargs):
        # 单例模式
        if cls._instance is None:
            with cls._lock:
                # 双重检查
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, text: str = None, callback_data: str = None):
        text = text or self._text or ""
        data = callback_data or self._callback_data or ""
        super().__init__(text, data)


class VariableStateButton(IKB):
    status = True


class OKButton(AtomicButton):
    _text = lang.b_ok
    _callback_data = Api.script_ok


class OKButton2(AtomicButton):
    _text = lang.b_ok2
    _callback_data = Api.select_ok


class Reverse(AtomicButton):
    _text = lang.b_reverse
    _callback_data = Api.reverse


# netflix youtube disdey+
class NYD(AtomicButton):
    _text = lang.b_nyd
    _callback_data = Api.nyd


class Cancel(AtomicButton):
    _text = lang.b_cancel
    _callback_data = Api.cancel


class Alive(AtomicButton):
    _text = lang.b_alive
    _callback_data = Api.alive


class OKPage(AtomicButton):
    _text = lang.b_okpage
    _callback_data = Api.okpage


class TestAll(AtomicButton):
    _text = lang.b_all
    _callback_data = Api.all


class SortOrigin(AtomicButton):
    _text = lang.b_origin
    _callback_data = Api.sort_origin


class SortRHttp(AtomicButton):
    _text = lang.b_rhttp
    _callback_data = Api.sort_rhttp


class SortHttp(AtomicButton):
    _text = lang.b_http
    _callback_data = Api.sort_http


class SortAvgSpeed(AtomicButton):
    _text = lang.b_aspeed
    _callback_data = Api.sort_aspeed


class SortAvgRSpeed(AtomicButton):
    _text = lang.b_arspeed
    _callback_data = Api.sort_arspeed


class SortMaxSpeed(AtomicButton):
    _text = lang.b_mspeed
    _callback_data = Api.sort_mspeed


class SortMaxRSpeed(AtomicButton):
    _text = lang.b_mrspeed
    _callback_data = Api.sort_mrspeed


class Close(AtomicButton):
    _text = lang.b_close
    _callback_data = Api.keyboard_close


class Back(AtomicButton):
    _text = lang.b_back
    _callback_data = Api.back


class DelCFG(AtomicButton):
    _text = lang.b_del_conf
    _callback_data = Api.cfg_del


class EditCFG(AtomicButton):
    _text = lang.b_edit_conf
    _callback_data = Api.cfg_edit


class AddCFG(AtomicButton):
    _text = lang.b_add_conf
    _callback_data = Api.cfg_new
