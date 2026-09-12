# /grant

## 解释

将一个TG目标（可以是TG账号，匿名身份，bot）升级为koipy用户组权限。用户权限可以使用bot的功能如下：

* 随时随地发起测试任务
* 使用支持的指令参数进行测试（自定义线程数、自定义过滤器、自定义结果输出格式等）
* 使用隐藏的后端测试
* 使用规则进行测试
* 创建或删除自己的测试规则
* 可以使用 /invite 邀请其他非用户权限的目标（匿名身份无效）测试
* 可以使用 /checkslaves 进行检查后端
* 可以随时中断任何正在进行的**测速**任务，除非开启bot的严格模式（参见配置 bot.strictMode）
* 可以随时开启/关闭实时渲染
* 可以通过在 /subinfo 指令中使用规则名作为参数查询流量信息
* 可以选择任意后端进行测试
* ~~装逼~~

## 用法

```
/grant <TG UID>
```

也可以直接回复一条目标消息，然后发送 `/grant`，此时不需要写 UID。

## 取消授权

```
/ungrant <TG UID>
```

`/ungrant` 是 `/grant` 的反向操作，会把目标从用户名单里移除。同样支持回复消息的方式。

## 特性

* 需要**管理员权限**。
* 支持一次授权多个目标，UID 之间用空格隔开。
* 这里修改的是 `user` 名单，不是 `admin`。管理员请直接改配置文件里的 `admin`。
* 修改后会立即写入配置文件并重载。
* 配置里的 `user` 名单同时支持写 UID 和用户名（大小写不敏感）。

## 相关配置

{% content-ref url="../pei-zhi-xiang-jie/user.md" %}
[user.md](../pei-zhi-xiang-jie/user.md)
{% endcontent-ref %}

{% content-ref url="../pei-zhi-xiang-jie/admin.md" %}
[admin.md](../pei-zhi-xiang-jie/admin.md)
{% endcontent-ref %}
