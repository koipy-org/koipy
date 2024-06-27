## 介绍

koipy是一个Telegram 节点测速、连通性测试机器人，同时提供对接[miaospeed](https://github.com/AirportR/miaospeed)后端的开源实现。
koipy是[fulltclash](https://github.com/AirportR/FullTclash)的下游分支。

## 功能

koipy目前是一个demo项目，未来还会继续完善。

koipy 是基于前后端模式的，并且后端仅支持miaospeed.

bot主端可以接收你的节点信息，构造测试请求发送到后端，并根据后端测试结果绘制图片。

## 结果展示
![测试](https://raw.githubusercontent.com/koipy-org/koipy/master/resources/image/example.png)
## 基本使用

前往配置文件示例 ./resources/config.example.yaml

搭建好机器人，并配置好后端以及脚本信息。



在你的测速bot中使用：

```
/test <订阅链接>
```

即可开始测试，注意订阅链接需要Clash订阅格式。



## 注意

此文档尚未完善，如果你无法部署机器人，请发起issue



## 授权许可

目前采用MIT开源许可，您可随意对此项目按照许可证所限定范围的进行使用。

