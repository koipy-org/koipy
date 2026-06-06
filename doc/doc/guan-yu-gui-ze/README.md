---
description: 此篇幅将介绍koipy的一大特性--规则系统
---

# 关于规则

## 定义

在 koipy 中，规则是一系列测试行为的集合。通过预先定义好的规则字段，可以在前端 bot 的测试指令中快速发起想要的测试，例如 `/test`、`/speed` 等。

## 规则字段（配置）

设置的一条规则中，有以下字段：

* `name`：此规则的名字。
* `url`：此规则所绑定的订阅 URL。
* `script`：测试脚本的数组。
* `runtime`：测试运行时动态改变的设置，比如测速线程（`speedThreads`）、测 Ping 任务的 `pingURL`、结果排序等。具体可用值参阅 `config.yaml` 里的全局 `runtime` 配置。
* `slaveid`：后端 ID。指定后端后将不会弹出选择后端页面。
* `owner`：此规则创建者的 TG UID。

## 场景举例

1. 将订阅保存为一个具体的名字，以方便进行测试，以及避免暴露订阅

使用 `/rule <订阅链接> <具体名字>`

例子：

```
/rule https://www.google.com 谷歌云
```

2. 在上面的基础上，指定后端 ID

由于 bot 未在前端实现指定后端 ID 的文本接收，故需要手动在配置文件中进行配置：

```yaml
rules: # 注意这行，说明 rules 是一个数组，数组里面每一个元素即为规则的配置，下面不写的话自行补全
- name: 谷歌云
  url: "https://www.google.com"
  script: []
  slaveid: local
  runtime: null
  owner: 123456789 # 改成对应目标的 uid
```

你在后端配置中的所有后端 ID 均可用。如果 `slaveid` 对应的后端无法找到，将自动进入选择后端页面。

3. 在上面的基础上，选定 ping RTT 测试和 HTTP 延迟测试

这里需要用到预留脚本名称，有关预留名称的作用，参阅：

{% content-ref url="../pei-zhi-xiang-jie/scriptconfig.md" %}
[scriptconfig.md](../pei-zhi-xiang-jie/scriptconfig.md)
{% endcontent-ref %}

`script` 字段是一个数组。

```yaml
- name: 谷歌云
  url: "https://www.google.com"
  script: [TEST_PING_RTT, TEST_PING_CONN]
  slaveid: local
  runtime: null
  owner: 123456789
```

第二种写法，与上面效果等同：

```yaml
- name: 谷歌云
  url: "https://www.google.com"
  script:
  - "TEST_PING_RTT"
  - "TEST_PING_CONN"
  slaveid: local
  runtime: null
  owner: 123456789
```

4. 在上面的基础上，指定排序为“HTTP 升序”

```yaml
- name: 谷歌云
  url: "https://www.google.com"
  script:
  - "TEST_PING_RTT"
  - "TEST_PING_CONN"
  slaveid: local
  runtime:
    sort: "HTTP升序"
  owner: 123456789
```

## 优先级

或许你会想，如果我在设置规则的同时，又在测试指令中使用指令参数，会怎样呢，例如：

```
/test?s=local&sort=订阅原序 谷歌云
```

答案是指令参数的优先级大于规则。遵循的原则是所见即所得，你在前端操作的一切指令，都应该符合你的主观感受。如果不是，那就是程序出现 bug，欢迎向开发者反馈。
