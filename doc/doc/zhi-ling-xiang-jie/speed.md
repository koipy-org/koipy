---
description: 下行速度测试
---

# /speed

## 解释

构建并发起一次下行速度测试任务。

`/speed` 与 `/test` 共用同一套任务构建流程，区别在于它内置了一套默认勾选的测试项，省去手动挑选的步骤。

## 用法

### 用法1：

```
/speed <订阅链接> <包含过滤器:可选> <排除过滤器:可选>
```

### 用法2：

```
/speed <规则名> <包含过滤器:可选> <排除过滤器:可选>
```

### 用法3：加入指令参数

```
/speed?s=local&sort=订阅原序 <订阅链接> <包含过滤器:可选> <排除过滤器:可选>
```

### 用法4

回复或引用一条消息、文件发起测试，与 `/test` 一致。

## 位置参数

与 `/test` 相同：

* `<订阅链接>`：输入一个 HTTP 前缀的 URL
* `<规则名>`：输入一个规则名
* `<包含过滤器>`：过滤订阅里的节点，选择仅测试部分节点，支持正则关键字
* `<排除过滤器>`：过滤订阅里的节点，选择排除部分节点，支持正则关键字

## 内置测试项

`/speed` 会默认勾选以下测试项：

| 测试项 | 描述 |
| --- | --- |
| `TEST_PING_RTT` | TCP RTT（数据交换延迟测试） |
| `TEST_PING_CONN` | HTTP 请求体感延迟测试 |
| `SPEED_AVERAGE` | 平均下行传输速度 |
| `SPEED_MAX` | 最大下行传输速度 |
| `SPEED_PER_SECOND` | 每秒实时下行传输速度 |
| `UDP_TYPE` | UDP 协议过滤行为 / UDP 端口通断测试 |

## 特性

* 内置测试项只是默认勾选，你依然可以在选择页面里自行增删。
* 如果后端或规则里已经指定了测试项，则会以规则里的配置为准。
* 需要测试上行速度请使用 `/uspeed`。
* 测试项的具体含义参阅：

{% content-ref url="../pei-zhi-xiang-jie/scriptconfig.md" %}
[scriptconfig.md](../pei-zhi-xiang-jie/scriptconfig.md)
{% endcontent-ref %}

## 指令参数

详见：

{% content-ref url="zhi-ling-can-shu.md" %}
[zhi-ling-can-shu.md](zhi-ling-can-shu.md)
{% endcontent-ref %}
