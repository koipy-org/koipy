# 关于连通性测试

本章将讲解连通性测试的细节

## PING测试

ping测试入口如图所示

<figure><img src="../../.gitbook/assets/image (14).png" alt=""><figcaption></figcaption></figure>

### 测试项详情：

请记住，上图点击后开测的按钮本质上都是规则的自动填充，所以你可以自己建立规则，实现上面按钮实现的效果。

以下是所有koipy目前支持的内置测试项，大部分均为gofunc类型（除了GEOIP\_INBOUND和GEOIP\_OUBOUND），即miaospeed用golang自主实现的测试类型。

| 测试项                     | 描述                      |
| ----------------------- | ----------------------- |
| `TEST_PING_RTT`         | TCP RTT（数据交换延迟测试）       |
| `TEST_PING_CONN`        | HTTP 请求体感延迟测试           |
| `GEOIP_INBOUND`         | 入口拓扑测试（地理IP路径分析）        |
| `GEOIP_OUTBOUND`        | 出口拓扑测试（地理IP路径分析）        |
| `SPEED_AVERAGE`         | 平均下行传输速度                |
| `SPEED_MAX`             | 最大下行传输速度                |
| `SPEED_PER_SECOND`      | 每秒实时下行传输速度              |
| `UDP_TYPE`              | UDP协议过滤行为/UDP端口通断测试     |
| `TEST_PING_MAX_CONN`    | HTTP请求体感最大延迟            |
| `TEST_PING_MAX_RTT`     | 最大RTT（往返时延峰值）           |
| `TEST_PING_TOTAL_CONN`  | 总HTTP请求延迟（所有请求的累计值）     |
| `TEST_PING_TOTAL_RTT`   | 总RTT（所有数据包往返时延总和）       |
| `TEST_PING_SD_RTT`      | RTT标准差（延迟波动指标）          |
| `TEST_PING_SD_CONN`     | HTTP请求延迟标准差（稳定性分析）      |
| `TEST_PING_PACKET_LOSS` | RTT丢包率（数据包丢失百分比）        |
| `TEST_HTTP_CODE`        | 目标地址的HTTP状态码（如200、404等） |



### 详细解释

* `TEST_PING_RTT`

> ### 结果表现
>
> 在结果图显示为 延迟RTT或者TLS RTT（未来将弃用此名称，出于历史原因），这里的RTT 一般指TCP的RTT，如果是hysteria等基于UDP的协议，则以此类推，所以图片上不写TCP RTT就是这个原因。
>
> ### 用处
>
> 用来衡量一个后端到代理节点的数据交互速度，单位ms（毫秒），越小说明代理节点的连通性越好，在一些场景（如打游戏，实时聊天）体验更好。
>
> 另外，目前中国大陆到美国的物理延迟超过100ms，所以你要是看到一个美国节点的RTT<100，那几乎是假的结果了。
>
> 特殊说明：VLESS协议有时候测不准，会显示个位数延迟
>
> ### 算法
>
> 实现RTT的算法请参阅miaospeed源码：
>
> [https://github.com/AirportR/miaospeed/blob/master/service/macros/ping/ping.go](https://github.com/AirportR/miaospeed/blob/master/service/macros/ping/ping.go)
>
> ⚠️注意
>
> RTT算法实现和其他miaospeed分支有所不同，所以仅代表本项目维护的分支做出解释
>
> ### TLS RTT
>
> 有时候图片会显示此名称，意味着配置里pingURL是https开头的，koipy默认给所有未配置ping地址的后端一个缺省值：
>
> &#x20;https://cp.cloudflare.com/generate\_204
>
> TLS RTT是一个历史遗留名称，它的解释**根据源码中的算法解释为：**
>
> 经过TLS 握手成功后，单次数据的交换延迟，所以**本质上依旧是延迟RTT，** 很多人误以为这里是指TLS握手延迟，其实不是（包括原版miaospeed及未改动这部分源码的所有下游分支）。
>
> 至于为什么是这个名称，个人猜测是如果TLS握手失败，说明有ping地址的延迟劫持，这是一些代理提供商的造假手段之一，取这个名字可能给予用户一定的“安全感”（实际笔者并不感冒），现如今此名称造成的误解太多。为了确保表述严谨，未来将弃用此名称展示。

* `TEST_PING_CONN`

> ### 结果表现
>
> 此测试项在图片中显示为“HTTP延迟”或“HTTPS延迟”，取决于pingURL配置开头是否是“https://”
>
> ### 用处
>
> 测量访问网页的请求体感延迟，与延迟RTT区别就是，它计算了协议的延迟，沿用mihomo的说法，就是未开启统一延迟的URLTest
>
> ### 算法
>
> 算法参见源码，此项结果大约为2倍\~3倍的延迟RTT
>
>

