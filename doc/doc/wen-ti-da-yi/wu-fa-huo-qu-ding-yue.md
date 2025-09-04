# 无法获取订阅

如果你遇到以下情况：

<figure><img src="../../.gitbook/assets/image (17).png" alt=""><figcaption></figcaption></figure>

是因为koipy仅**原生支持**Clash配置格式的订阅文件

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

### 在Telegram回复一个配置文件下载

示例：

<figure><img src="../../.gitbook/assets/image (15).png" alt=""><figcaption></figcaption></figure>

## 订阅解析

koipy bot会将内容遵循yaml格式进行解析，并仅读取里面的 proxies 字段



## 订阅转换

虽然koipy仅原生支持Clash配置，但可以通过外部第三方的订阅转换应用，把通用URI格式转换成Clash配置。

目前，koipy适配了以下订阅转换服务：

* subconverter [详情](https://github.com/tindy2013/subconverter)
* Sub-Store [详情](https://github.com/sub-store-org/Sub-Store)

使用方式，请参阅koipy的配置文件，配置好订阅转换后，就可以实现以下效果：

<figure><img src="../../.gitbook/assets/image (16).png" alt=""><figcaption><p>启用订阅转换后可支持URI通用格式的测试</p></figcaption></figure>

### 订阅转换注意事项



{% tabs %}
{% tab title="First Tab" %}
⚠️应该知晓，转换后的配置文件可能不是百分百正确，出现节点不通，请首先检查转换前后是否缺漏
{% endtab %}
{% endtabs %}
