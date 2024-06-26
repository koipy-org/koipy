#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: koipy-org
@Date: 2024/6/17 下午1:21
@Description: 
"""
import io
import pathlib
from copy import deepcopy
from typing import Union, List
from urllib.parse import urlparse

import yaml
from loguru import logger

try:
    import re2 as re
except ImportError:
    import re

from utils.types.config import SubConverterCFG


class ArgCleaner:
    def __init__(self, string: str = None):
        self.string = string

    @staticmethod
    def getarg(string: str, sep: str = ' ') -> list[str]:
        """
        对字符串使用特定字符进行切片
        Args:
            string: 要切片的字符串
            sep: 指定用来切片的字符依据，默认为空格

        Returns: 返回一个切好的字符串列表

        """
        return [x for x in string.strip().split(sep) if x != ''] if string is not None else []

    def getall(self, string: str = None):
        """
        分割一段字符串中的参数，返回参数列表
        """
        if string is None:
            if self.string is None:
                return None
            arg = self.string.strip().split(' ')
            arg = [x for x in arg if x != '']
            return arg
        else:
            arg = string.strip().split(' ')
            arg = [x for x in arg if x != '']
            return arg


class ClashCleaner:
    """
    yaml配置清洗
    """

    def __init__(self, _config: Union[str, bytes] = None):
        """
        :param _config: 传入一个文件对象，或者一个字符串,文件对象需指向 yaml/yml 后缀文件
        """
        self.unsupport_type = []
        self.yaml = {}
        if _config is not None:
            self.load(_config)
        if not isinstance(self.yaml, dict):
            self.yaml = {}

    @staticmethod
    def notag(_config: bytes):
        """
        去除制表符，yaml反序列化不允许制表符出现在标量以外的地方
        """
        return _config.replace(b'\t', b'  ')

    def load(self, data: Union[str, bytes]):
        is_path = is_valid_path(data) if isinstance(data, str) else False

        try:
            if is_path:
                with open(data, 'r', encoding="UTF-8") as fp:
                    self.yaml = yaml.safe_load(fp)
            else:
                try:
                    if isinstance(data, str):
                        data = data.encode()
                    elif isinstance(data, bytes):
                        stream = io.BytesIO(data)
                        self.yaml = yaml.safe_load(stream)
                except yaml.MarkedYAMLError:
                    _config2 = self.notag(data)
                    stream = io.BytesIO(_config2)
                    self.yaml = yaml.safe_load(stream)

        except Exception as e:
            logger.error(str(e))

    def check_type(self):
        """
        检查反序列化后的对象是否符合clash配置格式
        """
        self.check_unsupport_proxy()

    def set_proxies(self, proxyinfo: list):
        """
        覆写里面的proxies键
        :return:
        """
        self.yaml['proxies'] = proxyinfo

    def check_unsupport_proxy(self):
        try:
            if self.yaml is None:
                self.yaml = {}
                return
            proxies: list = self.yaml['proxies']
            newproxies = []
            for i, proxy in enumerate(proxies):
                if isinstance(proxy, dict):
                    name = proxy['name']
                    ptype = proxy['type']

                    if not isinstance(name, str):
                        # 将节点名称转为字符串
                        proxy['name'] = str(name)
                    if ptype not in self.unsupport_type and len(name) < 128:
                        newproxies.append(proxy)
            self.yaml['proxies'] = newproxies
        except KeyError:
            logger.warning("读取节点信息失败！")
        except TypeError:
            logger.warning("读取节点信息失败！")

    def get_proxies(self):
        """
        获取整个代理信息
        :return: list[dict,dict...]
        """
        try:
            return self.yaml['proxies']
        except KeyError:
            logger.warning("读取节点信息失败！")
            return []
        except TypeError:
            logger.warning("读取节点信息失败！")
            return []

    def nodes_count(self):
        """
        获取节点数量
        :return: int
        """
        try:
            return len(self.yaml['proxies'])
        except TypeError:
            return 0

    def nodes_name(self, _filter: str = ''):
        """
        获取节点名
        :return: list
        """
        lis = []
        try:
            for i in self.yaml['proxies']:
                lis.append(str(i['name']))
            return lis
        except KeyError:
            return None
        except TypeError:
            return None

    def nodes_addr(self):
        """
        获取节点地址信息，返回（host,port）元组形式
        """
        try:
            return [(str(i['server']), i['port']) for i in self.yaml['proxies']]
        except KeyError:
            return None
        except TypeError:
            return None

    def nodes_type(self):
        """
        获取节点类型
        :return: list
        """
        t = []
        try:
            for i in self.yaml['proxies']:
                t.append(str(i['type']))
            return t
        except TypeError:
            logger.warning("读取节点信息失败！")
            return None

    def nodes_host(self, _filter: str = ''):
        """
        获取节点域名
        :return: list
        """
        y = []
        try:
            for i in self.yaml['proxies']:
                y.append(str(i['server']))
            return y
        except TypeError:
            logger.warning("读取节点信息失败！")
            return None

    @staticmethod
    def count_element(y: list = None):
        """
        返回入站域名信息,本质上是统计一个列表里每个元素出现的次数
        :return: dict
        """
        dip = {}
        if y is None:
            return None
        else:
            nodehosts = y
        try:
            for key in nodehosts:
                dip[key] = dip.get(key, 0) + 1
            return dip
        except Exception as e:
            logger.error(str(e))
            return None

    @staticmethod
    def count_elem(addrs: list = None):
        """
        返回入站ip信息,本质上是统计一个列表里每个元素出现的次数
        :return: dict
        """
        dic = {}
        if addrs is None:
            return None
        else:
            nodeaddrs = addrs
        try:
            for key in nodeaddrs:
                dic[key] = dic.get(key, 0) + 1
            return dic
        except Exception as e:
            logger.error(str(e))
            return None

    def node_filter(self, include: str = '', exclude: str = '', issave=False):
        """
        节点过滤
        :param issave: 是否保存过滤结果到文件
        :param include: 包含
        :param exclude: 排除
        :return:
        """
        logger.info(f'Node filter text>> included: {include}, excluded: {exclude}')
        result = []
        result2 = []
        nodelist = self.get_proxies()
        pattern1 = pattern2 = None
        try:
            if include:
                pattern1 = re.compile(include)
            if exclude:
                pattern2 = re.compile(exclude)
        except re.error:
            logger.error("Regular Error. Please check the regular expression!")
            return self.nodes_name()
        except Exception as e:
            logger.error(e)
            return self.nodes_name()
        if pattern1 is None:
            result = nodelist
        else:
            for node in nodelist:
                try:
                    nodename = node.get('name', '')
                    r = pattern1.findall(nodename)
                    if r:
                        logger.info("Include filters that have been matched:" + str(nodename))
                        result.append(node)
                except re.error as rerror:
                    logger.error(str(rerror))
                    result.append(node)
                except Exception as e:
                    logger.error(str(e))
                    result.append(node)
        jishu1 = len(result)
        jishu2 = 0
        if pattern2 is None:
            result2 = result
        else:
            for node in result:
                try:
                    nodename2 = node.get('name', '')
                    r = pattern2.findall(nodename2)
                    if r:
                        logger.info("Exclude filters that have been matched: " + str(nodename2))
                        jishu2 += 1
                    else:
                        result2.append(node)
                except re.error as rerror:
                    logger.error(str(rerror))
                except Exception as e:
                    logger.error(str(e))
        logger.info(f"Included {jishu1} node(s)  Excluded {jishu2} node(s)  Exported {jishu1 - jishu2} node(s)")
        self.yaml['proxies'] = result2
        if issave:
            self.save()

    @logger.catch
    def save(self, save_path: str = "./sub.yaml"):
        with open(save_path, "w", encoding="UTF-8") as fp:
            yaml.safe_dump(self.yaml, fp, encoding='utf-8')


class ResultCleaner:
    """
    测速结果的处理类，负责将得到的数据进行排序，重命名等操作
    """

    def __init__(self, info: dict):
        self.data = info

    @staticmethod
    def get_http_latency(data: list):
        """
        对所有列表延迟取平均，去除0
        :param data:
        :return:
        """
        if not data:
            raise IndexError("列表为空")
        n = len(data)
        m = len(data[0])
        new_list = []

        for j in range(m):
            col_sum = 0
            num = 0
            for i in range(n):
                if data[i][j] != 0:
                    col_sum += data[i][j]
                    num += 1
            if num:
                r1 = int(col_sum / num)
                new_list.append(r1)
            else:
                new_list.append(0)
        return new_list

    def convert_proxy_typename(self):
        if '类型' in self.data:
            new_type = []
            type1: List[str] = self.data['类型']
            if not isinstance(type1, list):
                return
            for t in type1:
                tt = t.lower()
                if tt == 'ss':
                    new_type.append("Shadowsocks")
                elif tt == "ssr":
                    new_type.append("ShadowsocksR")
                elif tt == 'tuic':
                    new_type.append("TUIC")
                else:
                    new_type.append(t.capitalize())
            self.data['类型'] = new_type

    def sort(self, sort_str: str = "订阅原序"):
        if sort_str == "HTTP降序" or sort_str == "HTTP倒序":
            self.sort_by_item("HTTP(S)延迟", reverse=True)
        elif sort_str == "HTTP升序":
            self.sort_by_item("HTTP(S)延迟")
        elif sort_str == "平均速度降序" or sort_str == '平均速度倒序':
            self.sort_by_item("平均速度", reverse=True)
        elif sort_str == "平均速度升序":
            self.sort_by_item("平均速度")
        elif sort_str == '最大速度升序':
            self.sort_by_item("最大速度")
        elif sort_str == '最大速度降序':
            self.sort_by_item("最大速度", reverse=True)

    @staticmethod
    def format_size(size: Union[int, float]):
        import math
        if not isinstance(size, (int, float)):
            return size
        SIZE_UNIT = ["B", "KB", "MB", "GB", "TB", "PB"]
        if size < 1:
            return "0KB"
        i = int(math.floor(math.log(size, 1024)))
        power = math.pow(1024, i)
        size = round(size / power, 2)
        return f"{size}{SIZE_UNIT[i]}"

    def padding(self):
        """
        填充字符
        """

        def padding_rtt(old_rtt: list):
            _new_rtt = []
            for _r in old_rtt:
                _n_r = str(_r).lower()
                _n_r = _n_r if _n_r.endswith("ms") else _n_r + "ms"
                _new_rtt.append(_n_r)
            return _new_rtt

        if 'HTTP(S)延迟' in self.data:
            rtt = self.data['HTTP(S)延迟']
            self.data['HTTP(S)延迟'] = padding_rtt(rtt)
        if 'TLS RTT' in self.data:
            tls_rtt = self.data['TLS RTT']
            self.data['TLS RTT'] = padding_rtt(tls_rtt)
        if '延迟RTT' in self.data:
            rtt = self.data['延迟RTT']
            self.data['延迟RTT'] = padding_rtt(rtt)
        if '平均速度' in self.data:
            new_list = []
            for a in self.data['平均速度']:
                avgspeed = self.format_size(a)
                new_list.append(avgspeed)
            self.data['平均速度'] = new_list
        if '最大速度' in self.data:
            new_list = []
            for a in self.data['最大速度']:
                maxspeed = self.format_size(a)
                new_list.append(maxspeed)
            self.data['最大速度'] = new_list
        if '每秒速度' in self.data:
            self.data['每秒速度'] = [[j / 1024 / 1024 for j in i] for i in self.data['每秒速度']]

    def calc_used(self):
        if '每秒速度' in self.data and '消耗流量' not in self.data:
            traffic_used = 0
            for node_res in self.data['每秒速度']:
                if isinstance(node_res, list):
                    traffic_used += sum(node_res)
                elif isinstance(node_res, (float, int)):
                    traffic_used += node_res
            self.data['消耗流量'] = traffic_used

    def start(self, sort="订阅原序"):
        try:
            self.convert_proxy_typename()
            self.sort(sort)
            self.padding()
            self.calc_used()
            return self.data
        except TypeError as t:
            logger.error(str(t))
            return {}

    def sort_by_item(self, item: str, reverse=False):
        """
        非常具有复用性的代码，我很满意(ง •_•)ง
        """
        if item not in self.data:
            return
        raw_item_list = self.data.get(item, [])
        item_list = deepcopy(raw_item_list)
        if item == "HTTP(S)延迟" and not reverse:
            for i in range(len(item_list)):
                if item_list[i] == 0:
                    item_list[i] = 999999
        temp_1 = [k for k, v in self.data.items()
                  if not isinstance(v, (list, tuple)) or len(v) != len(item_list)]
        temp_dict = {}
        for t in temp_1:
            temp_dict[t] = self.data.pop(t)
        if item_list:
            zipobj = zip(item_list, *(v for k, v in self.data.items()))
            new_list = [list(e) for e in zip(*sorted(zipobj, key=lambda x: x[0], reverse=reverse))]
            new_list.pop(0)
            for i, k in enumerate(self.data.keys()):
                self.data[k] = new_list[i]
            # self.data['平均速度'] = avgspeed
            self.data.update(temp_dict)

    def sort_by_ping(self, reverse: bool = False):
        if 'HTTP(S)延迟' not in self.data:
            return
        http_l = self.data.get('HTTP(S)延迟', [])
        if not reverse:
            for i in range(len(http_l)):
                if http_l[i] == 0:
                    http_l[i] = 999999
        temp_1 = [k for k, v in self.data.items()
                  if not isinstance(v, (list, tuple)) or len(v) != len(http_l)]
        temp_dict = {}
        for t in temp_1:
            temp_dict[t] = self.data.pop(t)
        if http_l:
            zipobj = zip(http_l, *(v for k, v in self.data.items() if len(v) == len(http_l)))
            new_list = [list(e) for e in zip(*sorted(zipobj, key=lambda x: x[0], reverse=reverse))]
            new_list.pop(0)
            for i, k in enumerate(self.data.keys()):
                self.data[k] = new_list[i]
            # self.data['平均速度'] = avgspeed
            self.data.update(temp_dict)

    def sort_by_ping_old(self, reverse=False):
        """
        旧版排序，已废弃
        """
        if 'HTTP(S)延迟' not in self.data:
            return
        http_l = self.data.get('HTTP(S)延迟')
        if not reverse:
            for i in range(len(http_l)):
                if http_l[i] == 0:
                    http_l[i] = 999999
        new_list = [http_l, self.data.get('节点名称'), self.data.get('类型')]
        for k, v in self.data.items():
            if k == "HTTP(S)延迟" or k == "节点名称" or k == "类型":
                continue
            new_list.append(v)
        lists = zip(*new_list)
        lists = sorted(lists, key=lambda x: x[0], reverse=reverse)
        lists = zip(*lists)
        new_list = [list(l_) for l_ in lists]
        http_l = new_list[0] if len(new_list) > 0 else []
        if not reverse:
            for i in range(len(http_l)):
                if http_l[i] == 999999:
                    http_l[i] = 0
        if len(new_list) > 2:
            self.data['HTTP(S)延迟'] = http_l
            self.data['节点名称'] = new_list[1]
            self.data['类型'] = new_list[2]
            num = -1
            for k in self.data.keys():
                num += 1
                if k == "HTTP(S)延迟" or k == "节点名称" or k == "类型":
                    continue
                self.data[k] = new_list[num]


def parse_url(string: str, subcvtconf: SubConverterCFG = None):
    """
    获取URL

    :param: protocol_match: 是否匹配协议URI，并拼接成subconverter形式
    """
    pattern = re.compile("https?://(?:[a-zA-Z]|\d|[$-_@.&+]|[!*,]|[\w\u4e00-\u9fa5])+")  # 匹配订阅地址
    # 获取订阅地址
    try:
        url = pattern.findall(string)[0]  # 列表中第一个项为订阅地址
        return url
    except IndexError:
        if subcvtconf is not None:
            args = ArgCleaner.getarg(string)
            protocol_link = args[1] if len(args) > 1 else string.strip() if not string.startswith("/") else ''
            new_link = protocol_join(protocol_link, subcvtconf)
            return new_link if new_link else None
        else:
            return None


def parse_site(suburl: str) -> str:
    netloc_list = urlparse(suburl).netloc.split('.')
    site = ''
    if len(netloc_list) > 1:
        site = "*." * (len(netloc_list) - 1) + str(netloc_list[-1])
    return site


def parse_command_option(command: str):
    match_option = ["s", "slave", "r", "rule", "sort", "thread", "include", "exclude"]
    question_mark_index = command.find("?")
    command_option_str = ""
    if question_mark_index != -1:
        command_option_str = command[question_mark_index + 1:]
    command_option_split = command_option_str.split("&")
    command_option = {}
    for c in command_option_split:
        _c = c.split("=")
        if len(_c) != 2:
            continue
        if _c[0] == "s":
            command_option["slave"] = _c[1]
        elif _c[0] == "r":
            command_option["rule"] = _c[1]
        elif _c[0] in match_option:
            command_option[_c[0]] = _c[1]
    return command_option


def protocol_join(protocol_link: str, subcvtconf: SubConverterCFG):
    if not protocol_link:
        return ''
    protocol_prefix = ['vmess', 'vless', 'ss', 'ssr', 'trojan', 'hysteria2', 'hysteria',
                       'socks5', 'snell', 'tuic', 'juicity']
    p = protocol_link.split('://')
    if len(p) < 2:
        return ''
    if p[0] not in protocol_prefix:
        return ''

    from urllib.parse import quote
    enable = subcvtconf.enable
    if not isinstance(enable, bool):  # 如果没有解析成bool值，强制禁用subconverter
        enable = False
    if not enable:
        return ''
    subcvtaddr = subcvtconf.address
    remoteconfig = subcvtconf.remoteConfig
    if not remoteconfig:
        remoteconfig = "https%3A%2F%2Fraw.githubusercontent.com%2FACL4SSR%2FACL4SSR%2Fmaster%2FClash%2F" \
                       "config%2FACL4SSR_Online.ini"
    else:
        remoteconfig = quote(remoteconfig)
    scheme = "https" if bool(subcvtconf.tls) else "http"
    new_link = f"{scheme}://{subcvtaddr}/sub?target=clash&new_name=true&url=" + quote(protocol_link) + \
               f"&insert=false&config={remoteconfig}"
    return new_link


def is_valid_path(path_string):
    try:
        path = pathlib.Path(path_string)
        # 检查路径是否是绝对路径
        if path.is_absolute():
            return True
        # 检查路径是否只包含有效的路径组件
        return all(part.isidentifier() or part in ['.', '..'] for part in path.parts)
    except Exception as e:
        logger.error(str(e))
        return False
