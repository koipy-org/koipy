---
description: 获取你的 UID 信息
---

# /id

## 解释

获取发起者的 UID 与当前对话的 ID 信息。

## 用法

```
/id
```

## 特性

* 任何人都可以使用，不需要权限。
* 输出内容包含：
  * 你的 TG UID
  * 当前对话（群组/私聊）的 ID
  * 用户对象与对话对象的完整信息，以折叠引用块的形式展示
* 过长内容默认折叠，避免刷屏。
* 在群组里使用时，消息会在一段时间后被自动删除。
* 这是获取群组 ID 最省事的方式，拿到群组 ID 后可以填进 `bot.inviteGroup` 等配置。

## 相关配置

{% content-ref url="../pei-zhi-xiang-jie/bot.md" %}
[bot.md](../pei-zhi-xiang-jie/bot.md)
{% endcontent-ref %}

{% content-ref url="../pei-zhi-xiang-jie/admin.md" %}
[admin.md](../pei-zhi-xiang-jie/admin.md)
{% endcontent-ref %}
