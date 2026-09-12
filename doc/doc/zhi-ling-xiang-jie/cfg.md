---
description: 在对话里读写配置文件
---

# /get、/set、/del

## 解释

这三个指令用于在对话里直接读取、修改、删除配置文件里的某个值，不需要手动打开 `config.yaml`。

它们的操作对象是 koipy 内存中的配置对象，路径语法使用 JSON 路径表达式。

## 用法

### 读取

```
/get <JSON路径表达式>
```

### 修改

```
/set <JSON路径表达式> <值>
```

### 删除

```
/del <JSON路径表达式>
```

## 路径写法

路径以 `$.` 开头，逐层写配置的键名：

```text
$.bot.cacheTime
$.runtime.speedThreads
$.slaveConfig.slaves.0.comment
```

也可以不写 `$.`，程序会自动补全。数组下标直接写数字。

## 例子

```text
/get $.bot.cacheTime
/set $.bot.cacheTime 120
/set $.runtime.speedThreads 8
/del $.bot.parseMode
```

## 特性

* 这三个指令都需要**管理员权限**。
* 每次操作后 bot 都会回显：执行的命令、是否成功、耗时、结果类型和结果值。
* `/set` 和 `/del` 会直接作用于内存中的配置对象，并在消息下方给出保存/重载的按钮，由你决定是否持久化配置。
* 修改后建议用 `/reload` 或面板上的按钮确认配置已写入文件。
* 值不需要加引号，程序会自动推断类型。

{% hint style="warning" %}
`/set` 不会校验你填的值是否合理，写错可能导致配置无法加载。建议在改动前先备份 `config.yaml`。
{% endhint %}

{% hint style="info" %}
配置解析失败时，现在会给出带出错位置的错误信息；热重载失败会回滚，不会把半成品配置应用进去。
{% endhint %}

## 相关页面

{% content-ref url="panel.md" %}
[panel.md](panel.md)
{% endcontent-ref %}

{% content-ref url="reload.md" %}
[reload.md](reload.md)
{% endcontent-ref %}
