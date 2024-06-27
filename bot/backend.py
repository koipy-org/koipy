#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: www
@Date: 2024/6/26 下午2:17
@Description: 
"""
import contextlib
import json
import ssl
import time
import hashlib
import base64
import asyncio
from copy import deepcopy
from typing import List, Union, Tuple

import aiohttp
from aiohttp import WSMsgType, ClientConnectorError, ClientWebSocketResponse, WSCloseCode
from loguru import logger
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot import check
from bot.config import lang, CONFIG
from bot.queue import message_edit_queue as meq
from bot.api import Api
from utils.export import KoiDraw
from utils.types.items import ScriptItem, BaseItem, ItemType
from utils.types.miaospeed import SlaveRequestMatrixEntry, SlaveRequestConfigs, SlaveRequestNode, \
    SlaveRequest as MSSlaveRequest, SlaveRequestMatrixType, SSLType, SlaveRequestBasics, Script as MSScript
from utils.types.task import SlaveRequest
from utils.types.config import MiaoSpeedSlave

DEFAULT_DOWNLOAD_URL = CONFIG.runtime.speedFiles
MS_BUILDTOKEN = "MIAOKO4|580JxAo049R|GEnERAl|1X571R930|T0kEN"  # miaospeed的build_token
MS_CONN = {}
SPEEDTESTIKM = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton(lang.task_stop_1, callback_data=Api.speed_stop)],
    ]
)
CONNTESTIKM = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton(lang.task_stop_2, callback_data=Api.speed_stop)],
    ]
)


class MiaoSpeed:
    def __init__(self,
                 buildtoken: str,
                 proxyconfig: list,
                 slave_req_matrix_entry_list: List[SlaveRequestMatrixEntry],
                 host: str = '127.0.0.1',
                 port: int = 1112,
                 start_token: str = "",
                 ssl_type: SSLType = SSLType.SECURE,
                 slave_config: SlaveRequestConfigs = None,
                 debug: bool = False,
                 ):
        """
        初始化miaospeed
        :paran buildtoken miaospeed的编译token
        :param proxyconfig 订阅配置
        :param slave_req_matrix_entry_list 构造的请求数据矩阵
        :param host 主机名
        :param port 端口
        :param start_token 启动token
        :param ssl_type [0: 无加密 1: tls加密 2: miaospeed tls自签证书适配]
        :param slave_config 测速后端自定义配置。
        :param debug 是否是debug模式，会打印出多一点信息

        """
        self.buildtoken = buildtoken
        self.token = start_token
        self.host = host
        self.port = port
        self.nodes = proxyconfig
        self.ssl_type = ssl_type
        self._debug = debug
        self.slaveRequestNode = [SlaveRequestNode(str(i), str(node)) for i, node in enumerate(self.nodes)]
        # self.slaveRequestNode = [{'Name': f'{i}', 'Payload': str(node)} for i, node in enumerate(self.nodes)]
        self.SlaveRequest = MSSlaveRequest()
        self.SlaveRequest.Options.Matrices = slave_req_matrix_entry_list
        if slave_config:
            self.SlaveRequest.Configs = slave_config
        # self.SlaveRequest = deepcopy(SlaveRequest)
        self.SlaveRequest.Nodes = self.slaveRequestNode

    def hash_miaospeed(self, token: str, request: str):
        buildTokens = [token] + self.buildtoken.strip().split('|')
        hasher = hashlib.sha512()
        hasher.update(request.encode())

        for t in buildTokens:
            if t == "":
                # unsafe, please make sure not to let token segment be empty
                t = "SOME_TOKEN"

            copy = hasher.copy()
            copy.update(t.encode())
            copy.update(hasher.digest())
            hasher = copy

        hash_url_safe = base64.urlsafe_b64encode(hasher.digest()).decode().replace("+", "-").replace("/", "_")
        return hash_url_safe

    def sign_request(self, branch: int = None):
        copysrt = deepcopy(self.SlaveRequest)  # 用深拷贝复制一份请求体数据，python拷贝行为涉及可变和不可变序列。
        copysrt.Challenge = ""  # 置为空是因为要与这个值进行比较，要是不为空，大概永远也过不了验证
        copysrt.Vendor = ""  # 因为miaospeed在这里拷贝的时候，并没有拷贝原来的Vendor值
        srt_json = copysrt.to_json()
        signed_req = self.hash_miaospeed(self.token, srt_json)
        self.SlaveRequest.Challenge = signed_req
        return signed_req

    def convert_result(self, _resdata: dict):
        info = {
            "节点名称": [],
            "类型": [],
        }

        _resdata = _resdata.pop('Result', {}).pop('Results', [])

        def get_node_index(r: dict):
            return self.nodes.index(list(filter(lambda node: node['name'] == r['ProxyInfo']['Name'], self.nodes))[0])

        with contextlib.suppress(Exception):
            _resdata: List[dict] = sorted(_resdata, key=get_node_index, reverse=False)

        for _r in _resdata:
            proxyinfo = _r.get('ProxyInfo', {})
            info["节点名称"].append(proxyinfo['Name'])
            info["类型"].append(proxyinfo['Type'])
            matrices: List[dict] = _r.get('Matrices', [])
            for m in matrices:
                if 'Type' in m:
                    j_obj: dict = json.loads(m.get('Payload', ""))
                    if m['Type'] == SlaveRequestMatrixType.TEST_PING_CONN.value:
                        if j_obj:
                            if "HTTP(S)延迟" not in info:
                                info["HTTP(S)延迟"] = []
                            delay = j_obj.get('Value', 0)
                            if delay and isinstance(delay, (int, float)):
                                info["HTTP(S)延迟"].append(delay)
                            else:
                                info["HTTP(S)延迟"].append(0)
                    elif m['Type'] == SlaveRequestMatrixType.TEST_PING_RTT.value:
                        rtt_type = "TLS RTT" if "https" in self.SlaveRequest.Configs.PingAddress.lower() else "延迟RTT"
                        if j_obj:
                            if rtt_type not in info:
                                info[rtt_type] = []
                            info[rtt_type].append(j_obj.get('Value', 0))
                    elif m['Type'] == SlaveRequestMatrixType.TEST_SCRIPT.value:
                        if j_obj:
                            script_name = j_obj.get('Key', '')
                            if script_name and (script_name != "HTTP(S)延迟" or script_name != "HTTP延迟"):
                                if script_name not in info:
                                    info[script_name] = []
                                info[script_name].append(j_obj.get('Text', "N/A"))
                    elif m['Type'] == SlaveRequestMatrixType.UDP_TYPE.value:
                        if "UDP类型" not in info:
                            info["UDP类型"] = []
                        info["UDP类型"].append(j_obj.get('Value', "Unknown"))
                    elif m['Type'] == SlaveRequestMatrixType.SPEED_AVERAGE.value:
                        if "平均速度" not in info:
                            info["平均速度"] = []
                        info["平均速度"].append(j_obj.get('Value', 0))
                    elif m['Type'] == SlaveRequestMatrixType.SPEED_MAX.value:
                        if "最大速度" not in info:
                            info["最大速度"] = []
                        info["最大速度"].append(j_obj.get('Value', 0))
                    elif m['Type'] == SlaveRequestMatrixType.SPEED_PER_SECOND.value:
                        if "每秒速度" not in info:
                            info["每秒速度"] = []
                        info["每秒速度"].append(j_obj.get('Speeds', []))
                    elif m['Type'] == SlaveRequestMatrixType.GEOIP_OUTBOUND.value:
                        print(j_obj)
                        info['outbound'] = j_obj
                    elif m['Type'] == SlaveRequestMatrixType.GEOIP_INBOUND.value:
                        print(j_obj)
                        info['inbound'] = j_obj
        info['线程'] = self.SlaveRequest.Configs.DownloadThreading
        return info

    async def start(self, slavereq: SlaveRequest = None):
        start_time = time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime())
        resdata = {}
        connected = False
        botmsg_d2 = {'message-id': slavereq.task.botMsgID, 'chat-id': slavereq.task.botMsgChatID}
        conn_key = str(botmsg_d2.get('chat-id', 0)) + ":" + str(botmsg_d2.get('message-id', 0))
        ws_scheme, verify_ssl = self.get_ws_opt()
        if len(MS_CONN) > 100:  # 清理占用
            logger.warning("WebSocket连接资源已超过100条，请联系开发者优化。")
        async with aiohttp.ClientSession() as session:
            try:
                async with session.ws_connect(f"{ws_scheme}://{self.host}:{self.port}", verify_ssl=verify_ssl) as ws:
                    self.sign_request()  # 签名请求
                    connected = True
                    count = 0
                    time1 = time.time()
                    if conn_key not in MS_CONN:
                        MS_CONN[conn_key] = ws
                    await ws.send_str(self.SlaveRequest.to_json())
                    while True:
                        msg = await ws.receive()
                        if self._debug:
                            print(msg.data)
                        if msg.type in (aiohttp.WSMsgType.CLOSED,
                                        aiohttp.WSMsgType.ERROR):
                            logger.info("退出循环")
                            break
                        elif msg.type == WSMsgType.TEXT:
                            ms_data: dict = json.loads(msg.data)
                            if not ms_data:
                                continue
                            if 'Result' in ms_data and ms_data.get('Result', {}):
                                resdata = self.convert_result(ms_data)
                                break
                            elif 'Error' in ms_data and ms_data.get('Error', ''):
                                error_text = f"{lang.error} {ms_data.get('Error', '')}"
                                if botmsg_d2:
                                    put_opt = (slavereq.task.botMsgChatID, slavereq.task.botMsgID, error_text)
                                    meq.put(put_opt + (5,))
                                break
                            elif 'Progress' in ms_data and ms_data.get('Progress', {}):
                                prograss = ms_data.get('Progress', {})
                                queuing = prograss.get('Queuing', 0)
                                cidx = 3
                                scomment = slavereq.slave.comment
                                count += 1
                                time2 = time.time()
                                if count == 1 or count == len(self.nodes) or (count % 4 == 0 and time2 - time1 > 4):
                                    time1 = time.time()
                                    ikm = SPEEDTESTIKM if cidx == 1 else CONNTESTIKM
                                    progress_text = ms_progress_text(cidx, count, len(self.nodes), queuing,
                                                                     scomment)
                                    if len(self.nodes) > 20:
                                        progress_text += lang.ws_conn_msg
                                    p_opt = (slavereq.task.botMsgChatID, slavereq.task.botMsgID, progress_text, 5, ikm)
                                    meq.put(p_opt)
                        elif msg.type == aiohttp.WSMsgType.BINARY:
                            pass
                    # await ws.close()
                    await ws.close(code=aiohttp.WSCloseCode.GOING_AWAY,
                                   message=b'(EOF)The connection is closed by the peer.')
            except ClientConnectorError as e:
                logger.error(str(e))
                err_text = lang.ws_conn_err2
                put_opt = (slavereq.task.botMsgChatID, slavereq.task.botMsgID, err_text, 5)
                meq.put(put_opt)
            except asyncio.TimeoutError:
                if connected:
                    err_text = f"{lang.ws_conn_err3}{self.port}"
                    logger.info(err_text)
                else:
                    err_text = f"{lang.ws_conn_err4}{self.port}"
                    logger.warning(err_text)
                    put_opt = (slavereq.task.botMsgChatID, slavereq.task.botMsgID, err_text, 5)
                    meq.put(put_opt)
            except Exception as e:
                logger.error(str(e))
            except KeyboardInterrupt:
                await ws.close()
            finally:
                if conn_key in MS_CONN:
                    MS_CONN.pop(conn_key)
                return resdata, start_time

    def get_ws_opt(self) -> Tuple[str, bool]:
        if self.ssl_type == SSLType.SECURE:
            ssl_context = ssl.create_default_context()
            verify_ssl = True
        elif self.ssl_type == SSLType.SELF_SIGNED:
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            verify_ssl = False
        elif self.ssl_type == SSLType.NONE:
            ssl_context = None
            verify_ssl = None
        else:
            raise ValueError(f"{lang.ms_type_err2} {type(self.ssl_type).__name__}:{self.ssl_type}")
        ws_scheme = "ws" if ssl_context is None else "wss"
        return ws_scheme, verify_ssl

    async def ping(self, session: aiohttp.ClientSession):
        ws_scheme, verify_ssl = self.get_ws_opt()
        try:
            async with session.ws_connect(f"{ws_scheme}://{self.host}:{self.port}", verify_ssl=verify_ssl) as ws:
                self.sign_request()  # 签名请求
                await ws.send_str(self.SlaveRequest.to_json())
                while True:
                    msg = await ws.receive()
                    if msg.type in (aiohttp.WSMsgType.CLOSED,
                                    aiohttp.WSMsgType.ERROR):
                        return False
                    elif msg.type == WSMsgType.TEXT:
                        return True
        except (ClientConnectorError, asyncio.TimeoutError):
            return False
        except Exception as e:
            logger.error(str(e))
            return False

    @staticmethod
    async def stop(conn_key: str) -> str:
        if conn_key in MS_CONN:
            ws_conn = MS_CONN[conn_key]
            if isinstance(ws_conn, ClientWebSocketResponse):
                try:
                    await ws_conn.close(code=WSCloseCode.GOING_AWAY)
                    return ""
                except Exception as e:
                    logger.warning(str(e))
                    return str(e)
        else:
            return lang.ws_conn_err


stopspeed = MiaoSpeed.stop


def ms_progress_text(corelabel: Union[int, str], progress: int, nodenum: int, queuing: int, scomment: str = "Local"):
    if corelabel == 'SpeedCore' or corelabel == 1:
        testtext = CONFIG.bot.speedText or lang.progress_1
    elif corelabel == 'TopoCore' or corelabel == 2:
        testtext = CONFIG.bot.analyzeText or lang.progress_2
    elif corelabel == 'ScriptCore' or corelabel == 3:
        testtext = CONFIG.bot.scriptText or lang.progress_3
    else:
        testtext = "未知测试进行中"
    # if scomment == "Local":
    #     scomment = GCONFIG.get_default_slave().get('comment', 'Local')
    progress_bars = CONFIG.bot.bar
    bracketsleft = CONFIG.bot.bleft
    bracketsright = CONFIG.bot.bright
    bracketsspace = CONFIG.bot.bspace

    cal = progress / nodenum * 100
    p_text = "%.2f" % cal
    equal_signs = int(cal / 5)
    space_count = 20 - equal_signs
    progress_bar = f"{bracketsleft}" + f"{progress_bars}" * equal_signs + \
                   f"{bracketsspace}" * space_count + f"{bracketsright}"
    if queuing > 0:
        edit_text = (f"{lang.progress_4}{scomment}\n{testtext}\n{lang.progress_5} `{queuing}`\n\n" + progress_bar +
                     f"\n\n{lang.progress_6}\n" + p_text + "%     [" + str(progress) + "/" + str(nodenum) + "]")
    else:
        edit_text = f"{lang.progress_4}{scomment}\n{testtext}\n\n" + progress_bar + f"\n\n{lang.progress_6}\n" + \
                    p_text + "%     [" + str(progress) + "/" + str(nodenum) + "]"
    return edit_text


# def build_req_config(req_conf: dict) -> SlaveRequestConfigs:
#     return SlaveRequestConfigs.from_option(req_conf)


def build_req_matrix(coreindex: int, items: List[ItemType] = None) -> List[SlaveRequestMatrixEntry]:
    if items and not isinstance(items[0], (BaseItem, ScriptItem)):
        return []
    if coreindex == 3:
        # srme_list = [SlaveRequestMatrixEntry(SlaveRequestMatrixType.TEST_PING_RTT, ""),
        #              SlaveRequestMatrixEntry(SlaveRequestMatrixType.TEST_PING_CONN, "")]
        srme_list = []
        if items:
            for i in items:
                if i.name == "TEST_SCRIPT":
                    srme_list.append(
                        SlaveRequestMatrixEntry(
                            Type=SlaveRequestMatrixType.TEST_SCRIPT,
                            Params=i.script.name
                        )
                    )
                elif i.name == "TEST_PING_RTT":
                    srme_list.append(SlaveRequestMatrixEntry(SlaveRequestMatrixType.TEST_PING_RTT, ""))
                elif i.name == "TEST_PING_CONN":
                    srme_list.append(SlaveRequestMatrixEntry(SlaveRequestMatrixType.TEST_PING_CONN, ""))
                elif i.name == "SPEED_AVERAGE":
                    srme_list.append(SlaveRequestMatrixEntry(SlaveRequestMatrixType.SPEED_AVERAGE, "0"))
                elif i.name == "SPEED_MAX":
                    srme_list.append(SlaveRequestMatrixEntry(SlaveRequestMatrixType.SPEED_MAX, "0"))
                elif i.name == "SPEED_PER_SECOND":
                    srme_list.append(SlaveRequestMatrixEntry(SlaveRequestMatrixType.SPEED_PER_SECOND, "0"))
                elif i.name == "UDP_TYPE":
                    srme_list.append(SlaveRequestMatrixEntry(SlaveRequestMatrixType.UDP_TYPE, "0"))

    elif coreindex == 1:
        srme_list = [
            SlaveRequestMatrixEntry(SlaveRequestMatrixType.TEST_PING_RTT, ""),
            SlaveRequestMatrixEntry(SlaveRequestMatrixType.TEST_PING_CONN, ""),
            SlaveRequestMatrixEntry(SlaveRequestMatrixType.SPEED_AVERAGE, "0"),
            SlaveRequestMatrixEntry(SlaveRequestMatrixType.SPEED_MAX, "0"),
            SlaveRequestMatrixEntry(SlaveRequestMatrixType.SPEED_PER_SECOND, "0"),
            SlaveRequestMatrixEntry(SlaveRequestMatrixType.UDP_TYPE, "0"),
        ]
    else:
        srme_list = []
    return srme_list


async def miaospeed_client(app: Client, slavereq: SlaveRequest):
    s1 = time.time()
    if not isinstance(slavereq.slave, MiaoSpeedSlave):
        raise TypeError(lang.ms_type_err)

    flt_obj = {"include": slavereq.runtime.includeFilter, "exclude": slavereq.runtime.excludeFilter}
    key = slavereq.slave.token
    tls = slavereq.slave.tls
    if tls:
        ssl_opt = SSLType.SECURE if not slavereq.slave.skipCertVerify else SSLType.SELF_SIGNED
    else:
        ssl_opt = SSLType.NONE
    msbuild_token = slavereq.slave.buildtoken or MS_BUILDTOKEN
    if not isinstance(app, Client):
        logger.warning("Failed to get Bot client instance, will not be able to generate and send images.")
        return
    coreindex = 3
    # script_list: list[str] = data.get('script', [])
    # botmsg_d2 = data.get('edit-message', {})
    # botmsg_d1 = data.get('origin-message', {})
    addr = slavereq.slave.address
    i = addr.rfind(":")
    # addrsplit = addr.split(":")
    host = addr[:i]
    try:
        ws_port = int(addr[i + 1:])
    except (TypeError, ValueError):
        return
    srme_list = build_req_matrix(coreindex, slavereq.items)
    srcfg = SlaveRequestConfigs.from_option(slavereq.slave.option)
    if not srme_list:
        temp_text = "❌MiaoSpeed后端暂不支持发起拓扑测试"
        await app.edit_message_text(slavereq.task.botMsgChatID, slavereq.task.botMsgID, temp_text)
        return
    ms = MiaoSpeed(msbuild_token, slavereq.proxies, srme_list, host, ws_port, key, ssl_opt, srcfg)
    ms.SlaveRequest.Basics = SlaveRequestBasics(
        ID="114514",
        Slave=str(slavereq.slave.id),
        SlaveName=slavereq.slave.comment,
        Invoker=str(slavereq.slave.invoker) or str(app.me.id),
        Version="1.0"
    )
    if coreindex == 3:
        for item in slavereq.items:
            if item.script and item.script.content:
                ms.SlaveRequest.Configs.Scripts.append(MSScript(ID=item.script.name, Content=item.script.content))
        # for s in script_list:
        #     js_content = addon.global_js_script.get(s.lower(), "")
        #     if js_content:
        #         ms.SlaveRequest.Configs.Scripts.append(Script(ID=s, Content=js_content))

    try:
        result, _ = await ms.start(slavereq)
        from utils.cleaner import ResultCleaner
        result = ResultCleaner(result).start(slavereq.runtime.sort)
    except Exception as e:
        logger.error(str(e))
        return

    msg_id = slavereq.task.messageID
    chat_id = slavereq.task.botMsgChatID
    botmsg_id = slavereq.task.botMsgID

    if not msg_id and not botmsg_id and not chat_id:
        logger.warning("获取消息失败！")
        return
    if result:
        result['filter'] = flt_obj
        result['slave'] = {
            'id': slavereq.slave.id,
            'comment': slavereq.slave.comment
        }
        result['sort'] = slavereq.runtime.sort
        result['task'] = {
            'initiator': slavereq.task.creator,
            'name': slavereq.task.name,
            'site': slavereq.task.name
        }
        s2 = time.time() - s1
        result['wtime'] = f"{s2:.1f}"
        loop = asyncio.get_running_loop()
        try:
            kd = KoiDraw('节点名称', result, CONFIG)
            file_name, img_size = await loop.run_in_executor(None, kd.draw)
            # 发送回TG
            await check.check_photo(app, msg_id, botmsg_id, chat_id, file_name, result['wtime'] + "s", img_size)
            # await select_export(app, msg_id, botmsg_id, chat_id, puttype[data.get('coreindex', -1)], result)
        except Exception as e:
            logger.error(str(e))


if __name__ == '__main__':
    pass
