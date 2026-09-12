# /reload

## 解释

重载你的配置文件

## 用法

```
/reload
```

## 特性

* 支持热重载，即在不重启bot的情况重新加载配置文件
* 支持保存内存改动重载，这适用于在bot中在线编辑配置文件
* 支持丢弃内存中的改动重载
* 需要**管理员权限**
* 重载失败时不会把半成品配置应用进去，当前生效的配置会保持原样
* 配置文件解析失败时，错误信息会带上出错的位置，方便定位到具体是哪一行写错了
* 启动阶段如果配置无法加载，程序会直接打印可读错误并退出，不会带着一份默认配置继续运行

{% hint style="warning" %}
只有启动阶段才读取的配置项（例如 `bot.autoResetCommands`、订阅黑名单）不会因为热重载而立即生效，这类改动仍需重启 bot。
{% endhint %}

## 相关页面

{% content-ref url="panel.md" %}
[panel.md](panel.md)
{% endcontent-ref %}

{% content-ref url="cfg.md" %}
[cfg.md](cfg.md)
{% endcontent-ref %}
