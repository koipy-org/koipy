---
description: 这里的配置用于控制单次测试任务的运行方式。
---

# runtime

这一页说明任务运行时相关配置。和 `bot`、`image` 这类长期静态配置不同，`runtime` 更偏向“本次任务怎么跑”。

<details>

<summary>runtime</summary>

{% code expandable="true" %}
```yaml
runtime: # 测速任务可以动态调整的配置
  entrance: true # 是否显示入口IP段
  duration: 10 # 测速时长，优先级高于后端单独设置的测速时长
  ipstack: true # 是否启用双栈检测
  pingURL: https://www.gstatic.com/generate_204 # 延迟测试地址
  speedFiles: # 速度测试的大文件下载地址
  - https://dl.google.com/dl/android/studio/install/3.4.1.0/android-studio-ide-183.5522156-windows.exe
  speedNodes: 300 # 最大测速节点数量
  speedThreads: 4 # 后端测速线程数量，优先级高于后端单独设置的
  output: image # 输出类型，目前支持 image 和 json 和 video 三种
  realtime: false # 是否实时渲染测试结果
  disableSubCvt: false # 是否针对单次测试禁用订阅转换
  protectContent: false # bot输出的所有图片设置为保护内容
  enableDNSInject: false # 是否启用 mihomo DNS 注入
```
{% endcode %}

</details>

## runtime 的作用域

1. 顶层 `runtime` 用来提供一组运行时默认值。
2. `rules[].runtime` 可以为单条规则单独覆写。
3. 指令参数也能覆写其中一部分，例如：`?thread=8&duration=15&sort=http&realtime=true&nocvt=true`
4. 源码里的 `runtime` 结构还支持 `includeFilter`、`excludeFilter`、`sort`，只是当前模板页没有全部展开。

{% hint style="warning" %}
按目前情况，全局 `runtime` 最稳定的字段是 `speedNodes`、`speedFiles`、`ipstack`、`entrance`、`protectContent`、`enableDNSInject`。`pingURL`、`duration`、`speedThreads`、`sort`、`output`、`realtime`、`disableSubCvt` 更适合写在 `rules[].runtime` 或通过指令参数覆写。
{% endhint %}

## runtime.pingURL

{% tabs %}
{% tab title="解释" %}
1. 这项配置用于覆写本次任务的延迟测试地址，对应后端里的 `option.pingAddress`。
2. 如果你填的是 `https://...`，结果图里相关列名会更偏向 HTTPS/TLS 延迟；如果是 `http://...`，则更偏向 HTTP 延迟。
3. 它只影响延迟测试的结果，不影响大文件地址测速的结果。
{% endtab %}

{% tab title="特性" %}
1. 类型：`str`
2. 更适合写在 `rules[].runtime` 中。按当前源码，全局 `runtime.pingURL` 不会稳定地自动继承给每个任务。
3. 如果当前任务没有设置它，程序会继续使用后端自身的 `option.pingAddress`。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
rules:
  - name: "CF 延迟测试"
    url: "https://example.com/sub"
    runtime:
      pingURL: "https://cp.cloudflare.com/generate_204"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## runtime.speedFiles

{% tabs %}
{% tab title="解释" %}
1. 这是测速大文件地址列表。
2. 只有当后端的 `option.downloadURL` 写成 `DYNAMIC:ALL` 时，后端才会从 `runtime.speedFiles` 中随机挑一个地址来测。
3. 如果后端 `downloadURL` 本来就是固定 URL，这个列表不会强行覆盖后端配置。
{% endtab %}

{% tab title="特性" %}
1. 类型：`list[str]`
2. koipy也接受把它写成单个字符串，但最终会被转换成列表。
3. 当前解析逻辑只保留以 `http` 开头的条目。
4. 这项全局默认值是稳定兜底生效的，如果规则和后端配置里均没有设置测速文件地址，则会使用顶层 `runtime` 的值。
5. 如果你的后端依赖 `DYNAMIC:ALL`，这里就不要留空。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
runtime:
  speedFiles:
    - "https://dl.google.com/dl/android/studio/install/3.4.1.0/android-studio-ide-183.5522156-windows.exe"
    - "https://speed.cloudflare.com/__down?bytes=200000000"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## runtime.speedNodes

{% tabs %}
{% tab title="解释" %}
1. 限制一次任务最多允许测试多少个节点。
2. 订阅拉取完成后，会先应用 `includeFilter` / `excludeFilter` 过滤，再检查过滤后的节点数量是否超过这个值。
3. 超过限制时，任务会直接报错，不会进入后端测速阶段。
{% endtab %}

{% tab title="特性" %}
1. 类型：`int`
2. 默认值：`300`
3. 这项全局默认值是稳定生效的，也可以在 `rules[].runtime` 里单独覆写。
4. 它控制的是“节点数量上限”，不是测速线程数。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
runtime:
  speedNodes: 300
```
{% endcode %}
{% endtab %}
{% endtabs %}

## runtime.speedThreads

{% tabs %}
{% tab title="解释" %}
1. 用来覆写本次任务的后端测速线程数，对应后端的 `option.downloadThreading`。
2. 线程开得越大，不代表结果一定越好；它更像是“并发压测强度”。
3. 对低配后端或高倍率节点，线程过高反而更容易让测试结果失真。
{% endtab %}

{% tab title="特性" %}
1. 类型：`int`
2. 后端校验范围是 `1 ~ 64`。
3. 如果你通过指令参数传入，则 `?thread=` / `?t=` 当前只接受 `1 ~ 64`。
4. 更适合写在 `rules[].runtime` 或用指令参数临时覆写。按当前源码，全局 `runtime.speedThreads` 不会稳定地自动继承给每个任务。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
rules:
  - name: "4线程测速"
    url: "https://example.com/sub"
    runtime:
      speedThreads: 4
```
{% endcode %}
{% endtab %}
{% endtabs %}

## runtime.duration

{% tabs %}
{% tab title="解释" %}
1. 用来覆写本次任务的测速时长，对应后端的 `option.downloadDuration`。
2. 持续时间更长，通常更容易拉开高倍率节点之间的差距，但任务整体也会更慢。
3. 这项配置主要对含有测速项的任务有意义，纯连通性测试基本不会用到它。
{% endtab %}

{% tab title="特性" %}
1. 类型：`int`
2. 后端校验范围是 `1 ~ 120` 秒。
3. 如果你通过指令参数传入，则 `?duration=` / `?d=` 当前只接受 `1 ~ 60`。
4. 更适合写在 `rules[].runtime` 或用指令参数临时覆写。按当前源码，全局 `runtime.duration` 不会稳定地自动继承给每个任务。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
rules:
  - name: "15秒测速"
    url: "https://example.com/sub"
    runtime:
      duration: 15
```
{% endcode %}
{% endtab %}
{% endtabs %}

## runtime.entrance

{% tabs %}
{% tab title="解释" %}
1. 控制拓扑结果中是否显示入口 IP 段。
2. 关闭后，拓扑结果仍然会有入口聚类和入口地域信息，只是不再显示入口 IP 段这一列。
3. 它主要影响的是拓扑图和 GEOIP 结果，不影响普通连通性测速图。
{% endtab %}

{% tab title="特性" %}
1. 类型：`bool`
2. 默认值：`true`
3. 这项全局默认值是稳定生效的，也可以在 `rules[].runtime` 里单独开启。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
runtime:
  entrance: true
```
{% endcode %}
{% endtab %}
{% endtabs %}

## runtime.ipstack

{% tabs %}
{% tab title="解释" %}
1. 控制拓扑结果中是否显示双栈信息，也就是常见的 IPv4 / IPv6 栈标识列。
2. 关闭后，拓扑图仍可继续生成，只是不显示栈信息那一列。
3. 它同样主要作用于 GEOIP / 拓扑结果。
{% endtab %}

{% tab title="特性" %}
1. 类型：`bool`
2. 默认值：`true`
3. 这项全局默认值是稳定生效的，也可以在 `rules[].runtime` 里单独开启。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
runtime:
  ipstack: true
```
{% endcode %}
{% endtab %}
{% endtabs %}

## runtime.sort

{% tabs %}
{% tab title="解释" %}
1. 控制结果输出时的排序方式。
2. 如果值非法，结果会回退到 `订阅原序`。
3. 当前koipy支持的完整值有：

```text
订阅原序
HTTP升序
HTTP降序
平均速度升序
平均速度降序
最大速度升序
最大速度降序
RTT升序
RTT降序
```

{% endtab %}

{% tab title="特性" %}
1. 类型：`str`
2. 更适合写在 `rules[].runtime` 或通过指令参数传入。按当前源码，全局 `runtime.sort` 不会稳定地自动继承给每个任务。
3. 如果你走的是指令参数，当前还支持短别名，例如：`http`、`rhttp`、`aspeed`、`mspeed`、`rtt`。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
rules:
  - name: "HTTP排序测速"
    url: "https://example.com/sub"
    runtime:
      sort: "HTTP升序"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## runtime.includeFilter / excludeFilter

{% tabs %}
{% tab title="解释" %}
1. 这两项用于按节点名称做筛选。
2. `includeFilter` 是先保留匹配项，`excludeFilter` 是再排除匹配项。
3. 支持正则表达式。
{% endtab %}

{% tab title="特性" %}
1. 类型：`str`
2. 过滤顺序是：先 `includeFilter`，再 `excludeFilter`。
3. 过滤发生在节点数量限制 `speedNodes` 之前。
4. 正则写错时，koipy会记录错误日志，并退回到“不做这次过滤”的效果。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
rules:
  - name: "只测日韩，排除低倍率"
    url: "https://example.com/sub"
    runtime:
      includeFilter: "(JP|KR)"
      excludeFilter: "(0\\.1x|剩余流量)"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## runtime.output

{% tabs %}
{% tab title="解释" %}
1. 控制任务结果输出格式。
2. 当前公开配置模板里列出的稳定值是：`image`、`json`、`video`。
3. `image` 是普通结果图，`json` 适合下游程序处理，`video` 用于展示动态炫酷图。
{% endtab %}

{% tab title="特性" %}
1. 类型：`str`
2. 更适合写在 `rules[].runtime` 或通过指令参数传入。按当前源码，全局 `runtime.output` 不会稳定地自动继承给每个任务，未显式设置时仍会回退到 `image`。
3. `video` 只适合单后端、含测速项、节点数不过大的任务；不满足条件时，程序会回退到 `image`。
4. 如果你的运行环境没有正确安装视频生成依赖库——ffmepg，`video` 会回退到图片结果。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
rules:
  - name: "测速导出JSON"
    url: "https://example.com/sub"
    runtime:
      output: "json"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## runtime.realtime

{% tabs %}
{% tab title="解释" %}
1. 控制测速任务是否默认打开实时渲染。
2. 实时渲染会在任务进行过程中不断编辑或更新结果图，比普通进度条更直观。
3. 它主要对“单后端 + 含测速项 + 图片/视频输出”的任务有意义。
{% endtab %}

{% tab title="特性" %}
1. 类型：`bool`
2. 更适合写在 `rules[].runtime` 或通过 `?realtime=true` 这类指令参数启用。按当前源码，全局 `runtime.realtime` 不会稳定地自动继承给每个任务。
3. 单后端时，当前默认实时渲染节点上限是 `40`；多后端时会按后端数量分摊这个上限。
4. 多后端目前没有稳定的合并实时画布，因此就算打开，更多也只是保留实时进度语义，而不是稳定输出一张实时总图。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
rules:
  - name: "实时测速"
    url: "https://example.com/sub"
    runtime:
      realtime: true
```
{% endcode %}
{% endtab %}
{% endtabs %}

## runtime.disableSubCvt

{% tabs %}
{% tab title="解释" %}
1. 这项配置用于在单次任务里临时禁用订阅转换。
2. 它只在你已经启用了全局 `subconverter` / `sub-store` 之类的订阅转换时才有意义。
3. 开启后，本次任务会直接拿原始订阅去解析，不再先走订阅转换。
{% endtab %}

{% tab title="特性" %}
1. 类型：`bool`
2. 更适合写在 `rules[].runtime` 或通过 `?nocvt=true` 这类指令参数启用。按当前源码，全局 `runtime.disableSubCvt` 不会稳定地自动继承给每个任务。
3. 它适合处理“某些新协议经过转换后反而丢节点”的场景。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
rules:
  - name: "直连原始订阅"
    url: "https://example.com/sub"
    runtime:
      disableSubCvt: true
```
{% endcode %}
{% endtab %}
{% endtabs %}

## runtime.protectContent

{% tabs %}
{% tab title="解释" %}
1. 控制 bot 发送的结果媒体是否使用 Telegram 的“保护内容”模式。
2. 开启后，TG 前端会限制转发、保存、复制等行为。
3. 它主要影响图片和视频这类媒体结果。
{% endtab %}

{% tab title="特性" %}
1. 类型：`bool`
2. 默认值：`false`
3. 这项全局默认值是稳定生效的，也可以在 `rules[].runtime` 中单独开启。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
runtime:
  protectContent: true
```
{% endcode %}
{% endtab %}
{% endtabs %}

## runtime.enableDNSInject

{% tabs %}
{% tab title="解释" %}
1. 控制是否把订阅里的 `dns:` 配置注入到后端请求中。
2. 开启后，如果当前订阅本身带有 mihomo 风格的 `dns` 段，koipy会把它编码成 `mihomo://...` 的字符串，并插到后端配置 `dnsServer` 列表最前面。
3. 如果订阅里没有 `dns` 字段，或者编码后过长 / 非法，就会静默回退到后端原有的 DNS 列表。
{% endtab %}

{% tab title="特性" %}
1. 类型：`bool`
2. 默认值：`false`
3. 这项全局默认值是稳定生效的，也可以在 `rules[].runtime` 中单独开启。
4. 它依赖后端对 `mihomo://` DNS格式的支持，要求较新的 miaospeed 后端版本。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
runtime:
  enableDNSInject: true
```
{% endcode %}
{% endtab %}
{% endtabs %}
