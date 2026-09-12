---
description: 邀请一个目标进行测试
---

# /invite

## 解释

邀请一个目标进行测试。

`/invite` 一般适用于这类场景：
1. 发起者提供订阅，目标只负责点按钮、发订阅，测试结果由 bot 产出
2. invite被设计得尽量人性化、简单化，适合接触koipy的新手入门使用
3. 公开群组中，不希望随便给予用户权限，但是有面向普通游客提供大批量测试服务的需求

## 用法

用 `/invite` 回复或引用一条目标消息：

```
/invite
```

也可以带上指令参数，提前指定后端与排序：

```
/invite?s=local&sort=订阅原序
```

支持回复一条消息、也可以直接在私聊里对自己使用。

## 权限

* 发起 `/invite` 需要**用户权限**，普通游客无法发起。
* 目标本身不需要任何权限，可以是普通 TG 账号。
* 如果希望某个群里的所有人都能发起邀请测试，需要把该群组 id 填进 `bot.inviteGroup`：

{% content-ref url="../pei-zhi-xiang-jie/bot.md" %}
[bot.md](../pei-zhi-xiang-jie/bot.md)
{% endcontent-ref %}

## 流程

1. 发起者用 `/invite` 回复目标消息。
2. bot 依次完成后端选择、排序选择，然后在目标消息下回复一条带按钮的邀请消息。
3. 目标点击按钮，会通过深链接进入与 bot 的私聊并自动触发确认。
4. bot 在私聊中提示「验证成功」，并给出 **60 秒**的等待窗口。
5. 目标在 60 秒内把订阅链接（或消息、文件）发给 bot。
6. bot 收到后开始测试，结果发回原对话。

{% hint style="warning" %}
等待窗口是 60 秒，超时后 bot 会把邀请消息标记为已过期，需要重新发起一次 `/invite`。
{% endhint %}

## 可选的测试类型

邀请消息里的按钮由 bot 内置按钮和 `bot.commands` 里的自定义指令共同组成。内置按钮如下：

| 按钮 | 说明 |
| --- | --- |
| `test` | 完整测试 |
| `analyze` | 拓扑测试（按钮文本默认显示为拓扑） |
| `speed` | 下行速度测试 |
| `uspeed` | 上行速度测试 |
| `full` | 全部测试项 |
| `ping` | 延迟测试 |
| `udptype` | UDP 类型测试 |

关于按钮的启用、隐藏与文本覆写，参阅：

{% content-ref url="../pei-zhi-xiang-jie/bot.md" %}
[bot.md](../pei-zhi-xiang-jie/bot.md)
{% endcontent-ref %}

## 目标可以发送什么

目标在等待窗口内可以发送以下任意一种：

* 一条订阅链接
* 一条包含订阅链接的消息
* 一个订阅文件（直接发送文档给 bot）

发送文件时，文件名会被用作订阅来源名。文件大小上限与订阅拉取一致，超过会被拒绝。

{% hint style="info" %}
通过邀请上传文档的能力在 v2.1.0 之后加入，如果你的 bot 版本较旧，请改用发送链接的方式。
{% endhint %}

目标还可以在消息里带上过滤器：

```text
https://example.com/sub 香港 直连
```

第一个位置参数是订阅，第二个是包含过滤器，第三个是排除过滤器。

## 限制

* 每个 UID 同时只允许存在一个邀请会话，无法同时发起两个 `/invite`。
* 目标没有用户权限时，本次测试会屏蔽测速时长与实时渲染，隐藏后端也不会被选中。
* 目标发送的订阅会经过黑名单校验，命中 `bot.inviteBlacklistURL` 或 `bot.inviteBlacklistDomain` 时会被拒绝。
* 邀请测试不使用缓存中的旧会话，重复对同一条消息发起邀请会被忽略。

## 相关配置

{% content-ref url="../pei-zhi-xiang-jie/bot.md" %}
[bot.md](../pei-zhi-xiang-jie/bot.md)
{% endcontent-ref %}

{% content-ref url="zhi-ling-can-shu.md" %}
[zhi-ling-can-shu.md](zhi-ling-can-shu.md)
{% endcontent-ref %}
