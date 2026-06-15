---
description: 这里的配置用于控制订阅获取前后的附加处理。
---

# subscription

这一页说明订阅获取相关配置。当前模板里 `subscription` 下面主要是 `age`，用于处理上游返回的 age 加密订阅内容。

<details>

<summary>subscription</summary>

{% code expandable="true" %}
```yaml
subscription:
  age:
    enable: false
    secretKey: ""
    publicKey: ""
    publicKeyHeader: X-Age-Public-Key
```
{% endcode %}

</details>

{% hint style="warning" %}
当前实现只支持 age `X25519 ASCII armor` 格式。若上游返回的是二进制 age 文件，koipy 不会解密成功。
{% endhint %}

## subscription.age.enable

{% tabs %}
{% tab title="解释" %}
1. 这项配置用于启用订阅内容的 age 解密流程。
2. 开启后，koipy 会在订阅下载成功后、解析 YAML 或执行订阅转换前，先尝试判断内容是否是 age armored 文本。
3. 如果内容本身不是 age 格式，当前实现会直接原样继续处理，不会因为开启了这项就强制报错。
{% endtab %}

{% tab title="特性" %}
1. 类型：`bool`
2. 默认值：`false`
3. 它只影响“下载后的订阅内容”，不影响请求 URL 本身。
4. 解密失败时，当前流程会记录警告并把这次订阅处理判定为失败。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
subscription:
  age:
    enable: true
    secretKey: "AGE-SECRET-KEY-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## subscription.age.secretKey

{% tabs %}
{% tab title="解释" %}
1. 这是 age X25519 私钥，格式通常是 `AGE-SECRET-KEY-...`。
2. 当前实现会先做首尾空白裁剪，再尝试参与解密。
3. 只有当上游实际返回 age armored 订阅内容时，这个私钥才真正会被用到。
{% endtab %}

{% tab title="特性" %}
1. 类型：`str`
2. 默认值：空字符串
3. 如果订阅内容是 age armored，但这里仍为空，当前实现会直接报出“缺少 secretKey”的解密错误。
4. 配置导出和安全拷贝时，这个字段会被掩码处理，不会原样暴露。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
subscription:
  age:
    enable: true
    secretKey: "AGE-SECRET-KEY-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## subscription.age.publicKey

{% tabs %}
{% tab title="解释" %}
1. 这是发给上游订阅服务端的 age 公钥，格式通常是 `age1...`。
2. 它不会参与本地解密；它的作用是告诉上游“请用这个公钥加密返回内容”。
3. 只有当你对接的订阅服务端支持这种约定时，这项配置才有意义。
{% endtab %}

{% tab title="特性" %}
1. 类型：`str`
2. 默认值：空字符串
3. 留空时，koipy 不会额外发送公钥请求头。
4. 它和 `secretKey` 往往需要成对使用，但不是语法层面的强制绑定。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
subscription:
  age:
    enable: true
    secretKey: "AGE-SECRET-KEY-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    publicKey: "age1xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## subscription.age.publicKeyHeader

{% tabs %}
{% tab title="解释" %}
1. 这项配置用于指定发送公钥时使用的 HTTP 请求头名。
2. 当前默认值是 `X-Age-Public-Key`。
3. 只有当 `publicKey` 和 `publicKeyHeader` 都非空时，请求头才会真正加到订阅请求里。
{% endtab %}

{% tab title="特性" %}
1. 类型：`str`
2. 默认值：`X-Age-Public-Key`
3. 如果你的上游服务端要求别的请求头名，可以在这里改。
4. 留空时，即使设置了 `publicKey`，当前实现也不会发送这个请求头。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
subscription:
  age:
    enable: true
    secretKey: "AGE-SECRET-KEY-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    publicKey: "age1xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    publicKeyHeader: "X-Age-Public-Key"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## 生效流程

{% tabs %}
{% tab title="解释" %}
1. koipy 先按原有逻辑发起订阅下载请求。
2. 如果启用了 `subscription.age.enable`，下载完成后会先尝试识别并解密 age 内容。
3. 解密成功后，后续的订阅解析、节点过滤、订阅转换才会继续使用解密后的明文内容。
4. 这意味着它作用在整个订阅处理链路的前面，而不是只对某一个后端生效。
{% endtab %}

{% tab title="特性" %}
1. 普通未加密订阅不会因为开启了 `age` 支持而被破坏。
2. 当前只支持 ASCII armor，不支持二进制 age payload。
3. 对 HTTP 请求的唯一额外影响，是可选发送 `publicKeyHeader` 这个请求头。
{% endtab %}

{% tab title="配置示例" %}
{% code title="典型场景" lineNumbers="true" %}
```yaml
subscription:
  age:
    enable: true
    secretKey: "AGE-SECRET-KEY-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    publicKey: "age1xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    publicKeyHeader: "X-Age-Public-Key"
```
{% endcode %}
{% endtab %}
{% endtabs %}
