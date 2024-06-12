from dataclasses import dataclass

from utils.types import DictCFG
from utils.types.manager import ConfigManager


@dataclass
class Translation(DictCFG, ConfigManager):
    username: str = r"用户名"
    uid: str = r"UID"
    reboot: str = r"正在重启bot..."
    born_1: str = r"您尚未配置管理员，请在bot启动成功后私聊bot发送任意消息，bot会自动将您注册为管理员。"
    born_2: str = r"✅初始化成功，您已被确定成管理员，已将您的身份写入到配置文件~"
    born_3: str = "您的UID为"
    born_4: str = r"✅已初始化管理员"
    is_not_admin: str = r"❌您不是bot的管理员，无法操作。"
    bye: str = r"再见~"
    reboot2: str = r"️开始重启(大约等待五秒)..."
    sysn: str = r"系统名称"
    sysv: str = r"系统版本"
    syst: str = r"系统时间"
    pyv: str = r"Python版本"
    mem: str = r"运行内存"
    bot_version: str = r"Bot版本"
    commit: str = r"提交哈希"
    build_time: str = r"编译时间"
    help_title: str = "节点测试BOT，可用指令如下："
    help_tourist: str = ""
    help_user: str = ""
    help_admin: str = ""
    help_other: str = ""
    help_tail: str = "如有使用问题请与Bot管理员联系"


if __name__ == "__main__":
    t = Translation()
    fields = getattr(t, '__dataclass_fields__')
    print(t)
    with open("zh-CN.yml", 'wb') as fp:
        t.to_yaml(fp, retain_raw=False)

