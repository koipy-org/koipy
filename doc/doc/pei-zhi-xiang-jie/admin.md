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

{% hint style="info" %}
`admin` 列表里的元素既可以是数字 UID，也可以是用户名（不带 `@`，大小写不敏感）。两种写法都会参与匹配，建议优先用数字 UID，因为它不会变。
{% endhint %}

## admin

{% tabs %}
{% tab title="解释" %}
1. 这是 bot 的管理员名单。
2. 管理员可以执行管理员权限指令，例如 `/reload`、`/grant`、`/leave` 等。
3. 管理员指令检查逻辑会拿发起者的 UID 和用户名，分别与这个列表比对，命中任意一个就算管理员。
{% endtab %}

{% tab title="特性" %}
1. 类型：`list[int | str]`
2. 实际推荐写法：`list[int]`
3. 用户名匹配不区分大小写，写 `Kala` 和 `kala` 效果相同。
4. 用户名可以随时改，改了之后旧名字就匹配不上了，所以长期稳定的授权还是用 UID 更稳妥。
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
