#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: www
@Date: 2024/6/26 下午2:09
@Description: 
"""
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import List

from utils.types.config import DEFAULT_PING_ADDRESS, DEFAULT_SPEEDFILE, MiaoSpeedOption


class ScriptType(Enum):
    STypeMedia: str = "media"
    STypeIP: str = "ip"


class SSLType(Enum):
    NONE: int = 0
    SECURE: int = 1
    SELF_SIGNED: int = 2


@dataclass
class Script:
    ID: str
    Type: str = ScriptType.STypeMedia
    Content: str = ""
    TimeoutMillis: int = 0


@dataclass
class SlaveRequestConfigs:
    STUNURL: str = 'udp://stunserver.stunprotocol.org:3478'
    DownloadURL: str = DEFAULT_SPEEDFILE
    DownloadDuration: int = 8
    DownloadThreading: int = 4
    PingAverageOver: int = 3
    PingAddress: str = DEFAULT_PING_ADDRESS
    TaskRetry: int = 3
    DNSServers: list = field(default_factory=lambda: [])
    TaskTimeout: int = 2500
    Scripts: List[Script] = field(default_factory=lambda: [])

    @staticmethod
    def from_option(slave_option: MiaoSpeedOption) -> "SlaveRequestConfigs":
        srcfg = SlaveRequestConfigs()
        if not isinstance(slave_option, MiaoSpeedOption):
            return srcfg
        srcfg.DownloadURL = slave_option.downloadURL
        srcfg.STUNURL = slave_option.stunURL
        srcfg.DownloadDuration = slave_option.downloadDuration
        srcfg.DownloadThreading = slave_option.downloadThreading
        srcfg.PingAverageOver = slave_option.pingAverageOver
        srcfg.PingAddress = slave_option.pingAddress
        srcfg.TaskRetry = slave_option.taskRetry
        return srcfg


@dataclass
class SlaveRequestBasics:
    ID: str
    Slave: str
    SlaveName: str
    Invoker: str
    Version: str


class SlaveRequestMatrixType(Enum):
    SPEED_AVERAGE = "SPEED_AVERAGE"
    SPEED_MAX = "SPEED_MAX"
    SPEED_PER_SECOND = "SPEED_PER_SECOND"
    UDP_TYPE = "UDP_TYPE"
    GEOIP_INBOUND = "GEOIP_INBOUND"
    GEOIP_OUTBOUND = "GEOIP_OUTBOUND"
    TEST_SCRIPT = "TEST_SCRIPT"
    TEST_PING_CONN = "TEST_PING_CONN"
    TEST_PING_RTT = "TEST_PING_RTT"
    INVALID = "INVALID"


class VendorType(Enum):
    VendorLocal: str = "Local"
    VendorClash: str = "Clash"
    VendorInvalid: str = "Invalid"


@dataclass
class SlaveRequestMatrixEntry:
    Type: SlaveRequestMatrixType
    Params: str  # 这个值的作用是配合Script.ID 的，设置为一致即可


@dataclass
class SlaveRequestOptions:
    Filter: str = ""
    Matrices: List[SlaveRequestMatrixEntry] = field(default_factory=lambda: [])


@dataclass
class SlaveRequestNode:
    Name: str
    Payload: str


@dataclass
class SlaveRequest:
    Basics: SlaveRequestBasics = field(default_factory=lambda: SlaveRequestBasics(
        ID="114514",
        Slave="114514miaospeed",
        SlaveName="slave1",
        Invoker="114514",
        Version="1.0"
    ))
    Options: SlaveRequestOptions = field(default_factory=lambda: SlaveRequestOptions())
    Configs: SlaveRequestConfigs = field(default_factory=lambda: SlaveRequestConfigs())
    Vendor: VendorType = VendorType.VendorClash
    Nodes: List[SlaveRequestNode] = field(default_factory=lambda: [])
    RandomSequence: str = ""
    Challenge: str = ""

    def to_json(self):
        json_str = json.dumps(self, default=lambda o: o.value if isinstance(o, Enum) else o.__dict__,
                              ensure_ascii=False, separators=(',', ':'))
        json_str = json_str.replace('<', r'\u003c').replace('>', r'\u003e').replace('&', r'\u0026')
        return json_str
