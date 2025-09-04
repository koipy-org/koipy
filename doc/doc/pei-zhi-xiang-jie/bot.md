---
description: 此项是bot的核心配置，决定了能否让bot成功运行
---

# bot

bot作为一个大项，它下面拥有许多子配置，其中有一些会特别说明：

```yaml
bot:
  bot-token: null # bot的token, 首次启动必填
  api-id:  # telegram的 api_id 可选，想用自己的api可以填，默认内置
  api-hash:  # telegram的 api_hash 可选， 可选，想用自己的api可以填，默认内置
  proxy: socks5://127.0.0.1:11112 # socks5代理
  ipv6: false #是否使用ipv6连接
  antiGroup: false
  strictMode: false # 严格模式，在此模式下，bot的所有按钮只能触发消息对话的那个人点，否则是全体用户权限均可点击。默认false
  bypassMode: false # 是否将bot设置为旁路模式，设置为旁路模式后，bot原本内置的所有指令都将失效。取而代之仅生效下面bot.commands配置的指令。关于旁路模式有什么用，请查阅在线文档。
  parseMode: MARKDOWN # bot的文本解析模式，可选值如下： [DEFAULT, MARKDOWN, HTML, DISABLED]
  scriptText: "" # 进度条文本
  analyzeText: ""  # 分析进度条文本
  speedText: "" # 速度进度条文本
  bar: "=" # 进度条
  bleft: "[" # 进度条
  bright: "]" # 进度条
  bspace: "  " # 进度条
  inviteGroup: [] # invite指令权限覆写群组白名单，写上对应群组id，那个群所有人都将可以使用/invite指令，默认只能用户权限使用。 群组id以-100开头
  cacheTime: 60 # 订阅缓存的最大时长，默认60秒。一个订阅不会重复拉取，在60秒内使用缓存值，超过60秒重新获取。
  inviteBlacklistURL: [] # 邀请测试里禁止测试的URL链接远程更新地址，多个用逗号隔开。样例： https://raw.githubusercontent.com/koipy-org/koihub/master/proxypool_url.txt
  inviteBlacklistDomain: [] # 邀请测试里禁止测试包含的域名远程更新地址，多个用逗号隔开。样例：https://raw.githubusercontent.com/koipy-org/koihub/master/proxypool_domain.txt
  commands: # bot的指令设置
    - name: "ping" # 指令名称
      enable: true # 是否启用该指令， 默认true。未启用时，无法使用该指令
      rule: "ping" # 将该指令升级为测试指令，写对应的规则名，会读取你配置好的规则，读取不到则判定该指令为普通指令，而非测试指令。普通指令相当于 /help /version 这些，等于仅修改描述文本，而无实际测试功能
      pin: true # 是否固定指令，固定指令后会始终显示在TG客户端的指令列表中，默认false
      text: "" # 指令的提示文本，默认空时自动使用name的值
      attachToInvite: true # 是否附加到invite指令中选择的按钮，让invite也能享受到此规则背后的script选择，默认true
    - name: "nf"
      rule: "nf"
      enable: true
      pin: false # 不固定指令时，相当于隐藏指令，只有你自己知道
```

## bot.api-id 与 bot.api-hash

这两项配置是成对绑定的，要么不填，要么都填。

你可以前往[这里](https://my.telegram.org/auth?to=apps)获取自己api-id和api-hash

koipy程序内部维护了自己的api-id和api-hash，所以你只需要填入bot-token即可开始玩耍。当然你也可以使用自己api。

⚠️注意

api-id和api-hash属于**敏感信息**，请勿泄露。一旦泄露，TG账号被注销也无法重置！

## bot.bot-token

关于bot-token，需要注意的是，koipy会使用bot-token在首次启动时生成一个 .seesion后缀文件，它相当于bot的会话密钥，它生成在koipy的工作目录，文件名为: my\_bot.session。它同样是敏感文件，请勿泄露。

这个文件存在时，每次bot重启将会直接读取这里的文件内容作为登录凭据，而不会重新生成。这有助于提升bot的启动速度。因此，当你想要重新生成session会话文件时，请先删除原来生成的。

## bot.proxy

你是否位于中国大陆等对Telegram访问受限的地区？

那么这项配置就很有帮助，它可以让你通过socks5或http代理来访问Telegram，前提是你的代理服务器能连上Telegram。

格式如下:&#x20;

```
socks5://username:password@hostname:port
http://myusername:mypassword@proxy.example.com:8080
```

socks5代理例子:

```yaml
bot:
 proxy: socks5://127.0.0.1:7890
```

需要身份认证的代理：

```yaml
bot:
 proxy: socks5://user1:123456@127.0.0.1:7890
```

http代理例子:

```yaml
bot:
 proxy: http://127.0.0.1:7891
```

## bot.inviteGroup

此项配置让 /invite指令的权限范围从用户降低到游客，但仅限你填入的群组id里的群组人员使用。群组id均为-100开头，TG群组id的获取请Google搜索

单个群组:

```yaml
bot:
 inviteGroup:
 - -1001111111111
```

多个群组:&#x20;

```yaml
bot:
 inviteGroup:
 - -100222222222
 - -100333333333
```
