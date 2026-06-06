# koipy主页

## 介绍

koipy 读作 `/ˈkɒpi/`，音同 "copy"，也可以读作 `/ˈkɒpaɪ/`。

koipy 是专注于代理平台的连通性测试工具。它目前依赖 Telegram 作为展示前端，因此是一个测试机器人（Telegram bot）。koipy 采用前后端分离架构，后端是具体的代理测试工具实现，名为 [miaospeed](https://github.com/AirportR/miaospeed)，前端负责构建测试任务等操作。

koipy 起源于 [fulltclash](https://github.com/AirportR/FullTclash)，是 fulltclash 的下游分支。

## 源代码

目前，koipy 开源了 1.0 版本的代码。

仓库地址：

{% @github-files/github-code-block url="https://github.com/koipy-org/koipy" %}

koipy 后续版本的代码保持**闭源**。如果你愿意接受闭源产品，可以继续查阅此文档，此文档会跟进最新版 koipy 使用指南。

## 能干什么

* 给代理服务器（节点）进行连通性测试（包括延迟 RTT、地区流媒体解锁检测等）
* 给代理服务器（节点）进行**下行**速度测试
* 给代理服务器（节点）进行网络拓扑分析（检测入口和出口）



## 结果展示

![连通性测试+速度测试](https://raw.githubusercontent.com/koipy-org/koipy/master/resources/image/example.png)

![拓扑测试](.gitbook/assets/image%20%2818%29.png)

## 如何开始

{% content-ref url="kuai-su-kai-shi.md" %}
[kuai-su-kai-shi.md](kuai-su-kai-shi.md)
{% endcontent-ref %}

## 特性

在不断地开发迭代中，koipy不断地支持新的特性，包括但不限于：

* 全Clash系代理协议支持（包括vless、hysteria2、anytls、tuic）
* 批量测试（重要）
* 支持代理服务提供商（机场）URL订阅
* 可高度定制化的测试结果绘图
* 可高度定制化的配置文件支持（自定义测速线程、ping地址、ping次数、节点过滤等）
* 自由可拓展的javascript脚本支持
* 轻量的访问权限控制
* 本地化语言包支持
* 多测试后端配置支持
* 针对实时测试需求临时修改的指令参数、位置参数、以及终极测试规则

更多功能，请自行搭建体验。
