import json
import os
import sys
from pathlib import Path

import tzlocal
from loguru import logger
from apscheduler.triggers.interval import IntervalTrigger
from pyrogram import Client

from bot.config import CONFIG
from bot.cron.schedule import scheduler
from bot.utils import parse_proxy
from bot.queue import message_delete_queue, message_edit_queue, handler_delete_queue
from utils import HOME_DIR, async_runtime
# from utils.cleaner import unzip, unzip_targz
# from utils.collector import get_latest_tag, Download, DownloadError


from bot.cron import cron_delete_message as cdm, cron_edit_message as cem, cron_delete_handler as cdh

BOT_VERSION = __version__ = "1.0"
app = Client(
    "my_bot",
    api_id=CONFIG.bot.api_id,
    api_hash=CONFIG.bot.api_hash,
    bot_token=CONFIG.bot.bot_token,
    proxy=parse_proxy(CONFIG.bot.proxy),
    app_version=__version__,
    ipv6=False
)


@async_runtime(loop=app.loop)
async def check_init():
    check_py_version()
    Init.init_cron()
    Init.init_dir()
    Init.init_user()
    await Init.init_emoji()
    # await Init.init_proxy_client()  # init_permission 的顺序和这里不能调换
    # Init.init_permission()
    return True


def check_py_version() -> None:
    if sys.version_info < (3, 9):
        py_url = "https://www.python.org/downloads/"
        logger.error(f"您的Python版本为{sys.version}。\n至少需要Python3.9才能运行此程序。前往: {py_url}下载新版本。")
        sys.exit()
    elif sys.version_info >= (3, 12):
        logger.warning(f"您的Python版本为{sys.version}。项目对该版本的支持是实验性的，如果有兼容性问题，请联系开发者。")


# def check_args():
#     import argparse
#     help_text_socks5 = "设置socks5代理，bot代理使用的这个\n格式--> host:端口:用户名:密码\t用户名和密码可省略"
#     help_text_http = "设置HTTP代理,拉取订阅用的。\n格式--> 用户名:密码@host:端口\t@符号前面的用户名和密码如果不设置可省略"
#     help_f = "强制覆盖原先的mybot.session文件，重新生成"
#     parser = argparse.ArgumentParser(
#         description="FullTClash命令行快速启动，其中api_id,api_hash,bot_token要么不填，要么全部填完")
#     parser.add_argument("-r", action='store_true', help=help_f)
#     parser.add_argument("-ah", "--api-hash", required=False, type=str, help="自定义api-hash")
#     parser.add_argument("-ai", "--api-id", required=False, type=int, help="自定义api-id")
#     parser.add_argument("-b", "--bot-token", required=False, type=str, help="自定义bot-token")
#     parser.add_argument("-ps5", "--proxy-socks5", required=False, type=str, help=help_text_socks5)
#     parser.add_argument("-http", "--proxy-http", required=False, type=str, help=help_text_http)
#     parser.add_argument("-su", "--admin", required=False, help="设置bot的管理员，多个管理员以 , 分隔")
#     parser.add_argument("-d", "--path", required=False, type=str, help="设置代理客户端路径")
#
#     args = parser.parse_args()
#     if args.r:
#         if os.path.exists("./my_bot.session"):
#             logger.info("检测到启用session文件覆写选项")
#             try:
#                 os.remove("my_bot.session")
#                 logger.info("已移除my_bot.session")
#             except Exception as e2:
#                 logger.error(f"session文件移除失败：{e2}")
#     if args.path:
#         GCONFIG.yaml['clash'] = GCONFIG.config.get('clash', {}).setdefault('path', str(args.d))
#     if args.admin:
#         adminlist = str(args.admin).split(",")
#         logger.info(f"即将添加管理员：{adminlist}")
#         GCONFIG.add_admin(adminlist)
#     if args.proxy_http:
#         GCONFIG.yaml['proxy'] = str(args.proxy_http)
#         logger.info("从命令行参数中设置HTTP代理")
#     if args.api_hash and args.api_id and args.bot_token:
#         tempconf = {
#             "api_hash": args.api_hash,
#             "api_id": args.api_id,
#             "bot_token": args.bot_token,
#             "proxy": args.proxy_socks5,
#         }
#         bot_conf = GCONFIG.getBotconfig()
#         bot_conf.update(tempconf)
#         GCONFIG.yaml['bot'] = bot_conf
#         logger.info("从命令行参数中设置api_hash,api_id,bot_token")
#         if args.proxy_socks5:
#             logger.info("从命令行参数中设置bot的socks5代理")
#     i = GCONFIG.reload()
#     if i:
#         if GCONFIG.yaml != GCONFIG.config:
#             logger.info("已覆写配置文件。")
#     else:
#         logger.warning("覆写配置失败！")


class Init:
    repo_owner = "AirportR"
    repo_name = "fulltclash"
    ftcore_owner = repo_owner
    ftcore_name = "FullTCore"

    @staticmethod
    def init_cron():
        scheduler.start()
        scheduler.add_job(cdm, IntervalTrigger(seconds=10, timezone=str(tzlocal.get_localzone())), max_instances=10,
                          id='delete1', name="Delete the telegram message", args=(app, message_delete_queue))
        scheduler.add_job(cem, IntervalTrigger(seconds=5, timezone=str(tzlocal.get_localzone())), max_instances=10,
                          id='edit1', name="Edit the telegram message", args=(app, message_edit_queue))
        scheduler.add_job(cdh, IntervalTrigger(seconds=5, timezone=str(tzlocal.get_localzone())), max_instances=10,
                          id='remove1', name="remove the pyrogram handlers", args=(app, handler_delete_queue))

    @staticmethod
    def init_user():
        admin = CONFIG.admin  # 管理员
        user_list = set(CONFIG.user)
        user_list.update(admin)
        CONFIG.user.from_obj(list(user_list))  # 管理员同时也是用户

    @staticmethod
    def init_dir():
        dirs = os.listdir(HOME_DIR)
        if "logs" in dirs and "results" in dirs:
            return
        logger.info("检测到初次使用，正在初始化...")
        if not os.path.isdir('logs'):
            os.mkdir("logs")
            logger.info("创建文件夹: logs 用于保存日志")
        if not os.path.isdir('results'):
            os.mkdir("results")
            logger.info("创建文件夹: results 用于保存测试结果")

    @staticmethod
    async def init_emoji():
        emoji_source = "TwemojiLocalSource"
        if CONFIG.image.emoji.enable and emoji_source == 'TwemojiLocalSource':
            from utils.myemoji import TwemojiLocalSource
            if not os.path.isdir('./resources/emoji/twemoji'):
                twemoji = TwemojiLocalSource()
                logger.info("检测到未安装emoji资源包，正在初始化本地emoji...")
                await twemoji.download_emoji(proxy=CONFIG.network.httpProxy)
                if twemoji.init_emoji(twemoji.savepath):
                    logger.info("初始化emoji成功")
                else:
                    logger.warning("初始化emoji失败")
    #
    # @staticmethod
    # def init_permission():
    #     if sys.platform != "win32":
    #         try:
    #             status = os.system(f"chmod +x {GCONFIG.get_clash_path()}")
    #             if status != 0:
    #                 raise OSError(f"Failed to execute command: chmod +x {GCONFIG.get_clash_path()}")
    #         except OSError as o:
    #             print(o)
    #         try:
    #              os.system(f"chmod +x updater")
    #         except OSError as o:
    #             print(o)
    #
    # @staticmethod
    # def init_commit_string():
    #     _latest_version_hash = ""
    #     try:
    #         output = check_output(['git', 'log'], shell=False, encoding="utf-8").strip()
    #         # 解析输出，提取最新提交的哈希值
    #         for line in output.split("\n"):
    #             if "commit" in line:
    #                 _latest_version_hash = line.split()[1][:7]
    #                 break
    #     except Exception as e:
    #         logger.info(f"可能不是通过git拉取源码，因此version将无法查看提交哈希。{str(e)}")
    #         _latest_version_hash = "Unknown"
    #     return _latest_version_hash

    # @staticmethod
    # async def init_proxy_client():
    #     """
    #     自动下载代理客户端FullTCore
    #     """
    #     if GCONFIG.get_clash_path() is not None:
    #         return
    #     import platform
    #     tag = await get_latest_tag(Init.ftcore_owner, Init.ftcore_name)
    #     tag2 = tag[1:] if tag[0] == "v" else tag
    #     arch = platform.machine().lower()
    #     if arch == "x86_64":
    #         arch = "amd64"
    #     elif arch == "aarch64" or arch == "armv8":
    #         arch = "arm64"
    #     elif arch == "x86":
    #         arch = "i386"
    #     elif arch == "arm":
    #         arch = "armv7l"
    #     suffix = ".tar.gz"
    #     if sys.platform.startswith('linux'):
    #         pf = "linux"
    #     elif sys.platform.startswith('darwin'):
    #         pf = "darwin"
    #     elif sys.platform.startswith('win32'):
    #         pf = "windows"
    #         suffix = ".zip"
    #     else:
    #         logger.info("无法找到FullTCore在当前平台的预编译文件，请自行下载。")
    #         return
    #
    #     # https://github.com/AirportR/FullTCore/releases/download/v1.3-meta/FullTCore_1.3-meta_windows_amd64.zip
    #     base_url = f"https://github.com/{Init.ftcore_owner}/{Init.ftcore_name}"
    #
    #     download_url = base_url + f"/releases/download/{tag}/{Init.ftcore_name}_{tag2}_{pf}_{arch}{suffix}"
    #     savename = download_url.split("/")[-1]
    #     logger.info(f"正在自动为您下载最新版本({tag})的FullTCore: {download_url}")
    #     savepath = Path(HOME_DIR).joinpath("bin").absolute()
    #     saved_file = savepath.joinpath(savename)
    #
    #     try:
    #         await Download(download_url, savepath, savename).dowload(proxy=GCONFIG.get_proxy())
    #     except DownloadError:
    #         logger.info("无法找到FullTCore在当前平台的预编译文件，请自行下载。")
    #         return
    #     except (OSError, Exception) as e:
    #         logger.info(str(e))
    #         return
    #
    #     if suffix.endswith("zip"):
    #         unzip_result = unzip(saved_file, savepath)
    #     elif suffix.endswith("tar.gz"):
    #         unzip_result = unzip_targz(saved_file, savepath)
    #     else:
    #         unzip_result = False
    #     if unzip_result:
    #         if pf == "windows":
    #             corename = Init.ftcore_name + ".exe"
    #         else:
    #             corename = Init.ftcore_name
    #         proxy_path = str(savepath.joinpath(corename).as_posix())
    #         clash_cfg = GCONFIG.config.get('clash', {})
    #         clash_cfg = clash_cfg if isinstance(clash_cfg, dict) else {}
    #         clash_cfg['path'] = proxy_path
    #         GCONFIG.yaml['clash'] = clash_cfg
    #         GCONFIG.reload()


def update(new_exe: str = None, information: str = ""):
    # print("版本:", __version__)
    # print(sys.argv)
    if new_exe is None:
        return
    aa = Path(new_exe)
    if aa.is_file():
        with open("need_to_upgrade.json", "w") as fp:
            d = {
                "old": str(Path(sys.argv[0]).as_posix()),
                "new": str(aa.absolute().as_posix()),
                "information": str(information)
            }
            print(d)
            json.dump(d, fp)

        updater_path = "updater.exe" if sys.platform.startswith('win32') else "updater"
        updater_path = Path(updater_path).absolute()

        if updater_path.is_file():
            updater_path2 = updater_path.as_posix()
            if sys.platform.startswith('win32'):
                updater_path2 = os.path.normpath(updater_path)
            print(updater_path2)
            compiled = getattr(update, "__compiled__", None)  # 是否处于编译状态
            if compiled:
                os.execlp(updater_path2, updater_path2)
            else:
                os.execlp(sys.executable, "main.py", *sys.argv)
        else:
            print("找不到更新程序，请联系开发者解决此问题。")
    else:
        print("找不到文件: ", new_exe)


check_init()
