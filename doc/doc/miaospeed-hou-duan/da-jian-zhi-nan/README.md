---
description: 此页将介绍具体搭建步骤
---

# 搭建指南

以下操作均使用本项目组维护的仓库，搭建环境为 Ubuntu 22.04（Linux）：

{% @github-files/github-code-block url="https://github.com/AirportR/miaospeed" %}

## 对接环境

MiaoSpeed 作为服务端（后端），需要公网 IP 或内网穿透等方式，才能让客户端（主端）连接上后端。

## 下载预编译的二进制

普通用户可以直接下载 GitHub 仓库编译好的二进制。需要自行编译的话，可以查阅相关文档。

## 赋予执行权限

```bash
chmod +x miaospeed-linux-amd64-<版本号>
```

## 启动

这是一个通用的启动示例：

```bash
./miaospeed-linux-amd64-<版本号> server -bind 127.0.0.1:8765 -path miaospeed -token 123123N2e{Q?W -mtls
```

对应 koipy 的后端配置：

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

每次任务结束的休息时间，默认不休息

### -serverprivatekey

覆写内置的miaospeed TLS证书对应的私钥，PEM格式

### -serverpublickey

覆写内置的miaospeed TLS证书，PEM格式

### -mtls

启用TLS认证（包含单向TLS和mTLS）。开启后后端默认使用TLS加密连接，后端不强制要求mTLS，是否切换到mTLS取决于客户端（主端）是否发送它的客户端证书。详见下文「mTLS 双向证书认证」。

### -upload

在此后端上启用上行速度测试。该功能默认关闭，需要显式加此参数才会开放。

{% hint style="info" %}
上行速度测试需要主端与后端版本同时支持。主端侧对应 `slave.option.apiVersion=3`，并且 `/uspeed` 指令与 `/test` 中的上行测试项都依赖后端开启 `-upload`。
{% endhint %}

### -connect

反向连接模式。加上该参数后，后端不再监听端口等待主端连接，而是主动拨出连接到 koipy。详见下文「反向连接」。

## -tasklimit

测速队列的任务限制数量，超过此值将会拒绝测速，默认1000

## -allowip

主端连接IP白名单，支持IP段设置。默认允许全部IP连接即 0.0.0.0/0 和 ::/0

## -mmdb

重定向所有GEOIP查询的优先级为mmdb数据库

参数例子:  -mmdb GeoLite2-ASN.mmdb,GeoLite2-City.mmdb

## mTLS 双向证书认证

普通的 `-mtls` 只是让主端验证后端的证书。如果你想反过来让**后端也验证主端**，也就是真正的双向认证，需要主端与后端都持有证书。

### 后端侧

启动时保留 `-mtls`，并用 `-serverpublickey` / `-serverprivatekey` 指定后端自己的证书与私钥（不改则使用内置证书）：

```bash
./miaospeed-linux-amd64-<版本号> server \
  -bind 0.0.0.0:8765 \
  -path miaospeed \
  -token 123123N2e{Q?W \
  -mtls \
  -serverpublickey /path/to/miaospeed.crt \
  -serverprivatekey /path/to/miaospeed.key
```

### 主端侧

在 koipy 的后端配置中开启 `mtls`，并提供客户端证书：

```yaml
slaveConfig:
  slaves:
    - id: "localmiaospeed"
      address: "127.0.0.1:8765"
      path: "/miaospeed"
      tls: true # 必须为 true，否则启动时报错
      mtls: true # 启用双向 TLS 客户端证书认证
      clientCertFile: "./resources/certs/client.crt" # 客户端证书，必填
      clientKeyFile: "" # 客户端私钥，证书里已包含私钥时可留空
      caCertFile: "" # 可选，为当前后端附加额外信任的 CA 证书
```

{% hint style="warning" %}
`mtls: true` 必须与 `tls: true` 同时使用。只开 `mtls` 不开 `tls`，koipy 启动时会直接报错。

`clientKeyFile` 只在证书文件里**没有**包含私钥时才需要填写。
{% endhint %}

关于 `caCertFile`：koipy 使用自己携带的 CA 证书来验证后端，不信任系统根证书。如果你的后端使用的是自签名证书，就需要通过 `caCertFile` 把它附加到 koipy 的信任列表里。

{% hint style="info" %}
mTLS 需要 miaospeed 版本不低于 **4.7.2**。
{% endhint %}

## 反向连接

通常情况是主端（koipy）主动连接后端。但如果后端位于 NAT 之后，主端无法访问到它，就可以使用反向连接：由后端主动拨入 koipy。

{% hint style="info" %}
反向连接使用的协议为 `msr-v1`，需要主端与后端版本同时支持。
{% endhint %}

### 主端侧

在 koipy 的后端配置中开启 `reverse`，并指定监听地址：

```yaml
slaveConfig:
  slaves:
    - id: "nat-backend"
      token: "123123N2e{Q?W" # 后端 -connect 时用同一个 token 签名
      reverse: true # 启用反向连接
      reverseListen: "0.0.0.0:8766" # 监听地址，留空则用默认 0.0.0.0:8766
      reverseTLS: true # 监听是否启用 TLS
      reverseCertFile: "./resources/certs/server.crt" # reverseTLS=true 时必填
      reverseKeyFile: "" # 私钥，证书里已包含时可留空
```

开启 `reverse` 后，该后端不再需要 `address` 与 `path`，也不需要能被 koipy 访问到。

### 后端侧

启动后端时加上 `-connect`，指向 koipy 的地址：

```bash
./miaospeed-linux-amd64-<版本号> server \
  -connect wss://your-koipy-host:8766/reverse \
  -token "123123N2e{Q?W"
```

`-connect` 的地址就是 koipy 侧 `reverseListen` 对应的地址与端口，路径部分可以随意填写，建议写复杂一点以防被扫描。后端会主动向该地址建立连接并保持，任务到来时直接复用。

### 注意事项

* 每个反向后端必须使用**独立的端口**，否则启动时会按后端逐个报端口冲突
* 反向连接**没有 IP 白名单**，token 就是唯一的鉴权校验。因此当监听地址暴露在公网时，务必开启 `reverseTLS`
* 开启 `reverseTLS` 后，`reverseCertFile` 指定的证书必须被**后端主机信任**（后端不会跳过证书校验）
* 后端会为每个 `-connect` 地址维持一个固定大小的连接池，并在连接异常断开后重连
