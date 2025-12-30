---
description: 此配置下，会影响一些bot的网络通讯行为
---

# network

```yaml
network: # 网络
  httpProxy: "http://host:port" # http代理，如果设置的话，bot会用这个拉取订阅
  socks5Proxy: "socks5://host:port" # socks5代理， bot的代理在下面bot那一栏填
  userAgent: "ClashMetaForAndroid/2.8.9.Meta Mihomo/0.16" # UA设置，影响订阅获取
```

## network.userAgent

{% tabs %}
{% tab title="解释" %}
1. 自定义内部程序部分请求头的user-agent字段
{% endtab %}

{% tab title="特性" %}
1. 类型：str
2. 此配置影响拉取订阅时的UA
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
network: # 网络配置
  userAgent: "ClashMetaForAndroid/2.8.9.Meta Mihomo/0.16" # UA设置，影响订阅获取
```
{% endcode %}
{% endtab %}
{% endtabs %}

此项配置会覆写bot内部拉取订阅时设置的user-agent，它是HTTP请求头的一部分。





## 关于订阅拉取

一种名为机场（跨境网络代理提供商）的存在，可以让你获取到http协议的url。它的用户面板（如V2board、Xboard、SSPanel）等会根据HTTP客户端的请求头下发对应的订阅格式。

koipy仅支持解析Clash订阅格式，它是基于yaml的配置。

但有时候，koipy内部自带的请求头不能获取到正确的订阅，可以通过修改请求头中的user-agent进行适配。或者试图用来绕过针对UA获取订阅的封锁。
