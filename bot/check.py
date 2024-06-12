#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: koipy-org
@Date: 2024/6/11 下午9:42
@Description:
"""
import asyncio
import hashlib
import re
import contextlib
from typing import Union

from pyrogram import Client
from pyrogram.enums import ChatAction
from pyrogram.types import Message, CallbackQuery
from pyrogram.errors import RPCError, MessageDeleteForbidden
from loguru import logger
from pyrogram.filters import private_filter

from bot.config import CONFIG
from bot.queue import message_delete_queue
from utils.types.config import UserList, AdminList

"""
这个模块主要是一些检查函数，用来验证某个值是否合法。一般是返回布尔值
"""


def get_telegram_id_from_message(message: "Message"):
    """
    获得唯一确定身份标识的id
    为什么我会写这个方法？因为该死的telegram里有频道匿名身份和普通用户身份，它们的id不是同一个属性。
    :param message:
    :return:
    """
    ID = -1
    try:
        if message and message.from_user:
            ID = message.from_user.id
        elif message and message.sender_chat:
            ID = message.sender_chat.id
        return ID
    except AttributeError:
        ID = message.sender_chat.id
        return ID
    except Exception as e:
        logger.error(str(e))
        return ID


get_id = get_telegram_id_from_message  # 别名


async def is_port_in_use(host='127.0.0.1', port=80):
    """
    检查主机端口是否被占用
    :param host:
    :param port:
    :return:
    """
    try:
        reader, writer = await asyncio.open_connection(host, port)
        writer.close()
        await writer.wait_closed()
        logger.warning(fr"{port} 已被占用，请更换。")
        return True
    except ConnectionRefusedError:
        return False


async def check_port(start: int, end: int):
    if start > end:
        start, end = end, start
    tasks = []
    for i in range(start, end):
        tasks.append(asyncio.create_task(is_port_in_use(port=i)))
    results = await asyncio.gather(*tasks)
    return True in results


async def is_shared(message, shareid: list):
    """
    检查是否在分享名单中,若在返回真，否则返回假。
    :param message: 消息对象
    :param shareid: 共享名单
    :return: [true, false]
    """
    try:
        ID = message.from_user.id
    except AttributeError:
        ID = message.sender_chat.id
    return str(ID) in shareid


async def is_callback_master(call: CallbackQuery, user_list: UserList = None, strict: bool = False,
                             answer: str = "不要乱动别人的操作哟👻"):
    """
    :param answer: 回答
    :param call: 回调数据结构
    :param user_list: 用户名单
    :param strict: 严格模式，如果为true,则每个任务的内联键盘只有任务的发起者能操作，若为false，则所有用户都能操作内联键盘。
    :return:
    """
    master = []
    if user_list and not strict:
        master.extend(user_list)
    try:
        from_id = None
        from_username = None
        if call.message and call.message.reply_to_message:
            r_msg = call.message.reply_to_message
            if r_msg.from_user:
                from_id = r_msg.from_user.id
            elif r_msg.sender_chat:
                from_id = r_msg.sender_chat.id
            if r_msg.from_user.username:
                from_username = r_msg.from_user.username
        if from_id:
            master.append(from_id)  # 发起测试任务的用户id

        if int(call.from_user.id) not in master or from_username not in master:
            if answer:
                await call.answer(answer, show_alert=True)
            return False
        else:
            return True

    except AttributeError:
        return False
    except Exception as e:
        logger.error(str(e))
        return False


async def check_node(backmsg: Message, core, nodenum: int) -> bool:
    """
    检查节点数量是否超出限制
    """
    flag = False
    if nodenum == 0:
        await backmsg.edit_text("❌节点数量为空，请检查你的过滤器或者订阅格式是否正确")
        flag = True
    if type(core).__name__ == 'SpeedCore':
        if CONFIG.runtime.speedNodes < nodenum:
            await backmsg.edit_text("⚠️节点数量超出限制，已取消测试。")
            flag = True
    if flag:
        return True
    return False


async def is_subowner(message: "Message", bot_message: "Message", subinfo: dict, admin: AdminList, password: str):
    """
    检查是否是订阅的拥有者
    :param password:
    :param admin: 管理员列表名单
    :param bot_message: bot自身的消息
    :param message: 触发指令的那条消息
    :param subinfo: config.get_sub()返回的字典
    :return: True|False
    """
    try:
        ID = message.from_user.id
    except AttributeError:
        ID = message.sender_chat.id
    if not subinfo:
        await bot_message.edit_text("❌找不到该任务名称，请检查参数是否正确。")
        message_delete_queue.put(bot_message, 10)
        # await back_message.delete()
        return False
    subpwd = subinfo.get('password', '')
    subowner = subinfo.get('owner', '')
    subuser = subinfo.get('share', [])
    if await is_user(message, admin, isalert=False):
        # 管理员至高权限
        return True
    if (subowner and subowner == ID) or await is_shared(message, subuser):
        if hashlib.sha256(password.encode("utf-8")).hexdigest() == subpwd:
            return True
        else:
            message_delete_queue.put(bot_message, 10)
            return False
    else:
        await bot_message.edit_text("❌身份ID不匹配，您无权使用该订阅。")
        message_delete_queue.put(bot_message, 10)
        return False


async def is_user(message: "Message", user: Union[UserList, AdminList], isalert=True):
    """
    检查是否是用户，如果是返回真
    :param isalert: 是否发送反馈给bot前端
    :param user: 用户列表
    :param message: 消息对象
    :return: bool
    """
    ID = get_id(message)
    username = None
    if message.from_user and message.from_user.username:
        username = message.from_user.username
    if ID in user or (username and username in user):
        return True
    else:
        if isalert:
            m2 = await message.reply("⚠️您似乎没有使用权限，请联系bot的管理员获取授权")
            message_delete_queue.put(m2, 10)
        return False


async def check_url(message, url):
    """
    检查url
    :param message:
    :param url:
    :return: bool
    """
    if not url:
        try:
            m2 = await message.edit_text("⚠️无效的订阅地址，请检查后重试。")
            message_delete_queue.put_nowait((m2.chat.id, m2.id, 10))
        except RPCError as r:
            logger.error(r)
        return True
    return False


async def check_sub(message, subconfig):
    """
    检查订阅是否获取成功
    :param message:
    :param subconfig:
    :return: bool
    """
    if not subconfig:
        logger.warning("ERROR: 无法获取到订阅文件")
        try:
            m2 = await message.edit_text("ERROR: 无法获取到订阅文件")
            message_delete_queue.put_nowait((m2.chat.id, m2.id, 10))
        except RPCError as r:
            logger.error(r)
        return True
    else:
        return False


async def check_nodes(message, nodenum, args: tuple, max_num=300):
    """
    检查获得的关键信息是否为空，以及节点数量是否大于一定数值
    :param max_num: 最大节点数量
    :param message: 消息对象
    :param nodenum: 节点数量
    :param args: 若干信息
    :return: bool
    """
    if not nodenum:
        try:
            m2 = await message.edit_text("❌发生错误，请检查订阅文件")
            message_delete_queue.put_nowait((m2.chat.id, m2.id, 10))
            return True
        except RPCError as r:
            logger.error(r)
    for arg in args:
        if arg is None:
            try:
                m3 = await message.edit_text("❌发生错误，请检查订阅文件")
                message_delete_queue.put_nowait((m3.chat.id, m3.id, 10))
            except RPCError as r:
                logger.error(r)
            return True
        else:
            pass
    if nodenum > max_num:
        logger.warning("❌节点数量过多！已取消本次测试")
        try:
            m4 = await message.edit_text("❌节点数量过多！已取消本次测试")
            message_delete_queue.put_nowait((m4.chat.id, m4.id, 10))
        except RPCError as r:
            logger.error(r)
        return True
    else:
        return False


async def check_speed_nodes(message, nodenum, args: tuple, speed_max_num=CONFIG.runtime.speedNodes):
    """
    检查获得的关键信息是否为空，以及节点数量是否大于一定数值
    :param speed_max_num: 最大节点数量
    :param message: 消息对象
    :param nodenum: 节点数量
    :param args: 若干信息
    :return: bool
    """
    if not nodenum:
        try:
            m2 = await message.edit_text("❌发生错误，请检查订阅文件")
            message_delete_queue.put_nowait((m2.chat.id, m2.id, 10))
            return True
        except RPCError as r:
            logger.error(r)
    for arg in args:
        if arg is None:
            try:
                m3 = await message.edit_text("❌发生错误，请检查订阅文件")
                message_delete_queue.put_nowait((m3.chat.id, m3.id, 10))
            except RPCError as r:
                logger.error(r)
            return True
        else:
            pass
    if nodenum > speed_max_num:
        logger.warning(f"❌节点数量超过了{speed_max_num}个的限制！已取消本次测试")
        try:
            m4 = await message.edit_text(f"❌节点数量超过了{speed_max_num}个的限制！已取消本次测试")
            message_delete_queue.put_nowait((m4.chat.id, m4.id, 10))
        except RPCError as r:
            logger.error(r)
        return True
    else:
        return False


async def check_photo(app: "Client", msg_id: int, botmsg_id: int, chat_id: int, name: str, wtime: str,
                      size: tuple = None):
    """
    检查图片是否生成成功
    :param app: bot客户端
    :param wtime: 消耗时间
    :param msg_id: 发起任务的消息id
    :param botmsg_id: bot消息id
    :param chat_id: 对话id
    :param name: 图片名
    :param size: 图片大小
    :return:
    """
    image_name = fr'./results/{name}.png'
    caption = f"⏱️总共耗时: {wtime}s"
    try:
        if name == '' or name is None:
            await app.edit_message_text(chat_id, botmsg_id, "⚠️生成图片失败,可能原因: 节点过多/网络不稳定")
            # await back_message.edit_text("⚠️生成图片失败,可能原因: 节点过多/网络不稳定")
        else:
            x, y = size if size is not None else (0, 0)
            if x > 0 and y > 0:
                if x < 2500 and y < 3500:
                    await app.send_chat_action(chat_id, ChatAction.UPLOAD_PHOTO)
                    await app.send_photo(chat_id, image_name, caption=f"⏱️总共耗时: {wtime}s",
                                         reply_to_message_id=msg_id)
                    # await message.reply_photo(fr'./results/{name}.png', caption=f"⏱️总共耗时: {wtime}s")
                else:
                    await app.send_chat_action(chat_id, ChatAction.UPLOAD_DOCUMENT)
                    await app.send_document(chat_id, image_name, caption=caption, reply_to_message_id=msg_id)
                    # await message.reply_document(fr"./results/{name}.png", caption=f"⏱️总共耗时: {wtime}s")
            else:
                await app.send_chat_action(chat_id, ChatAction.UPLOAD_DOCUMENT)
                await app.send_document(chat_id, image_name, caption=caption, reply_to_message_id=msg_id)
                # await message.reply_document(fr"./results/{name}.png", caption=f"⏱️总共耗时: {wtime}s")
            try:
                bot_msg = await app.get_messages(chat_id, botmsg_id)
                await bot_msg.delete()
                msg = await app.get_messages(chat_id, msg_id)
                if not await private_filter(name, name, msg):
                    with contextlib.suppress(MessageDeleteForbidden, AttributeError):
                        await msg.delete()
            except ValueError:
                pass

    except RPCError as r:
        if chat_id:
            await app.send_document(chat_id, image_name, caption=caption)
        logger.error(r)


def check_rtt(rtt, nodenum: int):
    if rtt == 0:
        new_rtt = [0 for _ in range(nodenum)]
        return new_rtt
    else:
        return rtt


def checkIPv4(ip):
    """
    检查合法v4地址，注意，该函数时间开销很大，谨慎使用
    :param ip:
    :return:
    """
    r = re.compile(r"\b((?:25[0-5]|2[0-4]\d|[01]?\d\d?)(?:(?<!\.)\b|\.)){4}")
    _ip = r.match(ip)
    if _ip:
        if _ip.group(0) == ip:
            return True
    return False
