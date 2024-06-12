import asyncio

from loguru import logger
from pyrogram import filters, Client
from pyrogram.types import Message

from bot.config import CONFIG, lang, CONFIG_PATH
from bot.impl import restart
from utils.types import Admin

_Lock = asyncio.Lock()


def born(app: "Client", admin: Admin):
    if not bool(admin):
        from pyrogram.handlers import MessageHandler
        # 如果admin列表为空，说明没有配置管理员或者初次启动，第一个给bot发私聊消息的将是管理员。
        # 这是来自小说的灵感，蛋生生物睁开第一眼看到的第一个目标是它的母亲。
        logger.warning(lang.born_1)

        async def waiting_born(client: "Client", message: "Message"):
            async with _Lock:
                admin_id = message.from_user.id
                await message.reply(f"{lang.born_2}\n"
                                    f"{lang.uid}: {admin_id}\n"
                                    f"{lang.username}: {message.from_user.username}")
                # 管理员身份添加到配置文件
                if admin_id:
                    CONFIG.admin.append(message.from_user.id)
                    CONFIG.reload(CONFIG_PATH)
                # 删除此handler回调，否则会将所有人注册成管理员
                if -100 in app.dispatcher.groups:
                    _g: list = app.dispatcher.groups[-100]
                    self_h = None
                    for _h in _g:
                        if isinstance(_h, MessageHandler) and "waiting_born" == _h.callback.__name__:
                            self_h = _h
                            break
                    if self_h is not None:
                        app.remove_handler(self_h, -100)
                logger.info(f"{lang.born_4}\n{lang.uid}:{admin_id}\n{lang.username}:{message.from_user.username}\n\n"
                            f"{lang.reboot}")
                await restart(client, message)

        hl = MessageHandler(waiting_born, filters.private)
        app.add_handler(hl, -100)
    else:
        return
