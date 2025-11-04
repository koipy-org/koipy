---
description: 此部分说明配置解释
---

# 配置详解

## 注意

此配置详解并未完善，部分配置可能没有详细的解释，完整配置请前往:

{% content-ref url="../../pei-zhi-mu-ban.md" %}
[pei-zhi-mu-ban.md](../../pei-zhi-mu-ban.md)
{% endcontent-ref %}

## 预备知识

koipy的配置文件名为 **config.yaml** 它需要你在首次搭建Bot时自主创建。yaml格式是一种人类可读的文本格式。如果你需要让Bot做一些个性化的设置，比如修改绘图配色，更改bot行为等，需要修改config.yaml配置文件，它是有一定语法要求的，详情请参阅：



{% embed url="https://zh.wikipedia.org/wiki/YAML" %}

接下来就是各种配置项的功能作用详解。

你可以在 ./resources/config.example.yaml 查看koipy支持的所有配置。它们都有着简要的说明以及默认值。你甚至可以直接复制一份，改自己想改的。

## 编辑器

善用编辑器，例如VS Code，它可以帮助你很好地格式化配置文件

## koipy 配置相关细节

koipy内部自主设计了一套反序列化和序列化模块，以更好地适配项目架构。

### 等效配置

对于以下两个配置，在被koipy加载到程序内部时，是等效的：

```yaml
log-level: INFO
log_level: INFO
```

原因是koipy内部将这两者进行了合并，以便统一命名。
