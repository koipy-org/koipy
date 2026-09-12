---
description: 展示许可证信息
---

# /license

## 解释

展示当前 bot 的许可证（激活码）信息。

## 用法

### 用法1：查询当前 bot 的许可证

```
/license
```

### 用法2：解析任意一个许可证

直接发送许可证码本身即可，不需要任何指令前缀。也可以回复一条包含许可证码的消息，然后发送 `/license`。

## 特性

* `/license` 需要**用户权限**。
* 任何一条长度与许可证码完全一致的消息，也会被当作许可证解析请求。
* 输出内容包含：Bot ID、版本称谓、后端数量上限、规则数量上限、群组测试额度、签发时间、到期时间、当前状态。
* 解析失败时会直接回显错误原因，方便判断是激活码抄错了还是已经过期。
* 消息会在一段时间后被自动删除，避免长期留在对话里。

{% hint style="warning" %}
许可证码属于敏感信息，请不要公开发送。发送后 bot 会记录一条 INFO 级别的解析日志。
{% endhint %}

## 相关页面

{% content-ref url="../../ji-huo.md" %}
[ji-huo.md](../../ji-huo.md)
{% endcontent-ref %}

{% content-ref url="panel.md" %}
[panel.md](panel.md)
{% endcontent-ref %}
