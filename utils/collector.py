import asyncio
import re
import time
from urllib.parse import quote, urlparse

import aiohttp
import async_timeout
from aiohttp import ClientConnectorError
from loguru import logger
from yarl import URL

from utils.types.config import KoiConfig


class SubCollector:
    """
    订阅采集器，默认采集clash配置文件
    """

    @logger.catch()
    def __init__(self, suburl: str, koicfg: KoiConfig, force_convert: bool = False):
        """
        这里在初始化中读取了subconverter的相关配置，但是由于sunconverter无人维护，容易出问题，因此之后我不会再维护此功能。也就是在下载订阅时
        订阅转换

        :param: force_convert: 是否强制转换，如果传进来的url本身就已经是subconverter拼接过的，那么套娃转换会拖慢拉去订阅的速度。
                                设置为False会检查是否为subconverter拼接过的
        """
        super().__init__()
        self.text = None
        self.koicfg = koicfg
        self._headers = {'user-agent': 'ClashMetaForAndroid/2.8.9.Meta Mihomo/0.16 Clash.Meta'}  # 这个请求头是获取流量信息的关键
        self.subcvt_conf = koicfg.subconverter
        self.cvt_enable = self.subcvt_conf.enable
        self.url = suburl
        self.codeurl = quote(suburl, encoding='utf-8')
        self.cvt_address = str(self.subcvt_conf.address)
        self.cvt_scheme = self.parse_cvt_scheme()
        self.cvt_url = f"{self.cvt_scheme}://{self.cvt_address}/sub?target=clash&new_name=true&url={self.codeurl}"
        self.sub_remote_config = self.subcvt_conf.remoteConfig
        self.config_include = quote(self.subcvt_conf.include, encoding='utf-8')  # 这两个
        self.config_exclude = quote(self.subcvt_conf.exclude, encoding='utf-8')
        # print(f"配置文件过滤,包含：{self.config_include} 排除：{self.config_exclude}")
        if self.config_include or self.config_exclude:
            self.cvt_url = f"{self.cvt_scheme}://{self.cvt_address}/sub?target=clash&new_name=true&url={self.cvt_url}" \
                           + f"&include={self.config_include}&exclude={self.config_exclude}"
        if self.sub_remote_config:
            self.sub_remote_config = quote(self.sub_remote_config, encoding='utf-8')
            self.cvt_url = self.cvt_url + "&config=" + self.sub_remote_config
        if not force_convert:
            if "/sub?target=" in self.url:
                self.cvt_url = self.url

    def parse_cvt_scheme(self) -> str:
        if not bool(self.subcvt_conf.tls):
            return "http"
        else:
            return "https"

    async def start(self, proxy=None):
        try:
            with async_timeout.timeout(20):
                async with aiohttp.ClientSession(headers=self._headers) as session:
                    async with session.get(self.url, proxy=proxy) as response:
                        return response
        except Exception as e:
            logger.error(e)
            return None

    async def get_site_title(self, proxy=None):
        _headers = ({'user-agent': self.koicfg.network.userAgent} or
                    {'user-agent': 'ClashMetaForAndroid/2.8.9.Meta Mihomo/0.16 Clash.Meta'})
        _proxy = proxy or self.koicfg.network.httpProxy

        async def fetch_title(s: aiohttp.ClientSession, url):
            try:
                async with s.get(url, proxy=_proxy, timeout=5) as response:
                    html = await response.text()
                    title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
                    if title_match:
                        title = title_match.group(1).strip()
                        if "just a moment" in title.lower():
                            title = ""
                    else:
                        title = ""
                    return title
            except (ClientConnectorError, aiohttp.client_exceptions.ClientError, asyncio.TimeoutError):
                return ""
            except Exception as e:
                logger.info(str(e))
                return ""

        parsed_url = urlparse(self.url)
        domain = parsed_url.netloc
        if '.' in parsed_url.netloc:
            n = parsed_url.netloc.split('.')
            domain2 = n[-2] + "." + n[-1]
        else:
            domain2 = ''
        async with aiohttp.ClientSession(headers=_headers) as session:
            if domain:
                url_domain = f"{parsed_url.scheme}://{domain}"
                logger.info(f'获取域名的站点标题: {url_domain}')
                domain_title = await fetch_title(session, url_domain)

            if not domain_title and domain2:
                url_subdomain = f"{parsed_url.scheme}://{domain2}"
                logger.info(f'尝试获取二级域名站点标题: {url_subdomain}')
                domain_title = await fetch_title(session, url_subdomain)

            site_title = domain_title or ""
            return site_title

    @logger.catch()
    async def get_sub_traffic(self, proxy=None):
        """
        获取订阅内的流量
        :return: str
        """
        _headers = ({'user-agent': self.koicfg.network.userAgent} or
                    {'user-agent': 'ClashMetaForAndroid/2.8.9.Meta Mihomo/0.16 Clash.Meta'})
        _proxy = proxy or self.koicfg.network.httpProxy
        try:
            async with aiohttp.ClientSession(headers=_headers) as session:
                async with session.get(self.url, proxy=_proxy, timeout=20) as response:
                    info = response.headers.get('subscription-userinfo', "")
                    info = info.split(';')
                    info2 = {'upload': 0, 'download': 0, 'total': 0, 'expire': 0}
                    for i in info:
                        try:
                            i1 = i.strip().split('=')
                            info2[i1[0]] = float(i1[1]) if i1[1] else 0
                        except IndexError:
                            pass
                    logger.info(str(info2))
                    traffic_up = info2.get('upload', 0) / 1024 / 1024 / 1024
                    traffic_download = info2.get('download', 0) / 1024 / 1024 / 1024
                    traffic_use = traffic_up + traffic_download
                    traffic_total = info2.get('total', 0) / 1024 / 1024 / 1024
                    expire = info2.get('expire', time.time())
                    days_diff = int((expire - time.time()) // (24 * 60 * 60))
                    expire_time = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(expire))
                    if expire_time.startswith('1970') and traffic_total and traffic_use:
                        expire_time = '长期有效'
                        days_diff = 0
                return [traffic_up, traffic_download, traffic_use, traffic_total, expire_time, days_diff]
        except asyncio.exceptions.TimeoutError:
            logger.info("获取订阅超时")
            return []
        except ClientConnectorError as c:
            logger.warning(c)
            return []

    async def get_sub_config(self, save_path: str = None, proxy=None):
        """
        获取订阅配置文件
        :param save_path: 订阅保存路径
        :param proxy:
        :return: 获得一个文件: sub.yaml, bool : True or False
        """
        _headers = ({'user-agent': self.koicfg.network.userAgent} or
                    {'user-agent': 'ClashMetaForAndroid/2.8.9.Meta Mihomo/0.16 Clash.Meta'})
        # suburl = self.url
        suburl = self.cvt_url if self.cvt_enable else self.url
        cvt_text = "subconverter状态: {}".format("已启用" if self.cvt_enable else "未启用")
        logger.info(cvt_text)
        if proxy is not None:
            logger.info(f"using proxy: {proxy}")

        async def safe_read(_response: aiohttp.ClientResponse, limit: int = 52428800):
            if _response.content_length and _response.content_length > limit:
                logger.warning(f"订阅文件大小超过了{limit / 1024 / 1024}MB的阈值，已取消获取。")
                return False
            _data = b''
            if save_path is None:
                while True:
                    _chunk = await _response.content.read(1024)
                    if not _chunk:
                        logger.info("获取订阅成功")
                        break
                    _data += _chunk
                    if len(_data) > limit:
                        logger.warning(f"订阅文件大小超过了{limit / 1024 / 1024}MB的阈值，已取消获取。")
                        return False
                return _data
            else:
                with open(save_path, 'wb+') as fd:
                    while True:
                        _chunk = await _response.content.read(1024)
                        if not _chunk:
                            logger.info("获取订阅成功")
                            break
                        fd.write(_chunk)
            return True

        if "/sub?target=" in suburl:
            suburl = URL(suburl, encoded=True)
        try:
            async with aiohttp.ClientSession(headers=_headers) as session:
                async with session.get(suburl, proxy=proxy, timeout=20) as response:
                    if response.status == 200:
                        return await safe_read(response)
                    else:
                        if self.url == self.cvt_url:
                            return False
                        self.cvt_url = self.url
                        return await self.get_sub_config()
        except asyncio.exceptions.TimeoutError:
            logger.info("获取订阅超时")
            return False
        except ClientConnectorError as c:
            logger.warning(c)
            return False
