---
description: 切换语言包
---

# /lang

## 解释

切换 bot 当前使用的语言包。

## 用法

```
/lang
```

## 特性

* `/lang` 需要**管理员权限**。
* bot 会列出 `translation.resources` 里所有可用的语言键，每个键一个按钮。
* 点击按钮后，bot 会把 `translation.lang` 改成对应的键，并提示你保存配置。
* 语言包文件加载失败时会静默跳过，不会导致 bot 启动失败。
* 切换语言后，绘制图片、信息显示与控制台输出都会跟着变。
* 语言包支持在文本里写颜色代码，用来给按钮着色。

## 相关配置

::: tip 相关内容

[translation](/doc/pei-zhi-xiang-jie/translation)

:::


## 相关页面

::: tip 相关内容

[语言包](/doc/yu-yan-bao/)

:::


::: tip 相关内容

[制作语言包](/doc/yu-yan-bao/zhi-zuo-yu-yan-bao)

:::

