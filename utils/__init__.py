import asyncio
from os import getcwd

__version__ = "1.0"  # 项目版本号

from typing import Optional

HOME_DIR = getcwd()
__all__ = [
    "__version__",
    "HOME_DIR",
    "async_runtime"
]


def async_runtime(loop: Optional[asyncio.AbstractEventLoop] = None):
    """
    临时的异步运行时，适用于只有一两个异步函数的情况
    :param: loop: 事件循环
    """
    if loop is None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    def wrapper(func):
        def inner(*args, **kwargs):
            result = loop.run_until_complete(func(*args, **kwargs))
            return result

        return inner

    return wrapper
