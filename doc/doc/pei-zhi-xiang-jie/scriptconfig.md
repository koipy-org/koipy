---
description: 此配置涉及测试时的后端脚本配置
---

# scriptConfig

这一页说明测试脚本相关配置。

在 koipy 里，脚本一般不长期存放在后端本地。它们主要由 bot 端读取、选择，然后在任务开始时连同测试请求一起发送给后端执行。

<details>

<summary>scriptConfig</summary>

{% code expandable="true" %}
```yaml
scriptConfig:
  scripts: # 脚本载入
    - type: gofunc # 表示是 miaospeed 的内置实现
      name: "TEST_PING_RTT" # 预留名称
      rank: -100 # 排序，越小越靠前
    - type: gojajs # 表示 miaospeed 主流脚本类型
      name: "示例脚本"
      rank: 0
      content: |
        function handler() {
          return {
            text: "成功",
            background: "186,230,126"
          }
        }
    - type: gojajs
      name: "Youtube"
      rank: 1
      content: "resources/scripts/builtin/youtube.js" # 也可以指定一个文件路径
```
{% endcode %}

</details>

## 概要

1. `scriptConfig.scripts` 是一个数组，每一项都是一个可被 koipy 识别的脚本条目。
2. 这些脚本既可以被交互式脚本选择器选中，也可以在 `rules[].script` 里通过名字直接引用。
3. 配置加载时，源码会先按 `rank` 升序排序，再进入后续选择与任务构造流程。

{% hint style="warning" %}
当前源码对脚本类型的实际支持只有 `gofunc` 和 `gojajs`。虽然内部常量里还保留了 `cpython`，但当前任务分发链路并不会正确处理它，不建议在配置中使用。
{% endhint %}

## scriptConfig.scripts

{% tabs %}
{% tab title="解释" %}
1. 这是脚本列表本体。
2. 如果你想让一个自定义脚本能被规则或前端选择器引用，它就需要出现在这里。
3. 普通自定义检测脚本通常写成 `gojajs`；内置测试项覆写通常写成 `gofunc` + 预留名称。
{% endtab %}

{% tab title="特性" %}
1. 类型：`list[Script]`
2. 源码加载后会按 `rank` 升序排序。
3. 普通脚本选择器展示的名称，来自这里每个脚本的 `name`。
4. `GEOIP_INBOUND` 和 `GEOIP_OUTBOUND` 虽然也是脚本名，但当前不会出现在普通脚本选择器列表里。
5. 建议每个脚本 `name` 都保持唯一；当前源码在按名字匹配时，命中的是排序后列表中的第一个同名项。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
scriptConfig:
  scripts:
    - type: gofunc
      name: "TEST_PING_RTT"
      rank: -100
    - type: gojajs
      name: "OpenAI"
      rank: 2
      content: "resources/scripts/builtin/openai.js"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## scriptConfig.scripts[n].type

{% tabs %}
{% tab title="解释" %}
1. 这项配置决定脚本的实现类型。
2. 当前最常用的是：
   1. `gojajs`：JavaScript 脚本，由 miaospeed 的 goja 引擎执行。
   2. `gofunc`：后端内置测试项，对应固定的预留名称。
3. `gofunc` 不是“任意 Go 代码注入”。它本质上只是告诉 koipy：这个名字要映射到某个已知内置测试项。
{% endtab %}

{% tab title="特性" %}
1. 类型：`str`
2. 可稳定使用的值：`gojajs`、`gofunc`
3. `gojajs` 适合自定义流媒体检测、地区检测、风险检测等逻辑。
4. `gofunc` 只适合和预留名称配套使用；任意自造的 `gofunc` 名字当前不会被正确映射。
5. `cpython` 虽然出现在源码常量里，但当前流程不会真正把它当成可执行脚本类型处理。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
scriptConfig:
  scripts:
    - type: gofunc
      name: "SPEED_AVERAGE"
      rank: -98
    - type: gojajs
      name: "Netflix"
      rank: 0
      content: "resources/scripts/builtin/netflix.js"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## scriptConfig.scripts[n].name

{% tabs %}
{% tab title="解释" %}
1. 这是脚本的唯一标识，也是规则里 `script` 数组要填写的名字。
2. 如果脚本类型是普通 `gojajs`，名字可以是任意字符串。
3. 如果你写的是预留名称，那么它会触发内置测试项覆写逻辑，而不再只是一个普通自定义脚本。
{% endtab %}

{% tab title="特性" %}
1. 类型：`str`
2. 建议保持唯一，避免同名。
3. `rules[].script` 引用的就是这里的 `name`。
4. 对于 `GEOIP_INBOUND`、`GEOIP_OUTBOUND` 这类 GEO 名称，当前更多是给规则或拓扑流程使用，而不是常规手动点选。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
scriptConfig:
  scripts:
    - type: gojajs
      name: "Claude"
      rank: 5
      content: "resources/scripts/builtin/Claude.js"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## scriptConfig.scripts[n].rank

{% tabs %}
{% tab title="解释" %}
1. 这项配置决定脚本结果在任务结果中的显示顺序。
2. 数字越小，排得越靠前。
3. koipy 在载入 `scriptConfig.scripts` 时会按这个值排序；任务真正合并测试项时，也会再次按脚本 `rank` 排序。
{% endtab %}

{% tab title="特性" %}
1. 类型：`int`
2. 可写负数、零、正数。
3. 内置测试项默认常见范围大致在 `-100 ~ 100`。
4. 如果你用预留名称覆写了一个内置项，那么它的 `rank` 也会跟着你写的值走。
5. 如果多个脚本 `rank` 相同，最终相对顺序更适合依赖配置加载顺序，但不建议把关键布局建立在这个细节上。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
scriptConfig:
  scripts:
    - type: gofunc
      name: "TEST_PING_RTT"
      rank: -100
    - type: gojajs
      name: "Youtube"
      rank: 0
      content: "resources/scripts/builtin/youtube.js"
    - type: gojajs
      name: "IP风险"
      rank: 11
      content: "resources/scripts/builtin/iprisk.js"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## scriptConfig.scripts[n].content

{% tabs %}
{% tab title="解释" %}
1. 这是脚本的实际内容来源。
2. 对 `gojajs` 来说，它既可以直接写内联脚本内容，也可以写成一个本地文件路径。
3. 对 `gofunc` 来说，通常可以留空；真正起作用的是预留名称本身。
4. koipy 在任务构造阶段会尝试把 `content` 当成本地路径解析；如果路径存在，就读取文件内容并发送给后端。
{% endtab %}

{% tab title="特性" %}
1. 类型：`str`
2. 文件路径支持相对路径和绝对路径；相对路径通常相对于 koipy 的工作目录。
3. 文件会按 `utf-8` 读取。
4. 一个很重要的细节是：如果你写的是路径字符串，但文件并不存在，程序不会在这里报错，而是会把这段字符串直接当成脚本源码本体发送出去。
5. 所以路径写错时，经常不是“读取失败”，而是“后端拿到一段毫无意义的脚本内容然后执行失败”。
6. 对自定义 `gojajs` 脚本来说，`content` 不应留空；否则任务构造时不会有真正脚本内容可发送。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
scriptConfig:
  scripts:
    - type: gojajs
      name: "内联示例"
      rank: 0
      content: |
        function handler() {
          return {
            text: "成功",
            background: "186,230,126"
          }
        }
    - type: gojajs
      name: "文件示例"
      rank: 1
      content: "resources/scripts/builtin/youtube.js"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## 预留脚本名称

以下名称会被 koipy 识别为内置测试项。它们既可以写进 `scriptConfig.scripts` 里用于覆写排序或特殊逻辑，也可以直接写进 `rules[].script` 里使用。

| 测试项 | 描述 |
| --- | --- |
| `TEST_PING_RTT` | TCP RTT（数据交换延迟测试） |
| `TEST_PING_CONN` | HTTP 请求体感延迟测试 |
| `TEST_PING_MAX_CONN` | HTTP请求体感最大延迟 |
| `TEST_PING_MAX_RTT` | 最大RTT（往返时延峰值） |
| `TEST_PING_TOTAL_CONN` | 总HTTP请求延迟（所有请求的累计值） |
| `TEST_PING_TOTAL_RTT` | 总RTT（所有数据包往返时延总和） |
| `TEST_PING_SD_RTT` | RTT标准差（延迟波动指标） |
| `TEST_PING_SD_CONN` | HTTP请求延迟标准差（稳定性分析） |
| `TEST_PING_PACKET_LOSS` | RTT丢包率（数据包丢失百分比） |
| `TEST_HTTP_CODE` | 目标地址的HTTP状态码（如200、404等） |
| `SPEED_AVERAGE` | 平均下行传输速度 |
| `SPEED_MAX` | 最大下行传输速度 |
| `SPEED_PER_SECOND` | 每秒实时下行传输速度 |
| `USPEED_AVERAGE` | 平均上行速度 |
| `USPEED_MAX` | 最大上行速度 |
| `USPEED_PER_SECOND` | 每秒上行速度 |
| `UDP_TYPE` | UDP协议过滤行为 / UDP端口通断测试 |
| `GEOIP_INBOUND` | 入口拓扑测试（地理IP路径分析） |
| `GEOIP_OUTBOUND` | 出口拓扑测试（地理IP路径分析） |
| `TEST_HIJACK_DETECTION` | 测速劫持检测 |

{% hint style="info" %}
如果你只是想在规则里调用这些内置项，其实不一定非要先在 `scriptConfig.scripts` 里写一份；直接在 `rules[].script` 中写这些预留名称，当前源码也能识别。把它们显式写进 `scriptConfig.scripts` 的主要意义，是覆写 `rank`、统一管理、或让某些项出现在可选列表中。
{% endhint %}

## GEOIP 特殊处理

{% tabs %}
{% tab title="解释" %}
1. `GEOIP_INBOUND` 和 `GEOIP_OUTBOUND` 是最特殊的两项。
2. 如果它们按 `gofunc` 配置，koipy 会强制使用主端内置的 GEOIP 脚本内容。
3. 如果它们按 `gojajs` 配置，则可以把默认 GEOIP 脚本替换成你自己的脚本内容或脚本文件。
{% endtab %}

{% tab title="特性" %}
1. 想自定义拓扑 GEOIP 行为时，应使用 `gojajs`。
2. 这两项当前不会出现在普通脚本选择器列表里。
3. 拓扑相关结果在后端侧可能存在缓存，所以即使你换了脚本，也不一定每次都会立刻看到结果变化。
4. 如果你指定的自定义 GEOIP 脚本路径非法、内容为空，或脚本本身执行失败，实际效果就不会符合预期；具体表现取决于后端当时的处理结果与缓存状态。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
scriptConfig:
  scripts:
    - type: gojajs
      name: "GEOIP_INBOUND"
      rank: 1
      content: "resources/scripts/geo/my_geoip.js"
    - type: gojajs
      name: "GEOIP_OUTBOUND"
      rank: 1
      content: "resources/scripts/geo/my_geoip.js"
```
{% endcode %}
{% endtab %}
{% endtabs %}

关于 GEOIP 脚本的更多背景和缓存说明，可参考：

{% content-ref url="../wen-ti-da-yi/guan-yu-tuo-pu-ce-shi.md" %}
[guan-yu-tuo-pu-ce-shi.md](../wen-ti-da-yi/guan-yu-tuo-pu-ce-shi.md)
{% endcontent-ref %}

## 与规则联动

{% tabs %}
{% tab title="解释" %}
1. `rules[].script` 填的是脚本名字数组。
2. 数组元素既可以是你在 `scriptConfig.scripts` 里定义的普通脚本名，也可以是上面的预留名称。
3. 任务开始时，koipy 会按这些名字找到脚本配置，解析文件内容，按 `rank` 排序后统一发送给后端。
{% endtab %}

{% tab title="特性" %}
1. 规则里的 `script` 不写时，通常需要在前端手动选择测试项。
2. 规则写了 `script` 后，可以省掉脚本选择步骤，直接形成固定测试套餐。
3. 当规则同时引用自定义脚本和预留名称时，它们会按最终 `rank` 混排。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
scriptConfig:
  scripts:
    - type: gojajs
      name: "Youtube"
      rank: 0
      content: "resources/scripts/builtin/youtube.js"

rules:
  - name: "流媒体连通性"
    url: "https://example.com/sub"
    script:
      - "TEST_PING_RTT"
      - "TEST_PING_CONN"
      - "Youtube"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## 编写脚本

如果你要自己写 `gojajs` 脚本，建议直接看这部分文档：

{% content-ref url="../miaospeed-hou-duan/ce-shi-jiao-ben-bian-xie/README.md" %}
[README.md](../miaospeed-hou-duan/ce-shi-jiao-ben-bian-xie/README.md)
{% endcontent-ref %}

以及：

{% content-ref url="../miaospeed-hou-duan/ce-shi-jiao-ben-bian-xie/di-yi-ge-ce-shi-jiao-ben.md" %}
[di-yi-ge-ce-shi-jiao-ben.md](../miaospeed-hou-duan/ce-shi-jiao-ben-bian-xie/di-yi-ge-ce-shi-jiao-ben.md)
{% endcontent-ref %}
