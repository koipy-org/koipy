import os
import sys

from loguru import logger
from pyrogram.errors import RPCError
from pyrogram.types import Message

from bot.config import lang


async def restart(_, message: Message, kill=False):
    try:
        if kill:
            await message.reply(lang.bye)
            os.kill(os.getpid(), 2)
        else:
            await message.reply(lang.reboot2)
            compiled = getattr(restart, "__compiled__", None)  # 是否处于编译状态
            if compiled:
                filename = sys.argv[0]
                os.execlp(filename, filename)
            else:
                os.execlp(sys.executable, "main.py", *sys.argv)
            sys.exit()
    except RPCError as r:
        logger.error(str(r))


async def killme(app, message: Message):
    await restart(app, message, kill=True)
