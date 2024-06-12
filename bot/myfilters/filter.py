#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: koipy-org
@Date: 2024/6/11 下午8:26
@Description: 
"""
from pyrogram import filters
from pyrogram.types import Message
from bot.config import admin, lang
from bot.queue import message_delete_queue


def admin_filter():
    """
    检查管理员是否在配置文件所加载的的列表中
    """

    async def func(_, __, message: "Message"):
        try:
            if message.from_user and message.from_user.id not in admin and str(
                    message.from_user.username) not in admin:
                back_message = await message.reply(lang.is_not_admin)
                message_delete_queue.put_nowait((back_message.chat.id, back_message.id, 10))
                return False
            else:
                return True
        except AttributeError:
            if message.sender_chat and message.sender_chat.id not in admin:
                back_message = await message.reply(lang.is_not_admin)
                message_delete_queue.put_nowait((back_message.chat.id, back_message.id, 10))
                return False
            else:
                return True
        except Exception as e:
            print(e)
            return False

    return filters.create(func)