#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: koipy-org
@Date: 2024/6/17 上午11:21
@Description: 
"""


class Api:
    stop: str = "/api/speed/stop"
    slave_page: str = "/api/slave/page/"
    slave_content: str = "/api/getSlaveId"
    keyboard_close: str = "/api/close"
    sort: str = "/api/sort/"
    script: str = "/api/script/"
    script_page: str = "/api/script/page/"
    script_ok: str = "/api/script?action=ok"
    select_ok: str = "/api/ok"
    reverse: str = "/api/button/reverse"
    nyd: str = "/api/button/nyd"
    cancel: str = "/api/cancel"
    alive: str = "/api/alive"
    okpage: str = "/api/script?action=okpage"
    all: str = "/api/script?action=fulltest"
    sort_origin: str = "/api/sort/origin"
    sort_http: str = "/api/sort/http"
    sort_rhttp: str = "/api/sort/rhttp"
    sort_aspeed: str = "/api/sort/aspeed"
    sort_arspeed: str = "/api/sort/arspeed"
    sort_mspeed: str = "/api/sort/mspeed"
    sort_mrspeed: str = "/api/sort/mrspeed"
    back: str = "/api/back"
    cfg_del: str = "/api/config/del"
    cfg_new: str = "/api/config/new"
    cfg_edit: str = "/api/config/edit"
    change_status: str = "/api/changeStatus"
    close: str = "/api/close"
    speed_stop: str = "/api/speed?action=stop"
