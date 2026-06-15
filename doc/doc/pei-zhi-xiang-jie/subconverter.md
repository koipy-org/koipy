---
description: 这里的配置用于把原始订阅或协议链接转成 koipy 可测试的订阅地址。
---

# subconverter

这一页说明订阅转换对接配置。当前实现同时支持外部转换后端，以及 `builtin` 模式下的本地内置转换。

<details>

<summary>subconverter</summary>

{% code expandable="true" %}
```yaml
subconverter:
  enable: false
  mode: builtin
  template:
    backend: "http://$Host:$Port/sub?target=$Target&new_name=true&url=$EncodedURL"
  defaults:
    target: ClashMeta
```
{% endcode %}

</details>

{% hint style="warning" %}
`builtin` 模式和外部 `subconverter` / `sub-store` 不是同一条执行路径。外部模式主要靠 `template.backend` 拼 URL；`builtin` 模式则直接走 koipy 内部转换逻辑。
{% endhint %}

## subconverter.enable

{% tabs %}
{% tab title="解释" %}
1. 这项配置决定是否启用订阅转换流程。
2. 对外部模式来说，启用后会在真正拉取前用模板重写成转换后端地址。
3. 对 `builtin` 模式来说，启用后会直接在本地执行转换，不依赖额外转换服务进程。
4. 对 `vmess://`、`trojan://` 这类协议链接来说，只有启用后，koipy 才会尝试把它们转成可测试订阅。
{% endtab %}

{% tab title="特性" %}
1. 类型：`bool`
2. 默认值：`false`
3. 关闭时，HTTP(S) 订阅按原链接获取；协议链接则不会自动转成可测试订阅内容。
4. 如果原始链接里已经包含 `target=` 参数，外部模式下当前订阅采集器会把它视为“已经转换过”，不会再次重写。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
subconverter:
  enable: true
  mode: builtin
  defaults:
    target: ClashMeta
```
{% endcode %}
{% endtab %}
{% endtabs %}

## subconverter.mode

{% tabs %}
{% tab title="解释" %}
1. 这项配置用于告诉 koipy 当前走哪一类转换模式。
2. `subconverter` / `substore` 主要参与默认 `host`、`port`、`target` 的推断，并配合模板拼接外部转换地址。
3. `builtin` 代表走本地内置转换器，不需要额外转换服务进程。
{% endtab %}

{% tab title="特性" %}
1. 类型：`str`
2. 默认值：`builtin`
3. 当 `mode=substore` 时，默认端口会倾向 `3000`，默认 `target` 会倾向 `ClashMeta`。
4. 即使你没写 `mode=substore`，只要模板里出现 `/download/sub`，当前实现也会按 sub-store 风格推断部分默认值。
5. 当 `mode=builtin` 时，本地转换默认目标也会优先落到 `ClashMeta`。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
subconverter:
  enable: true
  mode: substore
  template:
    backend: "http://$Host:$Port/download/sub?target=$Target&url=$EncodedURL&fakeSub=true"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## subconverter.template.backend

{% tabs %}
{% tab title="解释" %}
1. 这是转换后端的完整 URL 模板。
2. 当前实现会做非常直接的字符串占位符替换，不是复杂的模板引擎。
3. 当你把原始订阅链接塞进 query 参数时，应该优先使用 `$EncodedURL`，而不是 `$URL`。
4. 同理，如果你的后端参数名习惯用 `content`，也可以使用 `$Content` / `$EncodedContent`。
5. 这项主要给外部模式使用；`builtin` 模式下不会靠它发起真正的远程转换请求。
{% endtab %}

{% tab title="特性" %}
1. 类型：`str`
2. 模板为空时，转换结果会是空字符串，等价于“没有可用后端模板”。
3. 模板里的 URL scheme 还会参与默认 `scheme` 推断。
4. 新协议是否能成功转换，外部模式取决于你对接的转换后端本身；`builtin` 模式则取决于 koipy 当前内置转换能力。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
subconverter:
  enable: true
  mode: substore
  template:
    backend: "http://$Host:$Port/download/sub?target=$Target&url=$EncodedURL&fakeSub=true"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## subconverter.defaults

{% tabs %}
{% tab title="解释" %}
1. 这是模板默认参数字典。
2. `host`、`port`、`scheme`、`target` 可以在这里显式指定，覆盖自动推断。
3. 你也可以放任意自定义键，例如 `ua`、`config`、`emoji`，然后在模板里通过 `$UA`、`$Config`、`$Emoji` 这类占位符读取。
4. 在 `builtin` 模式下，这一组里最常用的是 `target`，其余参数更多是为外部模式准备的。
{% endtab %}

{% tab title="特性" %}
1. 类型：`dict`
2. 默认 `host` 是 `127.0.0.1`
3. 默认 `port` 是 `25500`；如果 `mode=substore` 或模板里出现 `/download/sub`，默认端口会改成 `3000`
4. 默认 `scheme` 优先取模板本身的 scheme；模板没写时回退到 `http`
5. 默认 `target` 是 `clash`；如果走 sub-store 风格或 `builtin` 模式，则默认会倾向 `ClashMeta`
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
subconverter:
  enable: true
  template:
    backend: "http://$Host:$Port/sub?target=$Target&url=$EncodedURL&ua=$EncodedUA"
  defaults:
    host: "127.0.0.1"
    port: 25500
    target: "ClashMeta"
    ua: "clash-verge"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## 占位符与编码

{% tabs %}
{% tab title="解释" %}
1. 当前稳定可用的核心占位符包括：`$Mode`、`$Scheme`、`$Host`、`$Port`、`$Target`、`$URL`、`$Content`
2. 它们都支持对应的 URL 编码版本：`$EncodedMode`、`$EncodedURL`、`$EncodedContent` 等。
3. `defaults` 里的任意键，也会自动生成 `$Key` 和 `$EncodedKey` 版本。
4. 键名匹配不严格区分大小写，像 `ua`、`UA`、`Ua`、`user_agent` 这类常见变体，当前都会尝试注册出可用占位符。
5. `$Mode` 当前可能是 `subconverter`、`substore` 或 `builtin`。
{% endtab %}

{% tab title="特性" %}
1. 协议链接和普通 HTTP 订阅都会走同一套占位符替换逻辑。
2. 当原始值需要出现在 query 参数里时，优先使用 `Encoded` 版本更稳妥。
3. 如果模板后端要求的参数名不是 `url`，你可以自由改成 `content`、`src` 或其它名字，koipy 不做限制。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
subconverter:
  enable: true
  mode: substore
  template:
    backend: "http://$Host:$Port/download/sub?target=$Target&url=$EncodedURL&config=$EncodedConfig&fakeSub=true"
  defaults:
    config: "my-collection"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## 生效时机

{% tabs %}
{% tab title="解释" %}
1. 如果用户输入的是普通 HTTP(S) 订阅链接，外部模式下 koipy 会在真正下载前决定是否按模板重写；`builtin` 模式下则会在下载后直接本地转换内容。
2. 如果用户输入的是 `vmess://...` 这类协议链接，且 `subconverter.enable=true`，koipy 会先进入转换流程；外部模式是包装成远程转换 URL，`builtin` 模式是直接本地转换。
3. 如果原始 URL 里已经带有 `target=`，外部模式下当前实现会把它认作“已经是转换后链接”，不会二次转换。
4. 如果单次任务设置了 `runtime.disableSubCvt=true`，则会跳过这套转换流程。
{% endtab %}

{% tab title="特性" %}
1. 这套逻辑既影响手动输入链接，也影响规则中的 `url`。
2. 外部模式下，koipy 主要负责拼链接；最终仍要看目标转换服务返回的内容是否可解析。
3. `builtin` 模式下，转换发生在 koipy 进程内部，省掉了额外服务进程，但当前仍应视为实验性路径。
4. 如果你对接的是 sub-store，而模板或 target 写成了不兼容的目标格式，最常见的表现就是“拉取成功但节点为空”。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
subconverter:
  enable: true
  mode: builtin
  defaults:
    target: ClashMeta
```
{% endcode %}
{% endtab %}
{% endtabs %}

关于单次任务里临时禁用订阅转换，可参考：

{% content-ref url="runtime.md" %}
[runtime.md](runtime.md)
{% endcontent-ref %}
