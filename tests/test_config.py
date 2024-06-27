import os
import time
from dataclasses import fields

from utils.types.config import KoiConfig


def test_from_yaml():
    _ftcfg = KoiConfig()
    print("from_yaml 方法测试:")
    _ftcfg.from_yaml("admin: [11111, 2222]")
    print(_ftcfg.admin)
    for f in fields(_ftcfg):
        print(f.name, f.type)
    print(_ftcfg)


def test_02():
    ftcfg = KoiConfig()
    ftcfg.from_file("./ftconfig.yml")
    print(ftcfg.admin, type(ftcfg.admin))
    print(str(ftcfg))
    print(ftcfg.image.color.outColor)
    ftcfg.image.color.outColor.sort(key=lambda x: x.label)
    print(ftcfg.image.color.outColor)

    with open("ftconfig3.yml", 'wb') as _fp, open("ftconfig3.json", "w") as _fp2:
        ftcfg.to_yaml(_fp)
        ftcfg.to_json(_fp2)


if __name__ == "__main__":
    t1 = time.time()
    print("当前工作目录: ", os.getcwd())
    test_02()
    print("耗时: ", time.time() - t1)
