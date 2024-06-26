from pyrogram import Client
from pyrogram.types import CallbackQuery


from bot.impl.command.born import born
from bot.impl.command.power import killme, restart
from bot.impl.command.info import version, info
from bot.impl.command.help import helps
from bot.impl.command.test import task_handler

from bot.myfilters.filters import admin_filter, command, callback_master, prefix_filter, call_data_filter
from bot.impl.query import keyboard, selector
from bot.api import Api
from bot.config import CONFIG, lang


class GroupNum:
    Tourist: int = 0
    User: int = 1
    Admin: int = 2
    Max: int = 999


def loader(app: Client):
    # update_notify(app)
    born(app, CONFIG.admin)
    command_loader(app)
    # command_loader2(app)
    callback_query_loader(app)


def command_loader(app: "Client"):
    @app.on_message(command(['help']), group=GroupNum.Tourist)
    async def _(client, message):
        await helps(client, message)

    @app.on_message(command(['version']), group=GroupNum.Tourist)
    async def _(client, message):
        await version(client, message)

    @app.on_message(command(['killme']) & admin_filter(), group=GroupNum.Admin)
    async def _(client, message):
        await killme(client, message)

    @app.on_message(command(['restart', 'reboot']) & admin_filter(), group=GroupNum.Admin)
    async def _(client, message):
        await restart(client, message)

    @app.on_message(command(['system']) & admin_filter(), group=GroupNum.Admin)
    async def _(client, message):
        await info(client, message)

    @app.on_message(command(["test"]) & admin_filter(), group=GroupNum.User)
    async def _(client, message):
        await task_handler(client, message)


def callback_query_loader(app: "Client"):
    @app.on_callback_query(prefix_filter(Api.script) & callback_master(CONFIG.user), group=GroupNum.User)
    async def _(client, call):
        await keyboard.editkeybord_yes_or_no(client, call)

    @app.on_callback_query(call_data_filter(Api.okpage) & callback_master(CONFIG.user), group=GroupNum.User)
    async def _(client, call):
        await keyboard.select_page_ok(client, call)

    @app.on_callback_query(call_data_filter(Api.reverse) & callback_master(CONFIG.user), group=GroupNum.User)
    async def _(client, call):
        await keyboard.editkeybord_reverse(client, call)

    @app.on_callback_query(call_data_filter(Api.close) & callback_master(CONFIG.user), group=GroupNum.User)
    async def _(client, call: CallbackQuery):
        await keyboard.close(client, call)

    @app.on_callback_query(prefix_filter(selector.SortSelector.content_api) & callback_master(CONFIG.user),
                           group=GroupNum.User)
    async def _(client, call: CallbackQuery):
        await selector.SortSelector.accept(client, call)

    #
    @app.on_callback_query(prefix_filter(selector.SlaveSelector.content_api) & callback_master(CONFIG.user),
                           group=GroupNum.User)
    async def _(client, call: CallbackQuery):
        await selector.SlaveSelector.accept(client, call)

    @app.on_callback_query(call_data_filter(Api.script_ok) & callback_master(CONFIG.user), group=GroupNum.User)
    async def _(client, call: CallbackQuery):
        await selector.ScriptSelector.accept(client, call)

    @app.on_callback_query(call_data_filter(Api.all) & callback_master(CONFIG.user), group=GroupNum.User)
    async def _(client, call: CallbackQuery):
        await keyboard.test_all(client, call)
