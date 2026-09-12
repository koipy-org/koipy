---
description: 上行速度测试
---

# /uspeed

## 解释

构建并发起一次上行速度测试任务。

上行速度测试是 v1.12.0 起实验性加入的能力，需要后端侧同步支持，具体见下面的「前提」一节。

## 用法

### 用法1：

```
/uspeed <订阅链接> <包含过滤器:可选> <排除过滤器:可选>
```

### 用法2：

```
/uspeed <规则名> <包含过滤器:可选> <排除过滤器:可选>
```

### 用法3：加入指令参数

```
/uspeed?s=local&sort=订阅原序 <订阅链接>
```

### 用法4

回复或引用一条消息、文件发起测试，与 `/test` 一致。

## 位置参数

与 `/test` 相同，详见：

{% content-ref url="test.md" %}
[test.md](test.md)
{% endcontent-ref %}

## 内置测试项

`/uspeed` 会默认勾选以下测试项：

| 测试项 | 描述 |
| --- | --- |
| `TEST_PING_RTT` | TCP RTT（数据交换延迟测试） |
| `TEST_PING_CONN` | HTTP 请求体感延迟测试 |
| `USPEED_AVERAGE` | 平均上行速度 |
| `USPEED_MAX` | 最大上行速度 |
| `USPEED_PER_SECOND` | 每秒上行速度 |
| `UDP_TYPE` | UDP 协议过滤行为 / UDP 端口通断测试 |

## 前提

上行测速需要后端配合，缺一不可：

1. 后端的 miaospeed 版本需要支持上行测速（v4.6.1 起提供）
2. 后端启动时需要显式加上 `-upload` 参数，否则上行测速默认关闭
3. 后端配置里需要把 `option.apiVersion` 显式写成 `3`，上行测速字段才会被真正发送给后端

关于第 3 点，可以这样配置：

```yaml
slaveConfig:
  slaves:
    - type: miaospeed
      id: "upload-test"
      token: "secret"
      address: "127.0.0.1:8765"
      option:
        apiVersion: 3
        uploadURL: "https://speed.cloudflare.com/__up"
        uploadDuration: 8
        uploadThreading: 4
```

{% hint style="warning" %}
当 `apiVersion` 为 `0`、`1` 或 `2` 时，上行测速相关字段会在请求构造阶段被裁掉，后端根本收不到，此时 `/uspeed` 不会给出预期的结果。
{% endhint %}

## 特性

* 绘图结果的页脚里，上下行线程会分开显示。
* 目前上行测试的效果不太理想，加上很少人反馈bug，所以测试结果不太准确，未来可能需要重新实现
* 后端与规则的详细配置参阅：

{% content-ref url="../pei-zhi-xiang-jie/slaveconfig.md" %}
[slaveconfig.md](../pei-zhi-xiang-jie/slaveconfig.md)
{% endcontent-ref %}

## 指令参数

详见：

{% content-ref url="zhi-ling-can-shu.md" %}
[zhi-ling-can-shu.md](zhi-ling-can-shu.md)
{% endcontent-ref %}
