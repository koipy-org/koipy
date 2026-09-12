---
description: 节点出入口分析
---

# /topo

## 别名

* /analyze

## 解释

构建并发起一次网络拓扑测试，分析节点的入口和出口。

`/topo` 与 `/test` 共用同一套任务构建流程，区别在于它内置了拓扑相关的测试项，并默认使用订阅原序排序。

## 用法

### 用法1：

```
/topo <订阅链接> <包含过滤器:可选> <排除过滤器:可选>
```

### 用法2：

```
/topo <规则名> <包含过滤器:可选> <排除过滤器:可选>
```

### 用法3：加入指令参数

```
/topo?s=local <订阅链接>
```

### 用法4

回复或引用一条消息、文件发起测试，与 `/test` 一致。

## 内置测试项

`/topo` 会默认勾选以下测试项：

| 测试项 | 描述 |
| --- | --- |
| `GEOIP_INBOUND` | 入口拓扑测试（地理 IP 路径分析） |
| `GEOIP_OUTBOUND` | 出口拓扑测试（地理 IP 路径分析） |

## 特性

* `/topo` 与 `/analyze` 完全等价，配置 `bot.commands` 时二者会一起被启用或禁用。
* 排序不会起作用，拓扑的结果图为了保证显示效果，内部进行了特殊排序。
* 多后端联测时，拓扑结果可能因为 GEOIP 脚本的逻辑影响而不完全一致。
* 拓扑相关结果在后端侧可能存在缓存，所以即使你换了 GEOIP 脚本，也不一定每次都会立刻看到结果变化。
* 关于拓扑测试的常见疑问，参阅：

{% content-ref url="../wen-ti-da-yi/guan-yu-tuo-pu-ce-shi.md" %}
[guan-yu-tuo-pu-ce-shi.md](../wen-ti-da-yi/guan-yu-tuo-pu-ce-shi.md)
{% endcontent-ref %}

## 指令参数

详见：

{% content-ref url="zhi-ling-can-shu.md" %}
[zhi-ling-can-shu.md](zhi-ling-can-shu.md)
{% endcontent-ref %}
