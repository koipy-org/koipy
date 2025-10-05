# 预设函数

MiaoSpeed 用Golang实现并暴露了以下函数，可供在js层调用：

* fetch -> http应用层协议实现
* netcat -> tcp协议原始连接读写
* print -> 控制台打印INFO等级
* debug -> 控制台打印DEBUG等级

## 函数签名

### fetch

参见：

{% @github-files/github-code-block url="https://github.com/AirportR/miaospeed/blob/f49141500afd50e3216c17f39452c558890bf9ca/engine/factory/fetch.go#L11" %}

## netcat

参见:

{% @github-files/github-code-block url="https://github.com/AirportR/miaospeed/blob/f49141500afd50e3216c17f39452c558890bf9ca/engine/factory/netcat.go#L11" %}

## 预设脚本

ms有三个预设脚本：

{% embed url="https://github.com/AirportR/miaospeed/tree/master/engine/embeded" %}

其中，

[default\_geoip.js](https://github.com/AirportR/miaospeed/blob/master/engine/embeded/default_geoip.js) 用于查询ip信息

[default\_ip.js](https://github.com/AirportR/miaospeed/blob/master/engine/embeded/default_ip.js) 用于获取当前节点的出口IP

[predefined.js](https://github.com/AirportR/miaospeed/blob/master/engine/embeded/predefined.js) 预设的清洗函数，方便安全的返回解析内容
