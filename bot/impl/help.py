#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: koipy-org
@Date: 2024/6/11 下午9:42
@Description: 
"""
from loguru import logger
from pyrogram.errors import RPCError
from pyrogram.types import Message

from bot import __version__
from bot.check import is_user
from bot.config import CONFIG, lang
from bot.queue import message_delete_queue

help_title = lang.help_title
help_tail = lang.help_tail

tourist_text = f"""
/help [游客]获取帮助菜单
/version [游客]输出版本信息({__version__})
/traffic & /subinfo [游客]获取流量信息
"""
user_text = """测试指令
/test <订阅名> <包含过滤器> <排除过滤器> [用户]进行流媒体测试
/speed <订阅名> <包含过滤器> <排除过滤器> [用户]进行速度测试
/analyze & /topo <订阅名> [用户]进行节点链路拓扑测试
/re <高级参数> <包含过滤器> <排除过滤器> [用户]快速重测上一次测试
/invite <回复一个目标> [用户]临时邀请一个目标进行测试（匿名无法生效）
/share <回复一个目标> [用户]分享订阅的测试权
/new <订阅链接> <订阅名> <访问密码> [用户]添加一个订阅
/sub <订阅名> <访问密码> [用户]查看对应名称的订阅
/checkslaves [用户]检查后端在线情况
"""
admin_text = """/system [管理]查看系统信息
/user [管理]查看所有授权用户的id
/remove [管理]移除一个或多个订阅
/install [管理]安装脚本 
/uninstall [管理]卸载脚本
/setantigroup [管理]切换防拉群模式
/restart [管理]重启整个程序
/reload [管理]重载部分配置(一般情况下用不到)
/panel [管理]bot的控制面板
/update [管理] <回复一个二进制文件>更新BOT主体二进制
/logs <可选:整数n> [管理]输出本次运行的最后n行日志文件
killme [管理]杀死bot的自身进程
"""
other_text = ""


async def helps(_, message: "Message"):
    global user_text, admin_text, tourist_text, other_text
    USER_TARGET = CONFIG.user
    admin = CONFIG.admin
    if lang.help_user:
        user_text = lang.help_user
    if lang.help_tourist:
        tourist_text = lang.help_tourist
    if lang.help_admin:
        admin_text = lang.help_admin
    if lang.help_other:
        other_text = lang.help_other
    if await is_user(message, admin, isalert=False):
        send_text = help_title + "\n" + tourist_text + "\n" + user_text + "\n" + admin_text + "\n" + help_tail
    else:
        if await is_user(message, USER_TARGET, isalert=False):
            send_text = help_title + "\n" + tourist_text + "\n" + user_text + "\n" + help_tail
        else:
            send_text = help_title + "\n" + tourist_text + "\n" + help_tail
    try:
        bot_msg = await message.reply(send_text)
        message_delete_queue.put(bot_msg)
    except RPCError as r:
        logger.error(str(r))
