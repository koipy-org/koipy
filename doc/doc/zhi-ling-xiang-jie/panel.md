# /panel

## 解释

bot的控制面板，可以查看系统的部分信息，以及进行在线编辑配置。

## 用法

```
/panel
```

## 特性

* 需要**管理员权限**。
* 面板顶部会展示运行信息，包括系统名称与版本、系统时间、Python 版本、内存占用、bot 版本、代码提交、构建时间。
* 面板上提供两个入口：
  * **配置管理**：进入配置选择页面，可以逐项查看、修改、删除配置值。
  * **关于**：展示许可证信息。
* 在配置页面里可以直接点按钮改值，改完后会给出保存 / 重载的选择。
* `/panel` 取代了旧的 `/system` 指令。

{% hint style="info" %}
`/system` 已弃用，发送后 bot 会提示改用 `/panel`。
{% endhint %}

## 相关页面

{% content-ref url="cfg.md" %}
[cfg.md](cfg.md)
{% endcontent-ref %}

{% content-ref url="reload.md" %}
[reload.md](reload.md)
{% endcontent-ref %}

{% content-ref url="license.md" %}
[license.md](license.md)
{% endcontent-ref %}
