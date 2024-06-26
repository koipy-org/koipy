from urllib.parse import urlparse

from loguru import logger

from pyrogram.types import Message


class ParseProxyError(Exception):
    pass


def parse_proxy(url: str):
    if url is None:
        return None
    parsed = urlparse(url)
    scheme = parsed.scheme

    if scheme in ('socks5', 'http', 'socks4'):
        # 处理 socks5 或 http 代理链接
        try:
            netloclist = parsed.netloc.split('@')
            if len(netloclist) > 1:
                username, password = netloclist[0].split(':')
                proxy_host, proxy_port = netloclist[1].split(':')
            else:
                username, password = "", ""
                proxy_host, proxy_port = netloclist[0].split(':')
            _proxies = {
                "scheme": scheme,  # "socks4", "socks5" and "http" are supported
                "hostname": proxy_host,
                "port": int(proxy_port)
            }
            if username:
                _proxies['username'] = username
            if password:
                _proxies['password'] = password
            logger.info(f"解析代理配置成功: {_proxies}")
            return _proxies
        except Exception as e:
            raise ParseProxyError("代理地址解析错误") from e
    elif scheme:
        logger.warning(f"此代理类型不支持解析：{url}")
    else:
        logger.warning(f"此代理类型缺少协议头：{url} \n"
                       f"考虑如下格式: socks5://user:pass@proxy.example.com:1080 (user:pass@可省略)")


def gen_key(msg: Message):
    if isinstance(msg, Message):
        return str(msg.chat.id) + ":" + str(msg.id)
    else:
        return None


if __name__ == "__main__":
    # 示例用法
    parse_proxy('socks5://user:pass@proxy.example.com:1080')
    parse_proxy('socks5://proxy.example.com:1080')
    parse_proxy('http://user:pass@proxy.example.com:8080')
    parse_proxy('https://www.example.com/path/to/resource?param=value#section')
