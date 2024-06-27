import os
from utils.types.config import KoiConfig, SystemCFG, Translation
HOME_DIR = os.getcwd()
CONFIG = KoiConfig()
CONFIG_PATH = os.path.join(HOME_DIR, 'config.yaml')
if os.path.exists(CONFIG_PATH):
    CONFIG.from_file(CONFIG_PATH)
else:
    raise NameError(f"No configuration file was found. You should put the configuration file in the {HOME_DIR}")
CONFIG.translation.lang = CONFIG.translation.lang.replace("-", "_")
SYS_CONFIG = SystemCFG().load_tr_config(CONFIG.translation.resources, Translation)
lang = TRANSLATE_CONFIG = SYS_CONFIG.translation.get(CONFIG.translation.lang, Translation())
admin = CONFIG.admin
print(lang.tr_ok, lang)
