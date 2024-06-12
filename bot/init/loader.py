from pyrogram import Client, filters

from bot.impl.born import born
from bot.impl.power import killme, restart
from bot.impl.info import version, info
from bot.impl import helps
from bot.config import CONFIG
from bot.myfilters.filter import admin_filter


class GroupNum:
    Tourist: int = 0
    User: int = 1
    Admin: int = 2


def loader(app: Client):
    # update_notify(app)
    born(app, CONFIG.admin)
    command_loader(app)
    # command_loader2(app)
    # callback_loader(app)
    pass


def command_loader(app: "Client"):
    @app.on_message(filters.command(['help']), group=GroupNum.Tourist)
    async def _(client, message):
        await helps(client, message)

    @app.on_message(filters.command(['version']), group=GroupNum.Tourist)
    async def _(client, message):
        await version(client, message)

    @app.on_message(filters.command(['killme']) & admin_filter(), group=GroupNum.Admin)
    async def _(client, message):
        await killme(client, message)

    @app.on_message(filters.command(['restart', 'reboot']) & admin_filter(), group=GroupNum.Admin)
    async def _(client, message):
        await restart(client, message)

    @app.on_message(filters.command(['system']) & admin_filter(), group=GroupNum.Admin)
    async def _(client, message):
        await info(client, message)
