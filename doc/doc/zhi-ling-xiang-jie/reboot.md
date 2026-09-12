---
description: 重启或结束 bot 进程
---

# /reboot

## 别名

* /restart

## 解释

重启整个程序。

## 用法

```
/reboot
```

## 特性

* `/reboot` 与 `/restart` 完全等价，都需要**管理员权限**。
* 重启前会先结束 koipy 启动的子进程，然后重新执行程序本体。
* 重启期间 bot 会短暂离线，正在进行的测试任务会中断。
* 配置改动建议先用 `/reload` 试试，只有涉及启动阶段才生效的配置项才需要重启。

## 相关指令

### /killme

```
/killme
```

* 别名：`/kill`
* 需要**管理员权限**。
* 直接结束 bot 进程，不重新拉起。
* 与 `/reboot` 的区别是：`/reboot` 会重新执行程序，`/killme` 只是让进程退出。

## 相关页面

{% content-ref url="reload.md" %}
[reload.md](reload.md)
{% endcontent-ref %}

{% content-ref url="panel.md" %}
[panel.md](panel.md)
{% endcontent-ref %}

{% hint style="info" %}
`/system` 已弃用，发送后会提示改用 `/panel`。
{% endhint %}
