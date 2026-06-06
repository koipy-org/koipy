---
description: 此部分说明配置解释
---

# 配置详解

## 注意

此配置详解并未完善，部分配置可能没有详细的解释。完整配置请前往：

{% content-ref url="../../pei-zhi-mu-ban.md" %}
[pei-zhi-mu-ban.md](../../pei-zhi-mu-ban.md)
{% endcontent-ref %}

## 预备知识

koipy 的配置文件名为 **config.yaml**，需要你在首次搭建 Bot 时自主创建。YAML 是一种人类可读的文本格式。如果你需要让 Bot 做一些个性化设置，比如修改绘图配色、更改 bot 行为等，就需要修改 `config.yaml`，它有一定语法要求，详情请参阅：

{% embed url="https://zh.wikipedia.org/wiki/YAML" %}

接下来就是各种配置项的功能作用说明。

你可以在配置模板页查看 koipy 支持的所有配置。它们都有简要说明和默认值。

## 编辑器

善用编辑器，例如 VS Code，它可以帮助你更方便地格式化配置文件。

## koipy 配置相关细节

koipy 内部自主设计了一套反序列化和序列化模块，以更好地适配项目架构。

### 等效配置

对于以下两个配置，在被 koipy 加载到程序内部时是等效的：

```yaml
log-level: INFO
log_level: INFO
```

原因是koipy内部将这两者进行了合并，以便统一命名。
