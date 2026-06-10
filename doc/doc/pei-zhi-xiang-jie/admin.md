---
description: 这里的配置用于定义 bot 的管理员名单。
---

# admin

这一页说明管理员配置。`admin` 决定哪些 Telegram 账号可以执行管理员专属命令，以及哪些人拥有最高级别的配置操作权限。

<details>

<summary>admin</summary>

{% code expandable="true" %}
```yaml
admin:
  - 123456789
  - 987654321
```
{% endcode %}

</details>

{% hint style="warning" %}
虽然底层列表解析器接受 `int` 和 `str` 两种元素，但当前管理员权限检查实际按 Telegram `UID` 判断。新配置请直接写数字 UID，不要写用户名。
{% endhint %}

## admin

{% tabs %}
{% tab title="解释" %}
1. 这是 bot 的管理员名单。
2. 管理员可以执行管理员权限指令，例如 `/reload`、`/grant`、`/leave` 等。
3. 管理员指令检查逻辑都是按 Telegram `UID` 是否在这个列表里判断的。
{% endtab %}

{% tab title="特性" %}
1. 类型：`list[int | str]`
2. 实际推荐写法：`list[int]`
3. 如果你把用户名字符串写进来，配置能加载，但当前管理员检查通常不会把它当成有效管理员。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
admin:
  - 123456789
  - 987654321
```
{% endcode %}
{% endtab %}
{% endtabs %}

## 首次启动自动认主

{% tabs %}
{% tab title="解释" %}
1. 如果当前 `admin` 列表为空，koipy 会进入一次性的“自动认主”流程。
2. 第一个给 bot 发送私聊消息的人，会被加入管理员列表。
3. 写入配置后，程序会触发一次重载 / 重启流程，让新管理员身份立即生效。
{% endtab %}

{% tab title="特性" %}
1. 这个自动认主流程只在“管理员列表为空”时启用。
2. 它监听的是私聊消息，不是群消息。
3. 一旦已经有管理员，这个引导逻辑就不会再继续注册新的管理员。
{% endtab %}

{% tab title="配置示例" %}
{% code title="允许自动认主的最小配置" lineNumbers="true" %}
```yaml
admin: []
```
{% endcode %}
{% endtab %}
{% endtabs %}

## 与 user 的关系

{% tabs %}
{% tab title="解释" %}
1. 程序启动初始化时，会把 `admin` 里的成员合并进 `user`。
2. 这意味着大多数情况下，管理员天然也拥有普通用户权限，不需要再重复写进 `user`。
3. 但要注意，`/grant` 和 `/ungrant` 修改的是 `user`，不是 `admin`。
{% endtab %}

{% tab title="特性" %}
1. 如果你想新增普通用户，用 `/grant` 更合适。
2. 如果你想新增管理员，当前更适合直接编辑 `config.yaml` 里的 `admin` 列表。
3. 不要把“给用户授权”和“提升为管理员”混为一回事，它们是两套配置。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
admin:
  - 123456789

user:
  - 222222222
```
{% endcode %}
{% endtab %}
{% endtabs %}

普通用户授权指令可参考：

{% content-ref url="../zhi-ling-xiang-jie/grant.md" %}
[grant.md](../zhi-ling-xiang-jie/grant.md)
{% endcontent-ref %}
