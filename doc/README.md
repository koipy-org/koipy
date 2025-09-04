# koipy主页

## 介绍

koipy ​**​** ​**​/ˈkɒpi/ 音同 “copy”  ，或者 ​​/ˈkɒpaɪ/**&#x20;

koipy 是**专注于代理平台的**连通性测试的工具，它目前依赖于Telegram作为展示前端，所以它是一个测试​机器人（Telegram bot）。koipy目前是**前后端分离**的架构，后端是具体代理测试工具实现，名为[miaospeed](https://github.com/AirportR/miaospeed)前端负责构建测试任务等操作。

koipy起源于 [fulltclash](https://github.com/AirportR/FullTclash) ，是fulltclash的下游分支。

## 源代码

目前，koipy开源了1.0版本的代码

仓库地址：

{% @github-files/github-code-block url="https://github.com/koipy-org/koipy" %}

koipy后续版本的代码是保持**闭源**的，如果你愿意接受闭源产品，可以继续查阅此文档，此文档跟进最新版koipy使用指南。

## 能干什么

* 给代理服务器（节点）进行连通性测试（包括延迟RTT、地区流媒体解锁检测等）
* 给代理服务器（节点）进行**下行**速度测试
* 给代理服务器（节点）进行网络拓扑分析（检测入口和出口）



## 结果展示

![连通性测试+速度测试](https://raw.githubusercontent.com/koipy-org/koipy/master/resources/image/example.png)

<figure><img src=".gitbook/assets/image (18).png" alt=""><figcaption><p>拓扑测试</p></figcaption></figure>

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

✨更多功能，请自行搭建体验✨
