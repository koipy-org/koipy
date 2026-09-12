---
description: 测试梦开始的地方
---

# /test

## 解释

构建并发起一次测试任务

## 用法

### 用法1：

```
/test <订阅链接> <包含过滤器:可选> <排除过滤器:可选>
```

### 用法2：

```
/test <规则名> <包含过滤器:可选> <排除过滤器:可选>
```

### 用法3：加入指令参数

```
/test?s=local&sort=订阅原序 <订阅链接> <包含过滤器:可选> <排除过滤器:可选>
```

### 用法4

可以回复一个订阅链接进行测试，如图：

![](../../.gitbook/assets/image%20%2823%29.png)

### 用法5:

回复一个文件进行测试，如图：

![](../../.gitbook/assets/image%20%2824%29.png)

### 用法6:

同时也支持通过引用一条消息/文件进行测试：

![](../../.gitbook/assets/image%20%2825%29.png)

![](../../.gitbook/assets/image%20%2826%29.png)

![](../../.gitbook/assets/image%20%2827%29.png)

![](../../.gitbook/assets/image%20%2828%29.png)

## 位置参数

* `<订阅链接>`：输入一个 HTTP 前缀的 URL，例：https://www.google.com
* `<规则名>`：输入一个规则名，什么是规则请查看：

{% content-ref url="../guan-yu-gui-ze/" %}
[guan-yu-gui-ze](../guan-yu-gui-ze/)
{% endcontent-ref %}

* `<包含过滤器>`：过滤订阅里的节点，选择仅测试部分节点，支持正则关键字
* `<排除过滤器>`：过滤订阅里的节点，选择排除部分节点，支持正则关键字
* 过滤器是先包含，再排除

🎗️提示

* 如果你是通过回复或引用消息、文件发起测试，想要使用过滤器，那么第一个参数（本该是订阅链接或规则）可以用任意字符代替，但不能留空，koipy 不会读取它。

## 测试项按钮

进入测试项选择页面后，除了常规的延迟、速度、流媒体解锁项之外，还有一些值得单独说明的按钮：

* **🕵️‍♂️ 劫持检测**：快速发起「测速劫持检测」。对应内置测试项 `TEST_HIJACK_DETECTION`，它不经过 js 脚本的 macro 兼容层，由 koipy 直接使用 miaospeed 的原生 macro 接口，因此需要 miaospeed 后端版本 > 4.6.2。
* **上行测试**：v1.12.0 起，`/test` 的测试项里可以选择上行测试，但需要后端把 `option.apiVersion` 写成 `3` 才会真正生效。

## 同族指令

`/test` 是通用入口，bot 还内置了几个带默认测试项的同族指令，用来省去挑选项的步骤：

| 指令 | 说明 |
| --- | --- |
| `/test` | 完整测试，测试项由你自己勾选 |
| `/speed` | 下行速度测试，默认勾选延迟与下行速度项 |
| `/uspeed` | 上行速度测试，默认勾选延迟与上行速度项 |
| `/topo` | 拓扑测试，等价于 `/analyze`，默认勾选入口与出口分析项 |

它们的用法、位置参数与指令参数与 `/test` 完全一致。

{% content-ref url="speed.md" %}
[speed.md](speed.md)
{% endcontent-ref %}

{% content-ref url="uspeed.md" %}
[uspeed.md](uspeed.md)
{% endcontent-ref %}

{% content-ref url="topo.md" %}
[topo.md](topo.md)
{% endcontent-ref %}

## 指令参数

详见：

{% content-ref url="zhi-ling-can-shu.md" %}
[zhi-ling-can-shu.md](zhi-ling-can-shu.md)
{% endcontent-ref %}
