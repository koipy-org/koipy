---
description: 这里的配置用于定义普通授权用户名单。
---

# user

这一页说明普通用户权限配置。`user` 决定哪些人可以使用受限指令、按钮和规则能力。

<details>

<summary>user</summary>

{% code expandable="true" %}
```yaml
user:
  - 123456789
  - 987654321
```
{% endcode %}

</details>

{% hint style="warning" %}
底层列表虽然接受 `int` 和 `str`，但当前多数权限判断最终还是按 Telegram `UID` 走。为了减少歧义，`user` 也推荐直接写数字 UID。
{% endhint %}

## user

{% tabs %}
{% tab title="解释" %}
1. 这是普通授权用户名单。
2. 很多需要权限的交互式操作，都会先检查发起者是否在 `user` 里。
3. 当前实现的主要用户过滤器是按 `UID` 判断；少数辅助路径会顺便兼容用户名字符串，但不建议把这种兼容当主配置方式。
{% endtab %}

{% tab title="特性" %}
1. 类型：`list[int | str]`
2. 实际推荐写法：`list[int]`
3. 列表为空时，普通受限功能通常只剩管理员可用。
4. 想长期稳定管理权限，最好使用不会变化的 UID，而不是用户名。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
user:
  - 123456789
  - 987654321
```
{% endcode %}
{% endtab %}
{% endtabs %}

## 与 admin 的关系

{% tabs %}
{% tab title="解释" %}
1. 程序启动初始化时，会把 `admin` 里的成员合并进 `user`。
2. 因此大多数情况下，你不需要把管理员再手动重复写一遍。
3. `user` 更偏向“普通授权名单”，`admin` 更偏向“最高权限名单”。
{% endtab %}

{% tab title="特性" %}
1. 管理员和普通用户不是同一个概念。
2. 想加普通用户，改 `user` 即可；想加管理员，要改 `admin`。
3. 这个合并动作发生在启动初始化阶段，日常管理时最好仍然把两者分开理解。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
admin:
  - 111111111

user:
  - 222222222
  - 333333333
```
{% endcode %}
{% endtab %}
{% endtabs %}

## 推荐管理方式

{% tabs %}
{% tab title="解释" %}
1. 对日常增删普通用户来说，直接用 `/grant` 和 `/ungrant` 比手改配置更方便。
2. 当前这两个命令会修改 `CONFIG.user`，再保存并重载配置。
3. 所以 `user` 这页更适合拿来理解机制，而不是每次都手工编辑。
{% endtab %}

{% tab title="特性" %}
1. `/grant` 和 `/ungrant` 都是管理员命令
2. 它们修改的是 `user`，不是 `admin`
3. 如果你在群里频繁临时授权，这种方式明显更省事
{% endtab %}

{% tab title="配置示例" %}
{% code title="手工预填示例" lineNumbers="true" %}
```yaml
user:
  - 123456789
```
{% endcode %}
{% endtab %}
{% endtabs %}

## 游客与受限指令

{% tabs %}
{% tab title="解释" %}
1. 不在 `user` 里的用户，很多受限操作会直接被拦下。
2. 一个比较特殊的例子是 `/subinfo`：如果发起者不在 `user`，而你又没有配置 `network.httpProxy`，当前实现会拒绝游客使用这个命令。
3. 这样做是为了避免直接暴露主端 IP。
{% endtab %}

{% tab title="特性" %}
1. `user` 不只是“能不能点按钮”，它还会影响部分规则、任务和订阅查询入口
2. 如果你希望游客也能安全地查 `/subinfo`，需要额外配好 `network.httpProxy`
{% endtab %}

{% tab title="配置示例" %}
{% code title="允许少量固定用户" lineNumbers="true" %}
```yaml
user:
  - 123456789
  - 222222222
```
{% endcode %}
{% endtab %}
{% endtabs %}

相关命令可继续看：

{% content-ref url="../zhi-ling-xiang-jie/grant.md" %}
[grant.md](../zhi-ling-xiang-jie/grant.md)
{% endcontent-ref %}

以及：

{% content-ref url="../zhi-ling-xiang-jie/subinfo.md" %}
[subinfo.md](../zhi-ling-xiang-jie/subinfo.md)
{% endcontent-ref %}
