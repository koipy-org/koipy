#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: www
@Date: 2024/6/11 下午6:11
@Description: 
"""
import ctypes
import platform
import time
import sys

from pyrogram import Client
from pyrogram.types import Message

from bot.config import lang
from bot import __version__, COMMIT, BUILD_TIME
from bot.queue import message_delete_queue


def get_linux_memory_info():
    mem_info = {}
    with open('/proc/meminfo', 'r') as f:
        for line in f:
            key, value = line.split(':')
            mem_info[key.strip()] = int(value.split()[0]) * 1024  # 转换为字节

    total = mem_info['MemTotal']
    available = mem_info.get('MemAvailable',
                             mem_info['MemFree'] + mem_info.get('Buffers', 0) + mem_info.get('Cached', 0))
    used = total - available
    percent = (used / total) * 100

    return {
        'total': total,
        'available': available,
        'used': used,
        'free': mem_info['MemFree'],
        'percent': percent,
        'cached': mem_info.get('Cached', 0),
        'buffers': mem_info.get('Buffers', 0)
    }


def get_windows_memory_info():
    class MEMORYSTATUSEX(ctypes.Structure):
        _fields_ = [
            ("dwLength", ctypes.c_ulong),
            ("dwMemoryLoad", ctypes.c_ulong),
            ("ullTotalPhys", ctypes.c_ulonglong),
            ("ullAvailPhys", ctypes.c_ulonglong),
            ("ullTotalPageFile", ctypes.c_ulonglong),
            ("ullAvailPageFile", ctypes.c_ulonglong),
            ("ullTotalVirtual", ctypes.c_ulonglong),
            ("ullAvailVirtual", ctypes.c_ulonglong),
            ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
        ]

    memory_status = MEMORYSTATUSEX()
    memory_status.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memory_status))

    total = memory_status.ullTotalPhys
    available = memory_status.ullAvailPhys
    used = total - available
    percent = memory_status.dwMemoryLoad

    return {
        'total': total,
        'available': available,
        'used': used,
        'free': available,  # Windows doesn't distinguish between 'free' and 'available'
        'percent': percent,
        'cached': None,  # Not easily available on Windows
        'buffers': None  # Not easily available on Windows
    }


def get_virtual_memory():
    if sys.platform.startswith('linux'):
        return get_linux_memory_info()
    elif sys.platform.startswith('win'):
        return get_windows_memory_info()
    else:
        raise NotImplementedError(f"Platform {sys.platform} is not supported")


def sysinfo():
    # 系统名称和版本
    system_name = platform.system()
    system_version = platform.version()

    # 系统时间
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # Python版本
    python_version = sys.version

    # 内存使用情况
    mem = get_virtual_memory()
    used_mem = mem.get("used", 0) >> 20  # 将内存使用量转换为MB
    total_mem = mem.get("total", 0) >> 20  # 将总内存转换为MB
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
