---
description: 这里的配置用于定义 koipy 可调用的测速后端。
---

# slaveConfig

这一页说明后端配置。`slaveConfig` 决定 bot 能连到哪些后端、后端在前端如何展示，以及每个后端默认用什么测速参数。

<details>

<summary>slaveConfig</summary>

{% code expandable="true" %}
```yaml
slaveConfig:
  healthCheck:
    numSamples: 10
    showStatusStyle: "default"
    autoHideOnFailure: false
  showID: true
  speedScheduling: pipeline
  geoClustering: true
  slaves:
    - type: miaospeed
      id: "localmiaospeed"
      token: "ZfffaQ4/E-7S"
      address: "127.0.0.1:8765"
      path: "/"
      skipCertVerify: true
      tls: true
      invoker: "1114514"
      buildtoken: ""
      comment: "本地 miaospeed 后端"
      hidden: false
      option:
        downloadDuration: 8
        downloadThreading: 4
        downloadURL: "https://dl.google.com/dl/android/studio/install/3.4.1.0/android-studio-ide-183.5522156-windows.exe"
        pingAddress: "https://cp.cloudflare.com/generate_204"
        pingAverageOver: 5
        stunURL: "udp://stunserver2025.stunprotocol.org:3478"
        taskRetry: 3
        taskTimeout: 5000
        dnsServer: []
        apiVersion: 1
        uploadURL: "https://speed.cloudflare.com/__up"
        uploadDuration: 8
        uploadThreading: 4
```
{% endcode %}

</details>

{% hint style="warning" %}
当前主线配置应以 `miaospeed` 后端为准。源码仍保留 `fulltclash` 的历史兼容分支，但新配置不建议围绕它展开。
{% endhint %}

## slaveConfig.healthCheck

{% tabs %}
{% tab title="解释" %}
1. 这是 `/checkslave` 和后端选择页的健康检查展示配置。
2. 它的作用更偏向“展示和筛选”，不是一个严格的熔断器。
3. 只有在程序拿到了后端健康检查结果后，这里的状态前缀、自动隐藏等设置才会体现出来。
{% endtab %}

{% tab title="特性" %}
1. 类型：`dict`
2. 子项包括：`numSamples`、`showStatusStyle`、`autoHideOnFailure`
3. 它不会改写后端真实连接参数，只影响检查结果的展示方式。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
slaveConfig:
  healthCheck:
    numSamples: 10
    showStatusStyle: "emoji"
    autoHideOnFailure: true
```
{% endcode %}
{% endtab %}
{% endtabs %}

## slaveConfig.healthCheck.numSamples

{% tabs %}
{% tab title="解释" %}
1. 这是健康检查时的采样次数。
2. 当前 `/checkslave` 会按这个值对后端做多次探测，再生成平均结果和状态。
3. 采样次数越大，结果通常越稳，但检查也会更慢。
{% endtab %}

{% tab title="特性" %}
1. 类型：`int`
2. 默认值：`10`
3. 这项只影响健康检查，不会改变正式测速任务的线程数或测速时长。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
slaveConfig:
  healthCheck:
    numSamples: 5
```
{% endcode %}
{% endtab %}
{% endtabs %}

## slaveConfig.healthCheck.showStatusStyle

{% tabs %}
{% tab title="解释" %}
1. 这项配置决定后端选择页里如何展示健康检查状态。
2. `default` 表示不额外加前缀。
3. `number` 会在备注前面加上类似 `(23ms)` 的延迟数字。
4. `emoji` 会在备注前面加上状态 emoji。
{% endtab %}

{% tab title="特性" %}
1. 类型：`str`
2. 默认值：`default`
3. 当前稳定可用值：`default`、`number`、`emoji`
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
slaveConfig:
  healthCheck:
    showStatusStyle: "number"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## slaveConfig.healthCheck.autoHideOnFailure

{% tabs %}
{% tab title="解释" %}
1. 这项配置用于在健康检查结果异常时自动隐藏后端。
2. 当前逻辑会在状态为 `DEAD` 或 `INVALID` 时把该后端标记为隐藏。
3. 隐藏后，它不会出现在基于健康检查结果构造出来的后端列表中。
{% endtab %}

{% tab title="特性" %}
1. 类型：`bool`
2. 默认值：`false`
3. 它是“检查结果视图”层面的自动隐藏，不是永久删除配置。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
slaveConfig:
  healthCheck:
    autoHideOnFailure: true
```
{% endcode %}
{% endtab %}
{% endtabs %}

## slaveConfig.showID

{% tabs %}
{% tab title="解释" %}
1. 这项配置决定后端选择页里是否把后端 `id` 追加到备注尾部。
2. 当前实现的展示形式是：`comment(id)`。
3. 它适合在后端很多、备注名接近时帮助你快速区分。
{% endtab %}

{% tab title="特性" %}
1. 类型：`bool`
2. 默认值：`true`
3. 它只影响显示文本，不影响后端真实 `id`、鉴权或任务执行。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
slaveConfig:
  showID: false
```
{% endcode %}
{% endtab %}
{% endtabs %}

## slaveConfig.speedScheduling

{% tabs %}
{% tab title="解释" %}
1. 这项配置控制koipy在“多后端联测”是如何进行后端调度。
2. `pipeline` 表示错峰流水线模式：后一个后端会在前一个后端完成第一个节点后启动。
3. `sequential` 表示严格串行模式：后一个后端要等前一个后端全部完成后才启动。
4. 当前实现里，除了这两个值之外，其它值都不会启用调度门控，效果等价于“所有后端同时开始”。
{% endtab %}

{% tab title="特性" %}
1. 类型：`str`
2. 默认值：`pipeline`
3. 它只在“含测速项的多后端任务”里生效，普通连通性或单后端任务基本感受不到。
4. 模板里常见的 `concurrent` 是约定值。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
slaveConfig:
  speedScheduling: sequential
```
{% endcode %}
{% endtab %}
{% endtabs %}

## slaveConfig.geoClustering

{% tabs %}
{% tab title="解释" %}
1. 这项配置用于控制多后端拓扑结果是否做聚类排序。
2. 开启后，结果相同或相近的后端会尽量排到一起，方便单元格合并和阅读。
3. 它只作用于 GEO / 拓扑类合并结果，不影响普通测速图。
{% endtab %}

{% tab title="特性" %}
1. 类型：`bool`
2. 默认值：`true`
3. 关闭后，拓扑合并结果更接近原始后端顺序。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
slaveConfig:
  geoClustering: false
```
{% endcode %}
{% endtab %}
{% endtabs %}

## slaveConfig.slaves

{% tabs %}
{% tab title="解释" %}
1. 这是后端列表本体，每一项都是一个后端定义。
2. bot 能调用哪些后端，取决于这里最终加载出来的条目。
3. 当前实现会在加载时识别重复 `id`：如果同 `id` 且同类型已存在，就会更新已有条目，而不是盲目追加。
4. 未识别的 `type` 会被直接忽略。
{% endtab %}

{% tab title="特性" %}
1. 类型：`list[Slave]`
2. 当前主流条目类型是 `miaospeed`
3. 后端是否“可用”，至少还取决于 `id`、`type`、`address`、`token` 这些关键字段是否完整。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
slaveConfig:
  slaves:
    - type: miaospeed
      id: "hk-1"
      token: "secret-1"
      address: "10.0.0.11:8765"
    - type: miaospeed
      id: "us-1"
      token: "secret-2"
      address: "10.0.0.12:8765"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## slaveConfig.slaves[n].type

{% tabs %}
{% tab title="解释" %}
1. 这项配置决定后端条目按哪种协议类型解释。
2. 当前文档应以 `miaospeed` 为准，它对应主流的 MiaoSpeed WebSocket 后端。
3. 源码里还兼容历史值 `fulltclash`，但不建议新配置继续依赖它。
{% endtab %}

{% tab title="特性" %}
1. 类型：`str`
2. 推荐值：`miaospeed`
3. 未识别值会在加载时被跳过。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
slaveConfig:
  slaves:
    - type: miaospeed
      id: "localmiaospeed"
      token: "secret"
      address: "127.0.0.1:8765"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## slaveConfig.slaves[n].id / token

{% tabs %}
{% tab title="解释" %}
1. `id` 是后端的稳定标识，也是 `rules[].slaveid` 要引用的名字。
2. `token` 是 bot 连接这个后端时使用的共享鉴权密钥。
3. 对当前实现来说，`id`、`type`、`address`、`token` 都是后端“准备就绪”的关键字段。
{% endtab %}

{% tab title="特性" %}
1. 类型：`str`
2. `id` 建议全局唯一，避免重复合并时覆盖到不该覆盖的条目。
3. `token` 为空时，后端条目通常无法正常参与连接。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
slaveConfig:
  slaves:
    - type: miaospeed
      id: "jp-1"
      token: "replace-with-your-token"
      address: "10.0.0.20:8765"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## slaveConfig.slaves[n].address / path / tls / skipCertVerify

{% tabs %}
{% tab title="解释" %}
1. 这几项共同决定 bot 如何连接到后端。
2. `address` 负责主机和端口，当前实现按 `host:port` 解析。
3. `path` 是 WebSocket 路径；留空时会退回到 `/`。
4. `tls=true` 时走加密连接；`skipCertVerify=true` 时会接受自签证书。
{% endtab %}

{% tab title="特性" %}
1. 类型：`str` + `bool`
2. `tls=true` 且 `skipCertVerify=false` 时，更适合搭配受信任证书。
3. 如果 `path` 不正确，即使地址和 token 正确，也无法成功握手。
4. 对公网后端来说，给 `path` 设置一个不那么显眼的随机路径更合适。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
slaveConfig:
  slaves:
    - type: miaospeed
      id: "remote-1"
      token: "secret"
      address: "backend.example.com:443"
      path: "/koipy/ws"
      tls: true
      skipCertVerify: false
```
{% endcode %}
{% endtab %}
{% endtabs %}

## slaveConfig.slaves[n].invoker / buildtoken

{% tabs %}
{% tab title="解释" %}
1. 这两项属于发给后端的附加身份字段。
2. `invoker` 为空时，当前实现会回退到 bot 自己的身份信息。
3. `buildtoken` 为空时，koipy会回退到内置默认值。
4. 只有在你明确知道目标后端分支有额外约束时，才需要改它们。
{% endtab %}

{% tab title="特性" %}
1. 类型：`str`
2. 日常主线使用里，通常保留默认或留空即可。
3. `buildtoken` 改错时，会导致与特定后端分支之间的签名或兼容性问题。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
slaveConfig:
  slaves:
    - type: miaospeed
      id: "localmiaospeed"
      token: "secret"
      address: "127.0.0.1:8765"
      invoker: "koipy-main"
      buildtoken: ""
```
{% endcode %}
{% endtab %}
{% endtabs %}

## slaveConfig.slaves[n].comment / hidden / proxy

{% tabs %}
{% tab title="解释" %}
1. `comment` 是后端备注名，会显示在 bot 的后端选择界面中。
2. `hidden=true` 时，这个后端会在常规选择列表里被隐藏。
3. `proxy` 是给“连接后端这件事”单独指定的代理。
4. 当前koipy只会实际使用 `http` 代理，其他代理协议即使写了也不一定生效（请让开发者适配更多协议）。
{% endtab %}

{% tab title="特性" %}
1. 类型：`str` + `bool`
2. `comment` 为空也能运行，但可读性会明显下降。
3. 如果全局 `showID=true`，最终展示文本会变成 `comment(id)`。
4. `hidden` 只是隐藏，不等于删除配置。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
slaveConfig:
  slaves:
    - type: miaospeed
      id: "us-1"
      token: "secret"
      address: "10.0.0.12:8765"
      comment: "美国测速后端"
      hidden: false
      proxy: "http://proxy.example.com:7890"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## slaveConfig.slaves[n].option

{% tabs %}
{% tab title="解释" %}
1. 这是后端默认测速参数集合。
2. 它更像“后端默认档位”，并不是所有任务都会原封不动照抄。
3. 当前实现里，`runtime.speedThreads`、`runtime.pingURL`、`runtime.duration`、`runtime.stunURL`、`runtime.enableDNSInject` 都可能在单次任务里覆写这里的一部分值。
4. `runtime.speedFiles` 只有在 `downloadURL="DYNAMIC:ALL"` 时才会参与覆写。
{% endtab %}

{% tab title="特性" %}
1. 类型：`dict`
2. 如果这里的值不符合后端请求校验范围，任务会在真正开测前直接报错。
3. 更细的运行时覆写规则，建议同时看 `runtime` 页。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
slaveConfig:
  slaves:
    - type: miaospeed
      id: "localmiaospeed"
      token: "secret"
      address: "127.0.0.1:8765"
      option:
        downloadDuration: 8
        downloadThreading: 4
        pingAddress: "https://cp.cloudflare.com/generate_204"
```
{% endcode %}
{% endtab %}
{% endtabs %}

{% content-ref url="runtime.md" %}
[runtime.md](runtime.md)
{% endcontent-ref %}

## slaveConfig.slaves[n].option.downloadDuration / downloadThreading

{% tabs %}
{% tab title="解释" %}
1. `downloadDuration` 是下行测速持续时间。
2. `downloadThreading` 是下行测速线程数，也就是后端压测强度。
3. 线程越高不一定越准，对低配后端或高倍率节点反而可能更失真。
{% endtab %}

{% tab title="特性" %}
1. 类型：`int`
2. 默认值：`8` 秒、`4` 线程
3. 当前校验范围：`downloadDuration=1~120`，`downloadThreading=1~64`
4. 单次任务里，`runtime.duration` 和 `runtime.speedThreads` 可以覆写它们。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
slaveConfig:
  slaves:
    - type: miaospeed
      id: "speed-1"
      token: "secret"
      address: "127.0.0.1:8765"
      option:
        downloadDuration: 15
        downloadThreading: 8
```
{% endcode %}
{% endtab %}
{% endtabs %}

## slaveConfig.slaves[n].option.downloadURL

{% tabs %}
{% tab title="解释" %}
1. 这是下行测速使用的大文件地址。
2. 你可以写固定 URL，也可以写特殊值 `DYNAMIC:ALL`。
3. 只有写成 `DYNAMIC:ALL` 时，后端才会从 `runtime.speedFiles` 中随机挑一个真实测速文件地址。
{% endtab %}

{% tab title="特性" %}
1. 类型：`str`
2. 默认值是 Android Studio 安装包地址
3. 当 `apiVersion=2` 时，`DYNAMIC:ALL` 当前不被支持，会直接触发校验错误。
4. 如果你希望不同任务动态切换测速文件，这一项就不要写死成固定 URL。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
slaveConfig:
  slaves:
    - type: miaospeed
      id: "dynamic-file"
      token: "secret"
      address: "127.0.0.1:8765"
      option:
        downloadURL: "DYNAMIC:ALL"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## slaveConfig.slaves[n].option.pingAddress / pingAverageOver

{% tabs %}
{% tab title="解释" %}
1. `pingAddress` 是延迟测试地址。
2. `pingAverageOver` 是延迟测试取样次数，用来计算平均结果。
3. `pingAddress` 更偏向“测什么地址的连通性”，`pingAverageOver` 更偏向“结果要多平滑”。
{% endtab %}

{% tab title="特性" %}
1. 类型：`str` + `int`
2. 默认值：`https://cp.cloudflare.com/generate_204`、`5`
3. `pingAverageOver` 当前校验范围是 `1~999`
4. 单次任务里的 `runtime.pingURL` 可以覆写 `pingAddress`
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
slaveConfig:
  slaves:
    - type: miaospeed
      id: "cf-ping"
      token: "secret"
      address: "127.0.0.1:8765"
      option:
        pingAddress: "https://cp.cloudflare.com/generate_204"
        pingAverageOver: 5
```
{% endcode %}
{% endtab %}
{% endtabs %}

## slaveConfig.slaves[n].option.stunURL

{% tabs %}
{% tab title="解释" %}
1. 这是 UDP / STUN 探测时使用的目标地址。
2. 它主要影响 UDP 通断或 NAT 行为相关测试。
3. 如果你的网络环境对某个公共 STUN 服务器不友好，可以换一个更稳定的。
{% endtab %}

{% tab title="特性" %}
1. 类型：`str`
2. 默认值：`udp://stunserver2025.stunprotocol.org:3478`
3. 推荐写成 `udp://host:port`
4. 单次任务里的 `runtime.stunURL` 可以覆写它。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
slaveConfig:
  slaves:
    - type: miaospeed
      id: "udp-check"
      token: "secret"
      address: "127.0.0.1:8765"
      option:
        stunURL: "udp://stunserver2025.stunprotocol.org:3478"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## slaveConfig.slaves[n].option.taskRetry / taskTimeout

{% tabs %}
{% tab title="解释" %}
1. `taskRetry` 是后端任务失败后的重试次数，不是秒数。
2. `taskTimeout` 是单个任务判定超时的毫秒数。
3. 它们更偏向“后端容错策略”，不是前端绘图超时。
{% endtab %}

{% tab title="特性" %}
1. 类型：`int`
2. 默认值：`3`、`5000`
3. 当前校验范围：`taskRetry=0~10`，`taskTimeout=1000~300000`
4. `taskTimeout` 太小容易误判超时，太大则会拉长失败任务回收时间。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
slaveConfig:
  slaves:
    - type: miaospeed
      id: "retry-safe"
      token: "secret"
      address: "127.0.0.1:8765"
      option:
        taskRetry: 2
        taskTimeout: 8000
```
{% endcode %}
{% endtab %}
{% endtabs %}

## slaveConfig.slaves[n].option.dnsServer

{% tabs %}
{% tab title="解释" %}
1. 这是后端解析节点域名时使用的 DNS 服务器列表。
2. 它支持普通 `host:port`、DoH URL，以及新版后端支持的 `mihomo://...` base64编码后的dns配置。
3. 如果你同时开启了 `runtime.enableDNSInject`，当前实现会优先把订阅里的 mihomo DNS 配置注入到这个列表最前面。
{% endtab %}

{% tab title="特性" %}
1. 类型：`list[str]`
2. 默认值：`[]`
3. 空列表表示使用后端自己的默认解析行为。
4. 如果同一个 DNS 已经存在，注入逻辑会尽量去重。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
slaveConfig:
  slaves:
    - type: miaospeed
      id: "dns-fixed"
      token: "secret"
      address: "127.0.0.1:8765"
      option:
        dnsServer:
          - "119.29.29.29:53"
          - "https://dns.google/dns-query"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## slaveConfig.slaves[n].option.apiVersion

{% tabs %}
{% tab title="解释" %}
1. 这是后端请求结构兼容版本开关。
2. 默认值 `1` 是当前最稳妥的主线兼容写法。
3. `2` 更偏向 AirportR/miaospeed 的 v2 结构；当前实现里它不支持 `downloadURL="DYNAMIC:ALL"`。
4. 上行测速相关字段是否会真正被保留发送，也取决于这里的版本号和你接的后端分支能力。
{% endtab %}

{% tab title="特性" %}
1. 类型：`int`
2. 默认值：`1`
3. `apiVersion=0` 或 `1` 时，请求里会裁掉版本字段和上行测速字段。
4. `apiVersion=2` 时，会裁掉上行测速字段。
5. 只有你明确知道目标后端支持更高版本请求时，才建议尝试保留上行测速字段。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
slaveConfig:
  slaves:
    - type: miaospeed
      id: "compat-v2"
      token: "secret"
      address: "127.0.0.1:8765"
      option:
        apiVersion: 2
```
{% endcode %}
{% endtab %}
{% endtabs %}

## slaveConfig.slaves[n].option.uploadURL / uploadDuration / uploadThreading

{% tabs %}
{% tab title="解释" %}
1. 这三项是上行测速相关配置。
2. 它们只有在你的目标后端分支真的支持带上行测速字段的请求时才有意义。
3. 默认 `apiVersion=1` 的情况下，这三项当前会在请求构造阶段被裁掉，不会真的发给后端。
{% endtab %}

{% tab title="特性" %}
1. 类型：`str` + `int`
2. 默认值：`https://speed.cloudflare.com/__up`、`8`、`4`
3. 当前校验范围：`uploadDuration=1~120`，`uploadThreading=1~64`
4. 如果你没有明确在跑支持上行测速的后端分支，保留默认即可，不必强行启用。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
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
{% endcode %}
{% endtab %}
{% endtabs %}

如果你还没搭好后端，可先看：

{% content-ref url="../miaospeed-hou-duan/da-jian-zhi-nan/README.md" %}
[README.md](../miaospeed-hou-duan/da-jian-zhi-nan/README.md)
{% endcontent-ref %}

以及：

{% content-ref url="../zhi-ling-xiang-jie/checkslave.md" %}
[checkslave.md](../zhi-ling-xiang-jie/checkslave.md)
{% endcontent-ref %}
