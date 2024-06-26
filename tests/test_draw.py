from loguru import logger


@logger.catch()
def test():
    from random import randint
    koicfg = KoiConfig().from_file("resources/config.yaml")

    koicfg.image.color.delay.sort(key=lambda x: x.label)
    koicfg.image.color.speed.sort(key=lambda x: x.label)

    koicfg.image.title = "配色绘图示例"
    nodenum = min(len(koicfg.image.color.delay), len(koicfg.image.color.speed))
    if nodenum == 0:
        raise ValueError("请先设置好配色")
    tips = ["解锁(US)", "失败", "待解锁(HK)", "超时", "N/A"]
    tips.extend(["解锁" for _ in range(abs(nodenum - 5))])
    a = [[float(j * 50) for j in range(randint(0, 10))] for _ in range(100)]
    a = a[:nodenum]
    a[-1] = [koicfg.image.color.speed[-1].label for _ in range(15)]
    test_result = {
        "节点名称": [f"🚩节点{i} --> {tips[i]}" for i in range(nodenum)],
        "类型": ["Shadowsocks" for _ in range(nodenum)],
        "HTTP(S)延迟": [str(int(i.label)) + "ms" for i in koicfg.image.color.delay[:nodenum]],
        "Netflix": tips[:nodenum],
        "Youtube": tips[:nodenum-1] + ["待解锁"],
        "平均速度": [str(i.label) + "MB" for i in koicfg.image.color.speed],
        "最大速度": [str(i.label + randint(0, 100) * randint(1, 10)) + "MB" for i in koicfg.image.color.speed],
        "每秒速度": a,
        "消耗流量": 4096,
        "线程": 4
    }
    kd = KoiDraw('节点名称', test_result, koicfg)
    kd.draw(debug=True)


if __name__ == "__main__":
    import os
    os.chdir("..")
    print(os.getcwd())
    from utils.export import KoiDraw
    from utils.types.config import KoiConfig
    test()
