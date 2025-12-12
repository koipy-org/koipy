---
description: 此配置涉及测试时的后端脚本配置
---

# scriptConfig

## 概要

后端一般不存储脚本，所有的脚本文件都存放主端bot，在测试的时候根据你选择测的选项实时分发对应的脚本



## 配置脚本

### scriptConfig.script

scriptConfig.scripts 是一个数组，它的每一项都是一个具体脚本

正常的配置一个新的脚本如下:

```yaml
scriptConfig:
  scripts: # 脚本载入
    - type: gofunc # 表示是miaospeed的内置实现
      name: "TEST_PING_RTT" # 特殊保留名称，当设置为这些特殊保留值时会覆写程序内部的默认配置，更多的特殊保留值请参阅这里: https://github.com/airportr/miaospeed/blob/master/interfaces/matrix.go#L3
      rank: -100 # 排序
      content: "你的脚本内容或者一个文件路径"
    - type: gojajs
      name: "Youtube"
      rank: 0
      content: "resources/scripts/builtin/youtube.js" # 也可以指定一个文件路径
```

### scriptConfig.script\[0].type

可用值:&#x20;

* gojajs 表示这是miaospeed的支持的javascript脚本引擎类型，更多解释请前往文档编写miaospeed脚本页面
* gofunc 表示这个脚本是miaospeed内部用Go语言实现的，仅能更改在主端的行为，例外排序等

### scriptConfig.script\[0].name

如果是gojajs脚本类型，则可以写保留名字外的任意字符串

### scriptConfig.script\[0].rank

脚本返回给bot的内容在绘图上显示的相对位置排序，值是整数，默认值为1，数字越小越排在前面。

### scriptConfig.script\[0].content

你可以直接填脚本里面的文件内容，也可以填一个文件路径

## 脚本预保留名称

以下这些字符串为bot的预保留脚本名称，当你使用这些预保留名称作为脚本名称时，会覆写内部程序的预留配置。

| 测试项                     | 描述                          |
| ----------------------- | --------------------------- |
| `TEST_PING_RTT`         | TCP RTT（数据交换延迟测试）           |
| `TEST_PING_CONN`        | HTTP 请求体感延迟测试               |
| `GEOIP_INBOUND`         | 入口拓扑测试（地理IP路径分析）            |
| `GEOIP_OUTBOUND`        | 出口拓扑测试（地理IP路径分析）            |
| `SPEED_AVERAGE`         | 平均下行速度                      |
| `SPEED_MAX`             | 最大下行速度                      |
| `SPEED_PER_SECOND`      | 每秒下行速度                      |
| `UDP_TYPE`              | UDP行为发现                     |
| `TEST_PING_MAX_CONN`    | HTTP请求体感最大延迟                |
| `TEST_PING_MAX_RTT`     | 最大RTT（往返时延峰值）               |
| `TEST_PING_TOTAL_CONN`  | 总HTTP请求延迟（所有请求的累计值）         |
| `TEST_PING_TOTAL_RTT`   | 总RTT（所有数据包往返时延总和）           |
| `TEST_PING_SD_RTT`      | RTT标准差（延迟波动指标）              |
| `TEST_PING_SD_CONN`     | HTTP请求延迟标准差（访问网页稳定性）        |
| `TEST_PING_PACKET_LOSS` | RTT丢包率（数据包丢失百分比）            |
| `TEST_HTTP_CODE`        | 目标PING地址的HTTP状态码（如200、404等） |
| `USPEED_AVERGE`         | 平均上行速度                      |
| `USPEED_MAX`            | 最大上行速度                      |
| `USPEED_PER_SECOND`     | 每秒上行速度                      |
| `TEST_HIJACK_DETECTION` | 测速劫持检测                      |





## 特殊脚本配置

在预保留名称中，只有 GEOIP\_INBOUND 和 GEOIP\_OUTBOUND 可以被覆写content值。

因此你可以覆写在bot程序内部的默认GEOIP脚本:

```yaml
    - type: gojajs
      name: "GEOIP_INBOUND"
      rank: 0
      content: "YOUR_GEOIP_SCRIPT" # 默认的GEOIP脚本参见 https://github.com/AirportR/miaospeed/blob/master/engine/embeded/default_geoip.js
```

