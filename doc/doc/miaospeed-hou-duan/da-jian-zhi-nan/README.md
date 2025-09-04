---
description: 此页将介绍具体搭建步骤
---

# 搭建指南

以下操作均使用本项目组维护的仓库，搭建的系统环境为Ubuntu22.04（Linux）：

{% @github-files/github-code-block url="https://github.com/AirportR/miaospeed" %}

1. 对接环境

miaospeed作为服务端（后端），需要公网IP或者内网穿透等方式才能让客户端（主端）连接上后端。

2. 下载预编译的二进制

对于普通用户，可以下载Github仓库编译好的二进制。对于高玩选手，可以自己进行编译，有关编译细节，请查阅相关文档。

3. 赋予执行权限：

```bash
chmod +x miaospeed-linux-amd64-<版本号>
```

4. 启动

这是一个通用的启动例子

```bash
./miaospeed-linux-amd64-<版本号> server -bind 127.0.0.1:8765 -path miaospeed -token 123123N2e{Q?W -mtls
```

对应koipy的后端配置：

```yaml
slaveConfig: # 后端配置
  slaves: # 后端列表，注意是数组类型
    - type: miaospeed # 固定值，目前只这个支持
      id: "localmiaospeed" # 后端id
      token: "123123N2e{Q?W" # 连接密码
      address: "127.0.0.1:8765" # 后端地址
      path: "/miaospeed" # websocket的连接路径，只有路径正确才能正确连接，请填写复杂的路径，防止路径被爆破。可以有效避免miaospeed服务被网络爬虫扫描到.
      skipCertVerify: true # 跳过证书验证，如果你不知道在做什么，请写此默认值
      tls: true # 启用加密连接，如果你不知道在做什么，请写此默认值
      invoker: "114514" # bot调用者，请删掉此行或者随便填一个字符串
      buildtoken: "MIAOKO4|580JxAo049R|GEnERAl|1X571R930|T0kEN" # 默认编译token  如果你不知道在做什么，请写此默认值
      comment: "本地miaospeed后端" # 后端备注，显示在bot页面的
      hidden: false # 是否隐藏此后端
      option: # 可选配置
        downloadDuration: 8 # 测试时长
        downloadThreading: 4 # 测速线程
        downloadURL: https://dl.google.com/dl/android/studio/install/3.4.1.0/android-studio-ide-183.5522156-windows.exe # 测速文件
        pingAddress: https://cp.cloudflare.com/generate_204 # 延迟测试地址
        pingAverageOver: 3 # ping多少次取平均
        stunURL: udp://stun.ideasip.com:3478 # STUN地址，测udp连通性的
        taskRetry: 3 # 后端任务重试
```

## 可选参数

你可以用:

```bash
./miaospeed-linux-amd64-<版本号> server -help
```

来查看更多启动参数

### -path

websocket的连接路径，只有路径正确才能正确连接，请填写复杂的路径，防止路径被爆破。可以有效避免miaospeed服务被网络爬虫扫描到.

### -nospeed

禁用测速

### -connthread

测试连接的并发数量，此参数会影响测脚本的速度，最大为64，最小为1，默认16

### -speedlimit

后端测速每秒所能占用的带宽，默认无限制，单位为字节,例如限速100兆(12.5MB/秒)换算字节得到13107200

### -verbose

显示更多的日志

### -whitelist

botid白名单，设置后只允许白名单内的主端botid连接。多个值以逗号隔开。

### -pausesecond

每次任务结束的休息时间，默认不休息&#x20;

### -serverprivatekey

覆写内置的miaospeed TLS证书对应的私钥，PEM格式

### -serverpublickey

覆写内置的miaospeed TLS证书，PEM格式

## -tasklimit

测速队列的任务限制数量，超过此值将会拒绝测速，默认1000

## -allowip

主端连接IP白名单，支持IP段设置。默认允许全部IP连接即 0.0.0.0/0 和 ::/0

## -mmdb

重定向所有GEOIP查询的优先级为mmdb数据库

参数例子:  -mmdb GeoLite2-ASN.mmdb,GeoLite2-City.mmdb
