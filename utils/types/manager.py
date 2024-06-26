import copy
import json
import io
from collections import OrderedDict
from dataclasses import fields
from enum import Enum
from io import StringIO
from os import PathLike
from pprint import pprint
from threading import Lock
from typing import Any, Union, TextIO

import yaml
from yaml import SafeDumper

from utils.types import ConfigTypeError, ConfigError, BaseCFG, ListCFG

try:
    from loguru import logger
except ImportError:
    logger = None

_CONFIG_LOCK = Lock()


class OrderedSafeDumper(SafeDumper):
    pass


class NoUnderScoresDict(OrderedDict):
    def __init__(self, *args, **kwargs):
        super(NoUnderScoresDict, self).__init__(*args, **kwargs)

    def __setitem__(self, key, value=None):
        if isinstance(key, str) and key.startswith('_'):
            return
        OrderedDict.__setitem__(self, key, value)


OrderedSafeDumper.add_representer(NoUnderScoresDict, lambda self, data: self.represent_dict(data.items()))


class ConfigManager(BaseCFG):
    _raw_config: dict = None

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

    def from_file(self, path: Union[str, bytes, PathLike]) -> "Any":
        try:
            with open(path, 'r', encoding='utf-8') as __fp:
                rawcfg: dict = yaml.safe_load(__fp)
            rawcfg2 = copy.deepcopy(rawcfg)
            self._raw_config = rawcfg2
            self.with_logger(rawcfg)
        except Exception as e:
            logger.error(str(e))
        finally:
            return self

    def from_yaml(self, yaml_str: Union[str, bytes]) -> "Any":
        """
        从yaml格式化字符串反序列化然后填充配置
        """
        yaml_str = yaml_str.encode() if isinstance(yaml_str, str) else yaml_str if isinstance(yaml_str, bytes) else ""
        io_instance = io.BytesIO(yaml_str)
        rawcfg: dict = yaml.safe_load(io_instance)
        self._raw_config = rawcfg
        self.with_logger(rawcfg)
        return self

    def to_dict(self, retain_raw: bool = False):
        """
        把所有数据转换成python原生类型
        :param retain_raw: 保留原始配置
        :return:
        """
        dictobj = asdict(self, dict_factory=NoUnderScoresDict)
        try:
            if retain_raw:
                diff_key = set(self._raw_config.keys()) - set(dictobj.keys())
                for d in diff_key:
                    dictobj[d] = self._raw_config[d]
        except Exception as e:
            logger.error(str(e))
        return dictobj

    def to_json(self, stream: TextIO = None, retain_raw: bool = True) -> str:
        dictobj = self.to_dict(retain_raw=retain_raw)
        dictobj = self.rename_to_yaml(dictobj)
        json_str = ""
        if stream is not None:
            try:
                json.dump(dictobj, stream, default=lambda o: o.value if isinstance(o, Enum) else o.__dict__,
                          ensure_ascii=True, separators=(',', ':'))
            except IOError as e:
                logger.error(str(e))
            finally:
                json_str = ""

        return json_str

    def to_yaml(self, stream=None, retain_raw: bool = True) -> bytes:
        """
        返回此对象的序列化字符串，如果提供IO流，则将输出重定向至给定的流，此时将返回 None
        """
        dictobj = self.to_dict(retain_raw=retain_raw)
        dictobj = self.rename_to_yaml(dictobj)
        yaml_str: bytes = yaml.dump(dictobj, stream,
                                    Dumper=OrderedSafeDumper, encoding="utf-8", allow_unicode=True)
        return yaml_str

    def save(self, save_path: str, _format: str = "yaml"):
        with _CONFIG_LOCK, open(save_path, "w+", encoding="utf-8") as fp:
            try:
                if _format == "yaml":
                    self.to_yaml(fp)
                elif _format == "json":
                    self.to_json(fp)
                return True
            except Exception as e:
                logger.error(e)
                return False

    @logger.catch
    def reload(self, path: str, issave=True):
        if issave:
            status = self.save(save_path=path)
            if status is False:
                logger.warning("重载配置的过程中未能保存先前配置")
        try:
            logger.info("执行配置重载操作......")
            self.from_file(path)
            logger.info("重载配置成功")
            return True
        except Exception as e:
            logger.error(e)
            return False

    def __str__(self):
        print_io = StringIO()
        pprint(self)
        # print_io.read(-1)
        return print_io.getvalue()

    def __repr__(self):
        return self.__str__()


def asdict(obj, *, dict_factory=dict):
    """Return the fields of a dataclass instance as a new dictionary mapping
    field names to field values.

    Example usage::

      @dataclass
      class C:
          x: int
          y: int

      c = C(1, 2)
      assert asdict(c) == {'x': 1, 'y': 2}

    If given, 'dict_factory' will be used instead of built-in dict.
    The function applies recursively to field values that are
    dataclass instances. This will also look into built-in containers:
    tuples, lists, and dicts.
    """
    if not hasattr(type(obj), '__dataclass_fields__'):
        raise TypeError("asdict() should be called on dataclass instances")
    return _asdict_inner(obj, dict_factory)


def _asdict_inner(obj: Any, dict_factory):
    if hasattr(type(obj), '__dataclass_fields__') and not isinstance(obj, ListCFG):
        result = []
        for f in fields(obj):
            value = _asdict_inner(getattr(obj, f.name), dict_factory)
            result.append((f.name, value))
        return dict_factory(result)
    elif isinstance(obj, (ListCFG, list)):
        return list(_asdict_inner(v, dict_factory) for v in obj)
    elif isinstance(obj, tuple) and hasattr(obj, '_fields'):
        # obj is a namedtuple.  Recurse into it, but the returned
        # object is another namedtuple of the same type.  This is
        # similar to how other list- or tuple-derived classes are
        # treated (see below), but we just need to create them
        # differently because a namedtuple's __init__ needs to be
        # called differently (see bpo-34363).

        # I'm not using namedtuple's _asdict()
        # method, because:
        # - it does not recurse in to the namedtuple fields and
        #   convert them to dicts (using dict_factory).
        # - I don't actually want to return a dict here.  The main
        #   use case here is json.dumps, and it handles converting
        #   namedtuples to lists.  Admittedly we're losing some
        #   information here when we produce a json list instead of a
        #   dict.  Note that if we returned dicts here instead of
        #   namedtuples, we could no longer call asdict() on a data
        #   structure where a namedtuple was used as a dict key.

        return type(obj)(*[_asdict_inner(v, dict_factory) for v in obj])
    elif isinstance(obj, (list, tuple)):
        # Assume we can create an object of this type by passing in a
        # generator (which is not true for namedtuples, handled
        # above).
        return type(obj)(_asdict_inner(v, dict_factory) for v in obj)
    elif isinstance(obj, dict):
        return type(obj)((_asdict_inner(k, dict_factory),
                          _asdict_inner(v, dict_factory))
                         for k, v in obj.items())
    else:
        return copy.deepcopy(obj)
