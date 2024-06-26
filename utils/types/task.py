#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: koipy-org
@Date: 2024/6/17 下午1:05
@Description: 
"""
from dataclasses import dataclass, field
from typing import List
from utils.types.config import RuntimeCFG, SlaveType, KoiConfig
from utils.types.items import *


@dataclass
class Task:
    url: str = ""
    name: str = ""
    creator: int = None
    messageID: int = None
    chatID: int = None
    botMsgID: int = None
    botMsgChatID: int = None

    def ready(self):
        return all([
            self.url != "",
            self.name != "",
            self.creator is not None,
            self.messageID is not None,
            self.chatID is not None
        ])


@dataclass
class SlaveRequest:
    slave: SlaveType = None
    items: List[ItemType] = field(default_factory=list)
    task: Task = field(default_factory=lambda: Task())
    runtime: RuntimeCFG = field(default_factory=lambda: RuntimeCFG())
    proxies: List[dict] = field(default_factory=list)
    _ready: bool = False  # 当所有数据都准备好时， 将其设置为 True
    error: str = None

    def ready(self) -> bool:
        if self.slave is None or not self.items or not self.task.ready():
            self._ready = False
            return False
        self._ready = True
        return True

    def merge_items(self, items_list: List[str], cfg: KoiConfig):
        if not isinstance(items_list, list):
            return
        for i_str in items_list:
            if i_str == "TEST_PING_RTT":
                self.items.append(TCPTest())
            elif i_str == "TEST_PING_CONN":
                self.items.append(HTTPTest())
            elif i_str == "SPEED_AVERAGE":
                self.items.append(AvgSpeed())
            elif i_str == "SPEED_MAX":
                self.items.append(MaxSpeed())
            elif i_str == "SPEED_PER_SECOND":
                self.items.append(PerSecond())
            elif i_str == "UDP_TYPE":
                self.items.append(UDPType())
            else:
                sptitem = ScriptItem().from_str(i_str, cfg)
                if isinstance(sptitem.script, Script):
                    self.items.append(sptitem)
        if self.items:
            self.items = sorted(self.items, key=lambda x: x.script.rank)
