import os.path

from utils.types.config import KoiConfig, SystemCFG, Translation
CONFIG = KoiConfig()
CONFIG_PATH = "./resources/config.yaml"
if os.path.exists(CONFIG_PATH):
    CONFIG.from_file(CONFIG_PATH)
CONFIG.translation.lang = CONFIG.translation.lang.replace("-", "_")
SYS_CONFIG = SystemCFG().load_tr_config(CONFIG.translation.resources, Translation)
lang = TRANSLATE_CONFIG = SYS_CONFIG.translation.get(CONFIG.translation.lang, Translation())
admin = CONFIG.admin
print("翻译已加载: ", lang)
