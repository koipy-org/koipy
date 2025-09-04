---
description: 测试梦开始的地方
---

# /test

## 解释

构建并发起一次测试任务

## 用法

用法1：

```
/test <订阅链接> <包含过滤器:可选> <排除过滤器:可选>
```

用法2：

```
/test <规则名> <包含过滤器:可选> <排除过滤器:可选>
```

用法3：加入指令参数

```
/test?s=local&sort=订阅原序 <订阅链接> <包含过滤器:可选> <排除过滤器:可选>
```

## 位置参数

* <订阅链接> 输入一个HTTP前缀的URL，例：https://www.google.com
* <规则名> 输入一个规则名，什么是规则请查看：

{% content-ref url="../guan-yu-gui-ze/" %}
[guan-yu-gui-ze](../guan-yu-gui-ze/)
{% endcontent-ref %}

* <包含过滤器> 过滤订阅里面的节点，选择仅测试部分节点，支持正则关键字
* <排除过滤器> 过滤订阅里面的节点，选择排除部分节点，支持正则关键字

过滤器是先包含再排除

## 指令参数

详见：

{% content-ref url="zhi-ling-can-shu.md" %}
[zhi-ling-can-shu.md](zhi-ling-can-shu.md)
{% endcontent-ref %}
