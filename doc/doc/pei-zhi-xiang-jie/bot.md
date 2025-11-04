---
description: 此项是bot的核心配置，决定了能否让bot成功运行
---

# bot

bot作为一个大项，它下面拥有许多子配置，其中有一些会特别说明：

<details>

<summary>bot</summary>

```yaml
bot:
  bot-token: null # bot的token, 首次启动必填
  api-id:  # telegram的 api_id 可选，想用自己的api可以填，默认内置
  api-hash:  # telegram的 api_hash 可选，想用自己的api可以填，默认内置
  proxy: socks5://127.0.0.1:11112 # bot的代理设置，推荐socks5代理，http代理也可以，目前仅支持这两种代理
  ipv6: false #是否使用ipv6连接
  antiGroup: false # 是否开启防拉群模式，默认false
  strictMode: false # 严格模式，在此模式下，bot的所有按钮只能触发消息对话的那个人点，否则是全体用户权限均可点击。默认false
  bypassMode: false # 是否将bot设置为旁路模式，设置为旁路模式后，bot原本内置的所有指令都将失效。取而代之仅生效下面bot.commands配置的指令。关于旁路模式有什么用，请查阅在线文档。
  parseMode: MARKDOWN # bot的文本解析模式，可选值如下： [DEFAULT, MARKDOWN, HTML, DISABLED]
  inviteGroup: [] # invite指令权限覆写群组白名单，写上对应群组id，那个群所有人都将可以使用/invite指令，默认只能用户权限使用。 群组id以-100开头
  cacheTime: 60 # 订阅缓存的最大时长，默认60秒。一个订阅不会重复拉取，在60秒内使用缓存值，超过60秒重新获取。
  echoLimit: 0.8 # 限制响应速度，单位秒，默认0.8秒，即bot每0.8秒最多响应一条消息。每0.8/2秒内按钮最多响应一次
  inviteBlacklistURL: [] # 邀请测试里禁止测试的URL链接远程更新地址，多个用逗号隔开。样例： https://raw.githubusercontent.com/koipy-org/koihub/master/proxypool_url.txt
  inviteBlacklistDomain: [] # 邀请测试里禁止测试包含的域名远程更新地址，多个用逗号隔开。样例：https://raw.githubusercontent.com/koipy-org/koihub/master/proxypool_domain.txt
  autoResetCommands: false # 是否自动重置bot指令，默认false。开启后，每次启动时会清除原来固定在TG前端的指令
  commands: # bot的指令设置
    # 特殊情况说明：1. 当name=invite的内置规则 enable=false attachToInvite=ture rule=任意，会禁用内置的invite按钮
    # 2. 当name=invite的内置规则 enable=true attachToInvite=true rule=任意，text=任意，即可更改内置invite按钮的文本
    # 3. 当name=invite的内置规则 enable=true attachToInvite=true rule=invite内置规则 ，会复写内置invite的规则，后台会有DEBUG日志提示
    # 内置invite规则名称：['test', 'analyze', 'speed', 'full', 'ping', 'udptype']
    - name: "ping" # 指令名称
      title: "PING测试" # 绘图时任务标题
      enable: true # 是否启用该指令， 默认true。未启用时，无法使用该指令。
      rule: "ping" # 将该指令升级为测试指令，写对应的规则名，会读取你配置好的规则，读取不到则判定该指令为普通指令，而非测试指令。普通指令相当于 /help /version 这些，等于仅修改描述文本，而无实际测试功能
      pin: true # 是否固定指令，固定指令后会始终显示在TG客户端的指令列表中，默认false
      text: "" # 指令的提示文本，默认空时自动使用name的值
      attachToInvite: true # 是否附加到invite指令中选择的按钮，让invite也能享受到此规则背后的script选择，默认true
    - name: "nf"
      rule: "nf"
      enable: true
      pin: false # 不固定指令时，相当于隐藏指令，只有你自己知道
```

</details>

## bot.api-id 与 bot.api-hash

{% tabs %}
{% tab title="解释" %}
1. bot依赖于[MTProto协议](https://core.telegram.org/mtproto)运行，接入官方Telegram平台时需要提供开发的API，bot.api-id 与 bot.api-hash是成对绑定的，要么不填，要么都填。
2. 你可以前往[这里](https://my.telegram.org/auth?to=apps)获取自己api-id和api-hash 。但是IP最好干净，否则申请过程会提示“ERROR”
3. api-id和api-hash属于**敏感信息**，请勿泄露。一旦泄露，TG账号被注销也无法重置！
{% endtab %}

{% tab title="特性" %}
1. api-id 是整型的
2. api-hash 是字符串
3. koipy程序内部维护了自己的api-id和api-hash，所以你只需要填入bot-token即可开始玩耍，此项配置不是必须填的。当然你也可以使用自己api。
4.
{% endtab %}

{% tab title="配置示例" %}
```yaml
bot: #此行不需要重复写，配置文件有一行就行
  api-id: 123456
  api-hash: 91eda59826c80a7bee5fe80967df3253
```
{% endtab %}
{% endtabs %}

## bot.bot-token

{% tabs %}
{% tab title="解释" %}
1. bot运行所必须的通信令牌
{% endtab %}

{% tab title="特性" %}
1. 类型： str
2. koipy会使用bot-token在首次启动时生成一个 .seesion后缀文件，它相当于bot的会话密钥，它生成在koipy的工作目录，文件名为: my\_bot.session。它同样是敏感文件，请勿泄露。
3. mybot.session文件存在时，每次bot重启将会直接读取这里的文件内容作为登录凭据，而不会重新生成，这有助于提升bot的启动速度。因此，当你想要重新生成session会话文件时，请先删除原来生成的。
{% endtab %}

{% tab title="配置示例" %}
```yaml
bot: #此行不需要重复写，配置文件有一行就行
  bot-token: 123456789:AAEakOyFndt9G8kO1zmIY-UFcWpAzOXmipk
  
```
{% endtab %}
{% endtabs %}

## bot.proxy

{% tabs %}
{% tab title="解释" %}
1. 你是否位于中国大陆等对Telegram访问受限的地区？那么这项配置就很有帮助，它可以让你通过socks5或http代理来访问Telegram，前提是你的代理服务器能连上Telegram。
2. 通常情况下，socks5代理端口由Clash等代理软件提供
{% endtab %}

{% tab title="特性" %}
1. 类型： str
2. bot运行的代理类型仅支持socks5和http类型
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
bot: #此行不需要重复写，配置文件有一行就行
  proxy: socks5://username:password@hostname:port
  # 以下是http类型 
  #proxy: http://myusername:mypassword@proxy.example.com:8080
  # 对于Clash，其默认端口为7890
  #proxy: socks5://127.0.0.1:7890
  # 需要身份认证的代理
  #proxy: socks5://user1:123456@127.0.0.1:
```
{% endcode %}
{% endtab %}
{% endtabs %}

## bot.inviteGroup

{% tabs %}
{% tab title="解释" %}
1. 此项配置让 /invite指令的权限范围从用户降低到游客，但仅限你填入的群组id里的群组人员使用。群组id均为-100开头，TG群组id的获取请Google搜索
2. 群组id获取方法，在想要的群组发送/id，就会有bot给你发送相关的群组信息，其中就有群组id
3.  群组id如图所示

    <figure><img src="../../.gitbook/assets/image (22).png" alt=""><figcaption></figcaption></figure>
{% endtab %}

{% tab title="特性" %}
1. 类型： list\[int]
2. 🌟群组测试目前是赞助用户所持有，个人用户无法使用群组测试，所以这项配置对于个人无法生效。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
bot: #此行不需要重复写，配置文件有一行就行
  inviteGroup: 
  - -1001111111111 #格式注意事项，两个短横线‘-’之间有个空格
  #- -1001111111112 #第二个群组
  # 或者你也可以这么写：
  #inviteGroup: [-1001111111111,-1001111111112]

```
{% endcode %}
{% endtab %}
{% endtabs %}





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
