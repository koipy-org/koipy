---
description: 这里的配置用于控制 koipy 的日志输出级别。
---

# log-level

这一页说明日志级别配置。它主要影响 koipy 的日志输出等级，以及少部分附属 logger 的等级设置。

<details>

<summary>log-level</summary>

{% code expandable="true" %}
```yaml
log-level: INFO
```
{% endcode %}

</details>

{% hint style="warning" %}
如果这里填了无效值，当前源码会自动回退到 `INFO`。如果填 `DISABLE`，则会直接移除 loguru 的 sink。
{% endhint %}

## log-level

{% tabs %}
{% tab title="解释" %}
1. 这项配置用于指定 koipy 主要日志输出的等级。
2. 等级越靠后，表示只保留越严重的日志。
3. 它既影响文件日志，也会影响部分使用 loguru / pyrogram session 的输出行为。
{% endtab %}

{% tab title="特性" %}
1. 类型：`str`
2. 稳定可用值：`DEBUG`、`INFO`、`WARNING`、`ERROR`、`CRITICAL`、`DISABLE`
3. `log-level` 和 `log_level` 在 koipy 配置加载后是等效的。
4. 非法值会回退到 `INFO`
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
log-level: WARNING
```
{% endcode %}
{% endtab %}
{% endtabs %}

## 各等级的含义

{% tabs %}
{% tab title="解释" %}
```text
DEBUG     最详细，适合排查问题
INFO      常规运行信息
WARNING   只看警告及以上
ERROR     只看错误及以上
CRITICAL  只看严重错误
DISABLE   禁用日志
```
{% endtab %}

{% tab title="特性" %}
1. 日常运行常见选择是 `INFO` 或 `WARNING`
2. 需要排查配置、网络、脚本问题时，更适合临时切到 `DEBUG`
3. `DISABLE` 不适合排查问题时使用，因为你会直接失去大部分主日志输出
{% endtab %}

{% tab title="配置示例" %}
{% code title="开发排错示例" lineNumbers="true" %}
```yaml
log-level: DEBUG
```
{% endcode %}
{% endtab %}
{% endtabs %}

## 生效范围

{% tabs %}
{% tab title="解释" %}
1. 当日志级别有效且不为 `DISABLE` 时，koipy 会把日志写到 `logs/koipy_{time}.log`。
2. 当前文件日志按 `7 days` 轮转。
3. `pyrogram.session` logger 会被设置成和这里一致的等级。
4. 但 `apscheduler` 会被固定压到 `ERROR`，Python 标准库 `logging.basicConfig` 也会固定在 `WARNING`。
{% endtab %}

{% tab title="特性" %}
1. 这项配置并不等于“所有控制台输出都严格同步到同一等级”
2. 它主要控制 koipy 主日志链路，而不是每个第三方库的全部细节
3. `DISABLE` 时，当前实现会 `logger.remove()`，因此 loguru 默认控制台输出也会一起关掉
{% endtab %}

{% tab title="配置示例" %}
{% code title="低噪声示例" lineNumbers="true" %}
```yaml
log-level: ERROR
```
{% endcode %}
{% endtab %}
{% endtabs %}
