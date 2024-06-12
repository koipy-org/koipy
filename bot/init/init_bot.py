import sys
from sqlite3 import OperationalError

from loguru import logger
from pyrogram import idle

from bot.init.loader import loader
from bot.init.init import app


def bot_info(_app):
    bot_me = _app.get_me()
    logger.info(f'>> Bot ID: {bot_me.id} Username: @{bot_me.username}')
    logger.info('>> Bot is running......')


def main():
    try:
        app.start()
        loader(app)
        bot_info(app)
        idle()
        app.stop()
    except OperationalError as err:
        if "database is locked" in str(err):
            print(f"Bot的会话数据库已被锁定，这可能是之前启动时出现了错误，"
                  f"尝试删除当前文件夹下的 {app.name}.session 与 {app.name}.session-journal 文件")
            sys.exit()
        else:
            raise
