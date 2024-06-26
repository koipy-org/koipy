#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: koipy-org
@Date: 2024/6/11 下午8:26
@Description: 
"""
import re
from typing import Union, List

from loguru import logger
from pyrogram import filters, Client
from pyrogram.filters import create, Filter
from pyrogram.types import Message, CallbackQuery
from bot.config import admin, lang, CONFIG
from bot.queue import message_delete_queue
from bot.utils import gen_key
from utils.cleaner import ArgCleaner


def admin_filter():
    """
    检查管理员是否在配置文件所加载的的列表中
    """

    async def func(_, __, msg: "Message"):
        try:
            if msg.from_user and msg.from_user.id not in admin and str(
                    msg.from_user.username) not in admin:
                back_message = await msg.reply(lang.is_not_admin)
                message_delete_queue.put_nowait((back_message.chat.id, back_message.id, 10))
                return False
            else:
                return True
        except AttributeError:
            if msg.sender_chat and msg.sender_chat.id not in admin:
                back_message = await msg.reply(lang.is_not_admin)
                message_delete_queue.put_nowait((back_message.chat.id, back_message.id, 10))
                return False
            else:
                return True
        except Exception as e:
            print(e)
            return False

    return filters.create(func)


def command(commands: Union[str, List[str]], prefixes: Union[str, List[str]] = "/", case_sensitive: bool = False):
    """Filter commands, i.e.: text messages starting with "/" or any other custom prefix.

    Parameters:
        commands (``str`` | ``list``):
            The command or list of commands as string the filter should look for.
            Examples: "start", ["start", "help", "settings"]. When a message text containing
            a command arrives, the command itself and its arguments will be stored in the *command*
            field of the :obj:`~pyrogram.types.Message`.

        prefixes (``str`` | ``list``, *optional*):
            A prefix or a list of prefixes as string the filter should look for.
            Defaults to "/" (slash). Examples: ".", "!", ["/", "!", "."], list(".:!").
            Pass None or "" (empty string) to allow commands with no prefix at all.

        case_sensitive (``bool``, *optional*):
            Pass True if you want your command(s) to be case sensitive. Defaults to False.
            Examples: when True, command="Start" would trigger /Start but not /start.
    """
    command_re = re.compile(r"([\"'])(.*?)(?<!\\)\1|(\S+)")

    async def func(flt, client: Client, msg: Message):
        username = client.me.username or ""
        text = msg.text or msg.caption
        msg.command = None

        if not text:
            return False

        for prefix in flt.prefixes:
            if not text.startswith(prefix):
                continue

            without_prefix = text[len(prefix):]
            tgargs = ArgCleaner.getarg(without_prefix, " ")
            for cmd in flt.commands:
                from_cmd = tgargs[0]
                without_username = from_cmd.split("@")[0]
                if f"@" in from_cmd and f"@{username}" not in from_cmd:
                    continue
                if cmd != without_username:
                    continue
                without_command = re.sub(rf"{cmd}(?:@?{username})?\s?", "", without_prefix, count=1,
                                         flags=re.IGNORECASE if not flt.case_sensitive else 0)

                # match.groups are 1-indexed, group(1) is the quote, group(2) is the text
                # between the quotes, group(3) is unquoted, whitespace-split text

                # Remove the escape character from the arguments
                msg.command = [cmd] + [
                    re.sub(r"\\([\"'])", r"\1", m.group(2) or m.group(3) or "")
                    for m in command_re.finditer(without_command)
                ]
                return True

        return False

    commands = commands if isinstance(commands, list) else [commands]
    commands = {c if case_sensitive else c.lower() for c in commands}

    prefixes = [] if prefixes is None else prefixes
    prefixes = prefixes if isinstance(prefixes, list) else [prefixes]
    prefixes = set(prefixes) if prefixes else {""}

    return create(
        func,
        "CommandFilter",
        commands=commands,
        prefixes=prefixes,
        case_sensitive=case_sensitive
    )


def prefix_filter(prefix: str):
    """
    特定文本前缀过滤器，支持回调数据过滤。
    """

    async def func(flt, _, update: Union[Message, CallbackQuery]):
        return update.text.startswith(flt.prefix) if isinstance(update, Message) else update.data.startswith(flt.prefix)

    return filters.create(func, prefix=prefix)


pflt = prefix_filter


def message(msg_key: str):
    """
    消息id过滤器
    """

    async def func(flt, _, update: Union[Message, CallbackQuery]):
        return gen_key(update) == flt.msg_key if isinstance(update, Message) else gen_key(update.message) == flt.msg_key

    return filters.create(func, msg_key=msg_key)


def callback_master(user_list: list = None, strict: bool = False):
    """
    :param user_list: 用户名单
    :param strict: 严格模式，如果为true,则每个任务的内联键盘只有任务的发起者能操作，若为false，则所有用户都能操作内联键盘。
    :return:
    """

    async def func(flt, _, update: CallbackQuery):
        master = []
        if flt.user_list and not strict:
            master.extend(flt.user_list)
        try:
            from_id = None
            if update.message and update.message.reply_to_message:
                r_msg = update.message.reply_to_message
                if r_msg.from_user:
                    from_id = r_msg.from_user.id
                elif r_msg.sender_chat:
                    from_id = r_msg.sender_chat.id
            if from_id:
                master.append(from_id)  # 发起测试任务的用户id
            if int(update.from_user.id) not in master:
                await update.answer("不要乱动别人的操作哟👻", show_alert=True)
                return False
            else:
                return True
        except AttributeError:
            master.append(update.message.reply_to_message.sender_chat.id)
            if int(update.from_user.id) in master:  # 如果不在master名单是不会有权限的
                return True
            if str(update.from_user.username) in master:
                return True
            else:
                await update.answer(f"不要乱动别人的操作哟👻", show_alert=True)
                return False
        except Exception as e:
            logger.error(str(e))
            return False

    return filters.create(func, user_list=user_list, strict=strict)


def call_data_filter(data: str) -> "Filter":
    """
    特定的回调数据过滤器。比如回调数据 callback.data == "close" ,data == "close"。那么成功命中，返回真
    """

    async def func(flt, _, query):
        return flt.data == query.data

    # "data" kwarg is accessed with "flt.data" above
    return filters.create(func, data=data)
