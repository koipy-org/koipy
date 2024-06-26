#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: www
@Date: 2024/6/25 下午5:29
@Description: 
"""
from dataclasses import dataclass, field
from typing import TypeVar

from utils.types.config import Script, DictCFG, KoiConfig, ScriptType


@dataclass
class BaseItem(DictCFG):
    name: str = "BASE"
    script: Script = None


ItemType = TypeVar('ItemType', bound='BaseItem')


@dataclass
class ScriptItem(BaseItem):
    name: str = "TEST_SCRIPT"
    script: Script = None

    def from_str(self, itemstr: str, koicfg: KoiConfig) -> "ScriptItem":
        for script in koicfg.scriptConfig.scripts:
            if script.name == itemstr:
                self.script = script
        return self


@dataclass
class SpeedItem(BaseItem):
    name: str = "SPEED"
    script: Script = None


@dataclass
class AvgSpeed(SpeedItem):
    name: str = "SPEED_AVERAGE"
    script: Script = field(default_factory=lambda: Script(type=ScriptType.GoBuiltin, name="SPEED_AVERAGE", rank=998))


@dataclass
class MaxSpeed(BaseItem):
    name: str = "SPEED_MAX"
    script: Script = field(default_factory=lambda: Script(type=ScriptType.GoBuiltin, name="SPEED_MAX", rank=999))


@dataclass
class PerSecond(BaseItem):
    name: str = "SPEED_PER_SECOND"
    script: Script = field(default_factory=lambda: Script(type=ScriptType.GoBuiltin, name="SPEED_PER_SECOND", rank=1000))


@dataclass
class HTTPTest(BaseItem):
    name: str = "TEST_PING_CONN"
    script: Script = field(default_factory=lambda: Script(type=ScriptType.GoBuiltin, name="TEST_PING_CONN", rank=-1))


@dataclass
class TCPTest(BaseItem):
    name: str = "TEST_PING_RTT"
    script: Script = field(default_factory=lambda: Script(type=ScriptType.GoBuiltin, name="TEST_PING_RTT", rank=-2))


@dataclass
class UDPType(BaseItem):
    name: str = "UDP_TYPE"
    script: Script = field(default_factory=lambda: Script(type=ScriptType.GoBuiltin, name="UDP_TYPE", rank=997))
