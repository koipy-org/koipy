# 无法获取订阅

如果你遇到以下情况：

![](../../.gitbook/assets/image%20%2817%29.png)

通常是因为 koipy 仅**原生支持** Clash 配置格式的订阅文件。

## 什么是Clash配置文件

请参考：

{% embed url="https://clash.wiki/configuration/introduction.html" %}

{% embed url="https://wiki.metacubex.one/config/proxies/" %}

## 获取方式

### 通过HTTP URL下载

示例：

```
https://www.google.com
```

### 在 Telegram 回复一个配置文件下载

示例：

![](../../.gitbook/assets/image%20%2815%29.png)

## 订阅解析

koipy bot 会按 YAML 格式解析内容，并仅读取其中的 `proxies` 字段。

## 订阅转换

虽然 koipy 仅原生支持 Clash 配置，但可以通过第三方订阅转换应用，把通用 URI 格式转换成 Clash 配置。

目前，koipy适配了以下订阅转换服务：

* subconverter [详情](https://github.com/tindy2013/subconverter)
* Sub-Store [详情](https://github.com/sub-store-org/Sub-Store)

使用方式请参阅 koipy 的配置文件。配置好订阅转换后，就可以实现以下效果：

![](../../.gitbook/assets/image%20%2816%29.png)

### 订阅转换注意事项



{% hint style="warning" %}
转换后的配置文件可能不是百分百正确。如果出现节点不通，请先检查转换前后是否有缺漏。
{% endhint %}
