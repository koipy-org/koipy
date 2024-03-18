"""配置反序列化后得到的类，参数意义请参阅 ./resources/config.yaml.example"""
import json

from collections import OrderedDict
from dataclasses import field, dataclass, asdict, fields
from enum import Enum
from os import PathLike
from pathlib import Path
from typing import List, Any, Dict, TypeAlias, Union

import yaml
from yaml import SafeDumper

try:
    from loguru import logger
except ImportError:
    logger = None
from utils.types.base import DictCFG, BaseCFG
from utils.types.exception import ConfigTypeError, ConfigError

Admin: TypeAlias = Union[str, int]
User: TypeAlias = Union[str, int]
DEFAULT_SPEEDFILE: str = "https://dl.google.com/dl/android/studio/install/3.4.1.0/" \
                         "android-studio-ide-183.5522156-windows.exe"
DEFAULT_PING_ADDRESS: str = "https://cp.cloudflare.com/generate_204"
DEFAULT_FONT_PATH: str = str(Path("./resources/alibaba-Regular.ttf").absolute())


class OrderedSafeDumper(SafeDumper):
    pass


OrderedSafeDumper.add_representer(OrderedDict, lambda self, data: self.represent_dict(data.items()))


@dataclass
class CoreCFG(DictCFG):
    vendor: str = None
    path: str = None

    def from_obj(self, obj: dict) -> "DictCFG":
        if not isinstance(obj, dict):
            return self
        if "vendor" in obj:
            a = obj.pop("vendor")


@dataclass
class ClashCFG(CoreCFG):
    vendor: str = "clash"
    allowCaching: bool = False
    branch: str = "origin"


@dataclass
class Mihomo(ClashCFG):
    vendor: str = "clash"
    branch: str = "meta"


@dataclass
class FullTCore(CoreCFG):
    vendor: str = "fulltcore"


@dataclass
class SubConverterCFG(DictCFG):
    enable: bool = False
    address: str = "127.0.0.1:25500"
    tls: bool = False
    remoteconfig: str = None


@dataclass
class BotCFG(DictCFG):
    api_id: int = None
    api_hash: str = None
    bot_token: str = None
    proxy: str = None
    strictmode: bool = False
    scripttext: str = "⏳连通性测试进行中..."
    analyzetext: str = "⏳节点测试拓扑进行中..."
    speedtext: str = "⏳速度测试进行中..."
    bar: str = "="
    bleft: str = "["
    bright: str = "]"
    bspace: str = "  "
    command: list[str] = field(default_factory=list)

    def from_obj(self, obj: dict) -> "BotCFG":
        if "command" in obj:
            raw_v = obj.pop("command")
            if isinstance(raw_v, list):
                self.command = raw_v
        super().from_obj(obj)
        return self


@dataclass
class RuntimeCFG(DictCFG):
    pingurl: str = "https://www.gstatic.com/generate_204"
    speedfile: List[str] = field(default_factory=lambda: [DEFAULT_SPEEDFILE])
    speednodes: int = 300
    speedthread: int = 4
    nospeed: bool = False
    ipstack: bool = False
    localip: bool = False
    dasn: str = None
    dorg: str = None
    dcity: str = None
    interval: int = 10
    entrance: str = "ip"

    def from_obj(self, obj: dict) -> "RuntimeCFG":
        if "speedfile" in obj:
            raw_v = obj.pop("speedfile")
            if isinstance(raw_v, list):
                self.speedfile = raw_v
            elif isinstance(raw_v, str):
                self.speedfile = [raw_v]
        else:
            super().from_obj(obj)
        return self


@dataclass
class Color(DictCFG):
    label: int = 0
    name: str = ""
    value: str = "#ffffff"
    alpha: int = 255
    end_color: str = "#ffffff"


@dataclass
class BackGroundColor(DictCFG):
    """
    背景图颜色配置
    """
    script: Color = Color()
    inbound: Color = Color()
    outbound: Color = Color()
    speed: Color = Color()
    speedTitle: Color = Color(value="#EAEAEA")
    scriptTitle: Color = Color(value="#EAEAEA")
    topoTitle: Color = Color(value="#EAEAEA")


@dataclass
class ColorCFG(DictCFG):
    speed: List[Color] = field(default_factory=list)
    delay: List[Color] = field(default_factory=list)
    outColor: List[Color] = field(default_factory=list)
    yes: Color = Color(value="#bee47e", end_color="#bee47e")
    no: Color = Color(value="#ee6b73", end_color="#ee6b73")
    na: Color = Color(value="#8d8b8e", end_color="#8d8b8e")
    wait: Color = Color(value="#dcc7e1", end_color="#dcc7e1")
    ipriskLow: Color = Color()
    ipriskMedium: Color = Color()
    ipriskHigh: Color = Color()
    ipriskVeryHigh: Color = Color()
    warn: Color = Color(value="#fcc43c", end_color="#fcc43c")
    background: "BackGroundColor" = BackGroundColor()

    def from_obj(self, obj: dict) -> "ColorCFG":
        def _temp(key: str, instance: BaseCFG):
            if key in obj:
                _raw_v = obj.pop(key)
                if isinstance(_raw_v, list):
                    self.from_list(key, _raw_v, instance)

        for k in ["speed", 'delay', 'outColor']:
            _temp(k, Color())

        super().from_obj(obj)
        return self


@dataclass
class WMCFG(DictCFG):
    """
    水印配置
    """
    enable: bool = False
    text: str = "只是一个水印"
    color: Color = Color(value="#000000", alpha=16)
    alpha: int = color.alpha
    size: int = 64
    angle: Union[float, int] = -16.0
    row_spacing: int = 1
    start_y: int = 0
    shadow: bool = False
    trace: bool = False

    def from_obj(self, obj: dict) -> "WMCFG":
        _temp = obj.pop('angle', None)
        if isinstance(_temp, (float, int)):
            self.angle = _temp
        super().from_obj(obj)
        return self


@dataclass
class ImageCFG(DictCFG):
    title: str = "FullTclash"
    font: str = DEFAULT_FONT_PATH
    speedEndColorSwitch: bool = False
    endColorsSwitch: bool = False
    compress: bool = False
    color: ColorCFG = ColorCFG()
    watermark: WMCFG = WMCFG()
    nonCommercialWatermark: WMCFG = WMCFG(text="请勿用于商业用途")


@dataclass
class EmojiCFG(DictCFG):
    enable: bool = True
    source: str = "TwemojiLocalSource"


@dataclass
class SlaveOption(DictCFG):
    pass


@dataclass
class MiaoSpeedOption(DictCFG):
    downloadDuration: int = 8
    downloadThreading: int = 4
    pingAverageOver: int = 3
    taskRetry: int = 3
    downloadURL: str = DEFAULT_SPEEDFILE
    pingAddress: str = DEFAULT_PING_ADDRESS
    stunURL: str = "udp://stun.ideasip.com:3478"


@dataclass
class Slave(DictCFG):
    id: Union[str, int] = None
    comment: str = ""
    hidden: bool = False
    token: str = None
    type: str = None
    address: str = None
    option: SlaveOption = SlaveOption()


DEFAULT_SLAVE: Slave = Slave("default-slave", "本地后端")


@dataclass
class BotSlave(Slave):
    type: str = "bot"
    username: str = None


@dataclass
class LocalSlave(Slave):
    id: str = "default"
    type: str = None
    username: str = "local"


@dataclass
class AiohttpWSSlave(Slave):
    type: str = "websocket"
    path: str = "/"


@dataclass
class MiaoSpeedSlave(Slave):
    type: str = "miaospeed"
    skip_cert_verify: bool = True
    tls: bool = True
    invoker: str = None
    branch: str = "fulltclash"
    buildtoken: str = None
    option: MiaoSpeedOption = MiaoSpeedOption()


@dataclass
class SubInfoCFG(DictCFG):
    owner: int = None
    password: str = None
    url: str = None
    share: List[int] = field(default_factory=list)

    def from_obj(self, obj: dict) -> "SubInfoCFG":
        if "share" in obj:
            raw_v = obj.pop("share")
            self.share = [i for i in raw_v if isinstance(i, int)]
        super().from_obj(obj)
        return self


@dataclass
class UserbotCFG(DictCFG):
    enable: bool = False
    uid: int = None
    whitelist: List[int] = field(default_factory=list)

    def from_obj(self, obj: dict) -> "UserbotCFG":
        if "whitelist" in obj:
            raw_v = obj.pop("whitelist")
            self.whitelist = [i for i in raw_v if isinstance(i, int)]
        super().from_obj(obj)
        return self


class ScriptType:
    PYTHON: int = 0
    GOJA_JS: int = 1


class SortType:
    ORIGIN: str = "订阅原序"
    HTTP: str = "HTTP升序"
    HTTP_R: str = "HTTP降序"  # http降序
    AVERAGE_SPEED: str = "平均速度升序"
    AVERAGE_SPEED_R: str = "平均速度降序"  # 平均速度降序
    MAX_SPEED: str = "最大速度升序"
    MAX_SPEED_R: str = "最大速度降序"  # 最大速度降序


@dataclass
class Script(DictCFG):
    type: str = ScriptType.PYTHON


@dataclass
class Rule(DictCFG):
    name: str = ""
    enable: bool = False
    script: List[Script] = field(default_factory=list)
    slaveid: str = "local"
    sort: str = SortType.ORIGIN


@dataclass
class KoiConfig(DictCFG):
    admin: List[Admin] = field(default_factory=list)
    user: List[User] = field(default_factory=list)
    bot: BotCFG = BotCFG()
    core: ClashCFG = ClashCFG()
    socks5Proxy: str = None
    httpProxy: str = None
    anti_group: bool = False
    subconverter: SubConverterCFG = SubConverterCFG()
    geoipAPI: str = "ip-api.com"
    geoipKey: str = None
    runtime: RuntimeCFG = RuntimeCFG()
    buildtoken: str = "c7004ded9db897e538405c67e50e0ef0c3dbad717e67a92d02f6ebcfd1022a5ad1d2c4419541f538ff623051759" \
                      "ec000d2f426e03f9709a6608570c5b9141a6b"
    rule: Dict[str, Rule] = field(default_factory=dict)
    slaveConfig: Dict[str, Slave] = field(default_factory=lambda: {DEFAULT_SLAVE.id: DEFAULT_SLAVE})
    userConfig: Dict[str, Any] = field(default_factory=lambda: {"rule": {}, "usage-ranking": {}})
    subinfo: Dict[str, SubInfoCFG] = field(default_factory=dict)
    userbot: UserbotCFG = UserbotCFG()
    image: ImageCFG = ImageCFG()

    def from_slaveConfig(self, obj: dict) -> "KoiConfig":
        self.slaveConfig = {}
        for k, v in obj.items():
            s_type = v.get('type', None)
            if isinstance(s_type, str) or k == "default":
                if s_type == AiohttpWSSlave.type:
                    a_slave = AiohttpWSSlave()
                elif s_type == MiaoSpeedSlave.type:
                    a_slave = MiaoSpeedSlave()
                elif s_type == BotSlave.type:
                    a_slave = BotSlave()
                elif s_type == LocalSlave.type and k == "default":
                    a_slave = LocalSlave()
                else:
                    a_slave = Slave()
                a_slave.from_obj(v)
                self.slaveConfig[k] = a_slave
        return self

    def from_obj(self, obj: dict) -> "KoiConfig":
        if not isinstance(obj, dict):
            return self

        def padding_admin_user(key: str):
            _t_l = []
            if key in obj:
                _t_raw_v_ = obj.pop(key)
                if isinstance(_t_raw_v_, list):
                    for _t_v in _t_raw_v_:
                        if isinstance(_t_v, (str, int)):
                            _t_l.append(_t_v)
                    setattr(self, key, _t_l)

        if "admin" in obj:
            padding_admin_user("admin")
        if "user" in obj:
            padding_admin_user("user")
        if "rule" in obj:
            _raw_v = obj.pop("rule")
            if isinstance(_raw_v, dict):
                self.from_dict("rule", _raw_v, Rule())
        if "slaveConfig" in obj:
            _raw_v = obj.pop("slaveConfig")
            if isinstance(_raw_v, dict):
                self.from_slaveConfig(_raw_v)
        if "userConfig" in obj:
            _raw_v = obj.pop("userConfig")
            if isinstance(_raw_v, dict):
                self.from_obj(_raw_v)
        if "subinfo" in obj:
            _raw_v = obj.pop("subinfo")
            if isinstance(_raw_v, dict):
                self.from_dict("subinfo", _raw_v, SubInfoCFG())
        super().from_obj(obj)
        return self

    def with_logger(self, cfg: Any) -> None:
        try:
            if logger is None:
                self.from_obj(cfg)
            else:
                logger.catch()(self.from_obj)(cfg)
        except TypeError as e:
            raise ConfigTypeError from e
        except Exception as e:
            raise ConfigError from e

    def from_file(self, path: str | bytes | PathLike) -> None:
        with open(path, 'r', encoding='utf-8') as __fp:
            rawcfg: dict = yaml.safe_load(__fp)
        self.with_logger(rawcfg)

    def from_yaml(self, yaml_str: str | bytes) -> None:
        """
        从yaml格式化字符串反序列化然后填充配置
        """
        import io
        yaml_str = yaml_str.encode() if isinstance(yaml_str, str) else yaml_str if isinstance(yaml_str, bytes) else ""
        io_instance = io.BytesIO(yaml_str)
        rawcfg: dict = yaml.safe_load(io_instance)
        self.with_logger(rawcfg)

    def to_json(self) -> str:
        json_str = json.dumps(self, default=lambda o: o.value if isinstance(o, Enum) else o.__dict__,
                              ensure_ascii=True, separators=(',', ':'))
        return json_str

    def to_yaml(self, stream=None) -> bytes:
        """
        返回此对象的序列化字符串，如果提供IO流，则将输出重定向至给定的流，此时将返回 None
        """
        dictobj = asdict(self, dict_factory=OrderedDict)
        dictobj = self.rename_to_yaml(dictobj)
        yaml_str: bytes = yaml.dump(dictobj, stream, Dumper=OrderedSafeDumper, encoding="utf-8", allow_unicode=True)
        return yaml_str


def test():
    _ftcfg = KoiConfig()
    _ftcfg.from_yaml("admin: [11111, 2222]")
    print(_ftcfg.admin)
    for f in fields(_ftcfg):
        print(f.name, f.type)

    _ftcfg = _ftcfg.from_obj("111")
    print(_ftcfg)


if __name__ == "__main__":
    import time

    t1 = time.time()
    test()
    # ftcfg = KoiConfig()
    # ftcfg.from_file("ftconfig.yml")
    # print(ftcfg.bot)
    # with open("ftconfig3.yml", 'wb') as _fp:
    #     ftcfg.to_yaml(_fp)

    print("耗时: ", time.time() - t1)
