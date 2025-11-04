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

## bot.ipv6

{% tabs %}
{% tab title="解释" %}
1. 启用IPV6连接，对于某些地区网络连通性可能有优化，但也可能是负面效果，默认不启用（false）
{% endtab %}

{% tab title="特性" %}
1. 类型： bool
2. 启用后仅使用ipv6连接到TG，不会回落到ipv4
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
bot: #此行不需要重复写，配置文件有一行就行
  ipv6: false #启用的话改成 true
```
{% endcode %}
{% endtab %}
{% endtabs %}

## bot.antiGroup

{% tabs %}
{% tab title="解释" %}
1. 是否开启防拉群功能。bot运行期间，非管理员的拉群行为会提示，然后bot会自行退出那个群
2. 开启后可以防止未经过同意把测试bot拉入其他群造成困扰
{% endtab %}

{% tab title="特性" %}
1. 类型： bool
2. 如果bot没有运行，无法在软件层面阻止拉群，但是可以通过@botfather 进行设置一律不允许加入群组
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
bot: #此行不需要重复写，配置文件有一行就行
  antiGroup: false #启用的话改成 true
```
{% endcode %}
{% endtab %}
{% endtabs %}

## bot.strictMode

{% tabs %}
{% tab title="解释" %}
1. 是否启用严格模式，在此模式下，bot的所有按钮只能触发消息对话的那个人点，否则是全体用户权限均可点击。默认 **false**
2. 严格模式会对bot的执行策略产生影响，具体查看‘特性’一栏
3. 严格模式产生的背景是，一个bot的按钮操作可以帮新手进行，这在/invite的操作流程得以体现。
{% endtab %}

{% tab title="特性" %}
1. 类型： bool
2. 严格模式下还会对订阅其中的代理类型进行检测和过滤，过滤其中不支持的代理类型。采用白名单模式，白名单目前维护在程序内部，会根据Clash（mihomo）版本迭代更新。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
bot: #此行不需要重复写，配置文件有一行就行
  strictMode: false #启用的话改成 true
```
{% endcode %}
{% endtab %}
{% endtabs %}

## bot.bypassMode

{% tabs %}
{% tab title="解释" %}
1. 是否将bot设置为旁路模式，设置为旁路模式后，bot原本内置的所有指令都将失效。取而代之仅生效下面bot.commands配置的指令。
2. 关于旁路模式有什么用，请查阅：[旁路模式](https://koipy.gitbook.io/koipy/doc/yi-pang-lu-mo-shi-yun-xing-bot)
{% endtab %}

{% tab title="特性" %}
1. 类型： bool
2. 旁路模式可以使用同一个bot-token运行多个bot实例，这在多客户端实现配合中往往有奇效。例如，有其他测试bot实现了基本测试功能，可使用koipy bot进行功能补充，互不影响。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
bot: #此行不需要重复写，配置文件有一行就行
  bypassMode: false #启用的话改成 true
```
{% endcode %}
{% endtab %}
{% endtabs %}

## bot.parseMode

{% tabs %}
{% tab title="解释" %}
1. bot的文本解析模式。决定bot在发送消息或者处理消息时以什么格式进行处理
2. 可选值如下： \[DEFAULT, MARKDOWN, HTML, DISABLED]
   1. MARKDOWN 使用markdown语法进行解析
   2. HTML 使用html语法进行解析
   3. DEFAULT 以上两者混合模式，即都支持
   4. DISABLED 禁用文本解析
{% endtab %}

{% tab title="特性" %}
1. 类型： str
2. 此配置的默认值为：DEFAULT&#x20;
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
bot: #此行不需要重复写，配置文件有一行就行
  parseMode: "MARKDOWN"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## bot.cacheTime

{% tabs %}
{% tab title="解释" %}
1. 订阅缓存的最大时长
2. bot有订阅拉取缓存机制，当从远程地址获取一个订阅时，会先检查之前有没有缓存，如果有就不会重复请求获取。这种机制可以优化测试体验，让测试更丝滑。
{% endtab %}

{% tab title="特性" %}
1. 类型： int
2. 此配置的默认值为：60  ，单位秒
3. 值为负数时配置不生效
4. 目前订阅缓存保存在内存中，未来会支持保存在外部数据库中
5. 从TG获取的订阅文件也支持缓存
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
bot: #此行不需要重复写，配置文件有一行就行
  cacheTime: 60
```
{% endcode %}
{% endtab %}
{% endtabs %}

## bot.echoLimit

{% tabs %}
{% tab title="解释" %}
1. 限制bot响应消息的频率
2. 如果bot短时间内响应大量无用消息，这会造成更多的计算资源浪费，产生类似DDOS的效果。开启后可以过滤大量重复性或者超过响应频率的消息。
{% endtab %}

{% tab title="特性" %}
1. 类型： int
2. 此配置的默认值为：0.8  ，单位秒
3. 值为负数时配置不生效
4. 默认每0.8秒内只会响应一次消息，超过限制时bot不会在前端做出任何回应
5. 触发限制时会写入消息到后台日志
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
bot: #此行不需要重复写，配置文件有一行就行
  echoLimit: 0.8
```
{% endcode %}
{% endtab %}
{% endtabs %}

## bot.inviteBlacklistURL

{% tabs %}
{% tab title="解释" %}
1. 当使用/invite指令时，会对本次测试进行黑名单匹配，如果命中，则不允许继续测试
2. 这个配置填一个远程链接，将用来获取链接对应的文件内容
3. 文件内容应该每行为一个URL
4. 此项配置个人使用场景用不到，一般是公开群组测试时用到
{% endtab %}

{% tab title="特性" %}
1. 类型： str
2. 此配置的默认值为：[https://raw.githubusercontent.com/koipy-org/koihub/master/proxypool\_url.txt](https://raw.githubusercontent.com/koipy-org/koihub/master/proxypool_url.txt)
3. 默认值里的URL文件内容是仅供测试的，你不应该将它用作生成环境
4. 设置为 "" 空字符串代表不启用黑名单URL
5. 黑名单只会在每次启动时加载一次，热更新配置时，黑名单不会生效重新获取，需要重启bot
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
bot: #此行不需要重复写，配置文件有一行就行
  inviteBlacklistURL: "https://raw.githubusercontent.com/koipy-org/koihub/master/proxypool_url.txt"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## bot.inviteBlacklistDomain

{% tabs %}
{% tab title="解释" %}
1. 和bot.inviteBlacklistURL配置类似，但是黑名单每行是域名，表示整个域名都是invite的黑名单范围，这对禁用测试某系列公共订阅/代理提供商尤为有效
2. 此项配置个人使用场景用不到，一般是公开群组测试时用到
{% endtab %}

{% tab title="特性" %}
1. 类型： str
2. 此配置的默认值为：[https://raw.githubusercontent.com/koipy-org/koihub/master/proxypool\_domain.txt](https://raw.githubusercontent.com/koipy-org/koihub/master/proxypool_domain.txt)
3. 默认值里的URL文件内容是仅供测试的，你不应该将它用作生成环境
4. 设置为 "" 空字符串代表不启用黑名单域名
5. 黑名单只会在每次启动时加载一次，热重载配置时，黑名单不会生效重新获取，需要重启bot
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
bot: #此行不需要重复写，配置文件有一行就行
  inviteBlacklistDomain: "https://raw.githubusercontent.com/koipy-org/koihub/master/proxypool_domain.txt"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## bot.autoResetCommands

{% tabs %}
{% tab title="解释" %}
1. 是否自动重置bot固定的指令
2. 在bot.commands的配置中，自定义指令在设置固定(commands\[x].pin)时默认不会清除原有固定指令，此项配置可以改变此行为，让其每次设置指令是都先清除一遍原有指令
3. 之所以有这个考虑，是因为[旁路模式](https://koipy.gitbook.io/koipy/doc/yi-pang-lu-mo-shi-yun-xing-bot)下，不同bot实例之间可能会互相设置指令，如果贸然清除原有固定的指令，可能会产生意想不到的bug
{% endtab %}

{% tab title="特性" %}
1. 类型： bool
2. 此配置的默认值为：false
3. 此配置生效时机是在启动bot固定指令时，热重载配置也不会生效，需要重启bot
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
bot: #此行不需要重复写，配置文件有一行就行
  autoResetCommands: false
```
{% endcode %}
{% endtab %}
{% endtabs %}



##

