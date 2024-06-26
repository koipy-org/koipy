#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: www
@Date: 2024/6/11 下午6:11
@Description: 
"""
import platform
import time
import sys

import psutil
from pyrogram import Client
from pyrogram.types import Message

from bot.config import lang
from bot import __version__, COMMIT, BUILD_TIME
from bot.queue import message_delete_queue


def sysinfo():
    # 系统名称和版本
    system_name = platform.system()
    system_version = platform.version()

    # 系统时间
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # Python版本
    python_version = sys.version

    # 内存使用情况
    mem = psutil.virtual_memory()
    used_mem = mem.used >> 20  # 将内存使用量转换为MB
    total_mem = mem.total >> 20  # 将总内存转换为MB
    compiled = getattr(sysinfo, "__compiled__", "")
    if compiled:
        compiled = f"({compiled})"
    sysinfo_str = (f"{lang.sysn}: `{system_name}` \n"
                   f"{lang.sysv}: `{system_version}` \n"
                   f"{lang.syst}: `{current_time}` \n"
                   f"{lang.pyv}{compiled}: `{python_version}` \n"
                   f"{lang.mem}: `{used_mem}MB/{total_mem}MB ({int(float(used_mem) / total_mem * 100)}%)`\n")
    return sysinfo_str


def botinfo():
    bot_info = (f"{lang.bot_version}: `{__version__}`\n"
                f"{lang.commit}: `{COMMIT}`\n"
                f"{lang.build_time}: `{BUILD_TIME}`\n")
    return bot_info


async def info(_: "Client", msg: "Message"):
    sys_info = sysinfo()
    bot_info = botinfo()
    bot_msg = await msg.reply(sys_info + "\n" + bot_info)
    message_delete_queue.put(bot_msg, 10, revoke=True)


async def version(_: "Client", msg: "Message"):
    bot_info = botinfo()
    bot_msg = await msg.reply(bot_info)
    message_delete_queue.put(bot_msg, 10)


if __name__ == "__main__":
    sysinfo()
