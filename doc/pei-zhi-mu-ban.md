# 配置模板

1. 以下是 koipy 启动配置文件模板，内容按最新版本整理。
2. 这页只做当前模板的镜像说明，不再作为历史模板的长期参考。
3. 如果你要开始测试，请至少配置一个后端。后端可以是本地，也可以是远程服务器。

<details>

<summary>config.yaml</summary>



```yaml
# 文档地址，有疑问先看文档：https://koipy.gitbook.io/koipy
license: "YOUR_LICENSE_CODE" # 激活码，必填，否则无法使用。
admin: # 管理员，可以不填，不填删掉。首次启动自动设置管理员。
- 12345678
network: # 网络配置
  httpProxy: "http://host:port" # http代理，如果设置的话，bot会用这个拉取订阅
  socks5Proxy: "socks5://host:port" # socks5代理， bot的代理在下面bot那一栏填
  userAgent: "ClashMetaForAndroid/2.8.9.Meta Mihomo/0.16" # UA设置，影响订阅获取
webapi: # Web 配置管理面板（可选）
  enable: false # 是否启用内置 Web 配置 API 服务，默认 false
  address: 127.0.0.1:8899 # 监听地址（host:port）
  password: "" # 访问密码。若设置，Web 端需输入访问密码后才能读写配置
  tls: false # 是否启用 HTTPS（TLS）
  tlsCertFile: "" # TLS 证书文件（PEM）。当 tls=true 时必填
  tlsKeyFile: "" # TLS 私钥文件（PEM）。可选，若证书文件已包含私钥可留空
  allowOrigins: # 允许跨域的来源列表
  - http://127.0.0.1:8899
  - http://localhost:8899
  - https://127.0.0.1:8899
  - https://localhost:8899
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
    # 特殊情况说明：1. 当name=invite的内置规则 enable=false attachToInvite=false rule=任意，会禁用内置的invite按钮
    # 2. 当name=invite的内置规则 enable=true attachToInvite=true rule=任意，text=任意，即可更改内置invite按钮的文本
    # 3. 当name=invite的内置规则 enable=true attachToInvite=true rule=invite内置规则 ，会复写内置invite的规则，后台会有DEBUG日志提示
    # 内置invite规则名称：['test', 'analyze', 'speed', 'full', 'ping', 'udptype', 'uspeed']
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
image:
  speedFormat: "byte/decimal" # 速度结果绘图格式，共有以下可用值： ["byte/binary", "byte/decimal", "bit/binary", "bit/decimal"] 具体解释请查看文档
  color: # 颜色配置
    background: # 背景颜色
      inbound: # 入口背景
        alpha: 255 # 透明度
        end-color: '#ffffff' # 透明度
        label: 0 # 值
        name: '' # 名称随意
        value: '#ffffff'
      outbound: #出口背景
        alpha: 255
        end-color: '#ffffff'
        label: 0
        name: ''
        value: '#ffffff'
      script: # 连通性测试图
        alpha: 255
        end-color: '#ffffff'
        label: 0
        name: ''
        value: '#ffffff'
      scriptTitle: # 连通性图标题栏颜色
        alpha: 255
        end-color: '#ffffff'
        label: 0
        name: ''
        value: '#EAEAEA'
      speed: # 速度图内容颜色
        alpha: 255
        end-color: '#ffffff'
        label: 0
        name: ''
        value: '#ffffff'
      speedTitle: # 速度图标题栏颜色
        alpha: 255
        end-color: '#ffffff'
        label: 0
        name: ''
        value: '#EAEAEA'
      topoTitle: # 拓扑图标题栏颜色
        alpha: 255
        end-color: '#ffffff'
        label: 0
        name: ''
        value: '#EAEAEA'
    delay: # 延迟配色
    - label: 1 # 延迟的值， >1 就采用这个颜色 单位ms
      name: '1'
      value: '#e4f8f9'
    - label: 50 # 延迟的值， >50 就采用这个颜色 单位ms
      name: '2'
      value: '#e4f8f9'
    - label: 100 # 以此类推
      name: '2'
      value: '#bdedf1'
    - label: 200
      name: '3'
      value: '#96e2e8'
    - label: 300
      name: '4'
      value: '#78d5de'
    - label: 500
      name: '5'
      value: '#67c2cf'
    - label: 1000
      name: '6'
      value: '#61b2bd'
    - label: 2000
      name: '7'
      value: '#466463'
    - label: 0
      name: '8'
      value: '#8d8b8e'
    ipriskHigh: # ip风险非常高的颜色
      alpha: 255
      end-color: '#ffffff'
      label: 0
      name: ''
      value: '#ffffff'
    ipriskLow: # ip风险最低的颜色
      alpha: 255
      end-color: '#ffffff'
      label: 0
      name: ''
      value: '#ffffff'
    ipriskMedium: # ip风险其他颜色同理
      alpha: 255
      end-color: '#ffffff'
      label: 0
      name: ''
      value: '#ffffff'
    ipriskVeryHigh:
      alpha: 255
      end-color: '#ffffff'
      label: 0
      name: ''
      value: '#ffffff'
    na: # na的颜色
      alpha: 255
      end-color: '#8d8b8e'
      label: 0
      name: ''
      value: '#8d8b8e'
    'no': # 解锁失败的颜色
      alpha: 255
      end-color: '#ee6b73'
      label: 0
      name: ''
      value: '#ee6b73'
    outColor: []
    speed: # 速度值颜色
    - label: 0.0
      name: '1'
      value: '#fae0e4'
      alpha: 255
      end_color: '#ffffff'
    - label: 0.0
      name: '2'
      value: '#f7cad0'
      alpha: 255
      end_color: '#ffffff'
    - label: 25.0
      name: '3'
      value: '#f9bec7'
      alpha: 255
      end_color: '#ffffff'
    - label: 50.0
      name: '4'
      value: '#ff85a1'
      alpha: 255
      end_color: '#ffffff'
    - label: 100.0
      name: '5'
      value: '#ff7096'
      alpha: 255
      end_color: '#ffffff'
    - label: 150.0
      name: '6'
      value: '#ff5c8a'
      alpha: 255
      end_color: '#ffffff'
    - label: 200.0
      name: '7'
      value: '#ff477e'
      alpha: 255
      end_color: '#ffffff'
    wait:
      alpha: 255
      end-color: '#dcc7e1'
      label: 0
      name: ''
      value: '#dcc7e1'
    warn:
      alpha: 255
      end-color: '#fcc43c'
      label: 0
      name: ''
      value: '#fcc43c'
    'yes':
      alpha: 255
      end-color: '#bee47e'
      label: 0
      name: ''
      value: '#bee47e'
    'xline': # x轴线条颜色
      value: '#E1E1E1'
    'yline': # y轴线条颜色
      value: '#EAEAEA'
    'font': # 字体颜色
      value: '#000000'
  compress: false # 是否压缩
  emoji: # emoji是否开启，建议开启，就这样设置
    enable: true
    source: TwemojiLocalSource
  endColorsSwitch: false
  font: ./resources/alibaba-Regular.otf #字体路径
  speedEndColorSwitch: false # 是否开启渐变色
  invert: false # 是否将图片取反色，与透明度模式不兼容，开启此项透明度将失效
  save: true # 是否保存图片到本地，设置为false时，图片将不会保存到本地，默认保存到本地备份(true)
  pixelThreshold: 2500x3500 # 图片像素阈值，超过阈值则发送原图，否则发送压缩图片，发送压缩图有助于让TG客户端自动下载图片以提升视觉体验。格式：宽的像素x高的像素，例如：2500x3500
  title: 节点测试机器人 # 绘图标题
  logo: true # 是否在绘图的类型中显示协议相关的logo
  watermark: # 水印
    alpha: 32 # 透明度
    angle: -16.0 # 旋转角度
    color: # 颜色
      alpha: 16
      end-color: '#ffffff'
      label: 0
      name: ''
      value: '#000000'
    enable: true #是否启用
    row-spacing: 0 # 行间距
    shadow: false # 暂时未实现
    size: 64 # 水印大小
    start-y: 0 # 开始坐标
    text: koipy # 水印内容
    trace: false # UID追踪开启，测试图结果显示任务发起人的UID，同时会在TG客户端发送图片时打上关联UID的tag
  nonCommercialWatermark: # 非商用水印
    alpha: 16
    angle: -16.0
    color:
      alpha: 16
      end-color: '#ffffff'
      label: 0
      name: ''
      value: '#000000'
    enable: false
    row-spacing: 1
    shadow: false
    size: 64
    start-y: 0
    text: 请勿用于商业用途
    trace: false
runtime: # 测速任务可以动态调整的配置
  entrance: true # 是否显示入口IP段
  duration: 10 # 测速时长，优先级高于后端单独设置的测速时长
  ipstack: true # 是否启用双栈检测
  localip: false # 暂时无用
  nospeed: false # 暂时无用
  pingURL: https://www.gstatic.com/generate_204 # 延迟测试地址
  speedFiles: # 速度测试的大文件下载地址，写多个地址后，在后端设置里 option.DownloadURL="DYNAMIC:ALL" 表示用runtime.speedFiles里随机一个地址
  - https://dl.google.com/dl/android/studio/install/3.4.1.0/android-studio-ide-183.5522156-windows.exe
  speedNodes: 300 # 最大测速节点数量
  speedThreads: 4 # 后端测速线程数量，优先级高于后端单独设置的
  output: image # 输出类型，目前支持 image 和 json 和 video 三种，其中video如果你用的不是docker镜像启动的，需要自己单独安装 ffmepg，然后设置好 ffmepg 的环境变量
  realtime: false # 是否实时渲染测试结果
  disableSubCvt: false # 是否针对单次测试禁用订阅转换，默认false。开启后，假如全局订阅转换开启，则单次测试不会进行订阅转换。配合rule或者指令参数使用
  protectContent: false # bot输出的所有图片设置为保护内容，默认false。设置为 true后，bot输出的图片不允许进行转发，复制。
  enableDNSInject: false # 是否启用 mihomo DNS 注入。开启后会读取订阅中的 dns 字段并编码成 mihomo://base64... 插入到后端 dnsServer 第一项。
scriptConfig:
  scripts: # 脚本载入
    - type: gofunc # 表示是miaospeed的内置实现
      name: "TEST_PING_RTT" # 特殊保留名称，当设置为这些特殊保留值时会覆写程序内部的默认配置，更多的特殊保留值请参阅这里: https://github.com/airportr/miaospeed/blob/master/interfaces/matrix.go#L3
      rank: -100 # 排序
    - type: gojajs # 表示miaospeed主流脚本类型
      name: "示例脚本" # 脚本名称
      rank: 0 # 排序，越小排在越前面
      content: | # 脚本内容
        const C_NA = '142,140,142';
        const C_UNL = '186,230,126';
        const C_FAIL = '239,107,115';
        const C_UNK = '92,207,230';

        function handler() {
          return {
              text: '失败',
              background: C_UNK,
          }
        }
    - type: gojajs
      name: "Youtube"
      rank: 0
      content: "resources/scripts/builtin/youtube.js" # 也可以指定一个文件路径
    - type: gojajs
      name: "Disney+"
      rank: 1
      content: "resources/scripts/builtin/disney+.js"
    - type: gojajs
      name: "OpenAI"
      rank: 2
      content: "resources/scripts/builtin/openai.js"
    - type: gojajs
      name: "Tiktok"
      rank: 3
      content: "resources/scripts/builtin/tiktok.js"
    - type: gojajs
      name: "维基百科"
      rank: 4
      content: "resources/scripts/builtin/wikipedia.js"
    - type: gojajs
      name: "Claude"
      rank: 5
      content: "resources/scripts/builtin/Claude.js"
    - type: gojajs
      name: "Bilibili"
      rank: 6
      content: "resources/scripts/builtin/bilibili.js"
    - type: gojajs
      name: "微软Copilot"
      rank: 7
      content: "resources/scripts/builtin/copilot.js"
    - type: gojajs
      name: "Spotify"
      rank: 8
      content: "resources/scripts/builtin/spotify.js"
    - type: gojajs
      name: "Viu"
      rank: 9
      content: "resources/scripts/builtin/viu.js"
    - type: gojajs
      name: "IP风险"
      rank: 11
      content: "resources/scripts/builtin/iprisk.js"
    - type: gojajs
      name: "DNS区域"
      rank: 10
      content: "resources/scripts/builtin/dns.js"
# 以下为固定脚本名称，用于覆写内置的GEOIP脚本，脚本名称不可更改：
#    - type: gojajs
#      name: "GEOIP_INBOUND"
#      rank: 0
#      content: "YOUR_GEOIP_SCRIPT" # 默认的GEOIP脚本参见 https://github.com/AirportR/miaospeed/blob/master/engine/embeded/default_geoip.js
slaveConfig: # 后端配置
  healthCheck: # checkslave 后端健康检查配置
    numSamples: 10 # 健康检查样本数量，单位整数次数，默认采样10次PING测试数据
    showStatusStyle: "default" # 在后端选择页面展示状态的样式，共有以下可用值： ["emoji", "number", "default"]，分别代表：展示emoji、展示延迟、不展示，默认default不展示
    autoHideOnFailure: false # 健康检查失败时是否自动隐藏后端，默认false。
  showID: true # 是否在选择后端页面展示slaveid
  # 后端测速任务的调度模式，共有以下可用值：["concurrent", "pipeline", "sequential"]，默认pipeline，分别代表：
  # 1. 并发模式（所有后端同时开始测速）
  # 2. 流水线模式（当第一个测速后端测完第一个节点，第二个后端才开始发送测速任务，以此类推）
  # 3. 串行模式（前一个后端全部测完后下一个才开始）
  speedScheduling: pipeline
  geoClustering: true # 是否开启拓扑结果的聚类排序，默认为true。开启后会将结果相同或相近的后端排列在一起，提高绘图时的单元格合并率，使图片更整洁。
  slaves: # 后端列表，注意是数组类型
    - type: miaospeed # 固定值，目前只这个支持
      id: "localmiaospeed" # 后端id
      token: "ZfffaQ4/E-7S" # 连接密码
      address: "127.0.0.1:8765" # 后端地址
      path: "/" # websocket的连接路径，只有路径正确才能正确连接，请填写复杂的路径，防止路径被爆破。可以有效避免miaospeed服务被网络爬虫扫描到.
      skipCertVerify: true # 跳过证书验证，如果你不知道在做什么，请写此默认值
      tls: true # 启用加密连接，如果你不知道在做什么，请写此默认值
      invoker: "1114514" # bot调用者，请删掉此行或者随便填一个字符串
      buildtoken: "MIAOKO4|580JxAo049R|GEnERAl|1X571R930|T0kEN" # 默认编译token  如果你不知道在做什么，请写此默认值
      comment: "本地miaospeed后端" # 后端备注，显示在bot页面的
      hidden: false # 是否隐藏此后端
      # proxy: http://username:password@proxy.example.com:7890 # 为此后端设置专门的http代理（暂时仅支持http代理）
      option: # 可选配置，请注意部分值设置得太大会不生效，比如taskTimeout设置成10000以上，就不会生效。
        downloadDuration: 8 # 测试时长
        downloadThreading: 4 # 测速线程
        downloadURL: https://dl.google.com/dl/android/studio/install/3.4.1.0/android-studio-ide-183.5522156-windows.exe # 测速大文件，有一个特殊值：DYNAMIC:ALL，表示随机选择一个下载地址，随机选择列表需要在runtime.speedFiles里或rule.runtime.speedFiles里设置。
        pingAddress: https://cp.cloudflare.com/generate_204 # 延迟测试地址
        pingAverageOver: 3 # ping多少次取平均
        stunURL: udp://stunserver2025.stunprotocol.org:3478 # STUN地址，测udp连通性的，格式: udp://host:port
        taskRetry: 3 # 后端任务重试，单位秒(s)
        taskTimeout: 2500 # 后端任务超时判定时长，单位毫秒(ms)
        dnsServer: [] # 后端指定dns服务器，解析节点域名时会用到。例子: ["119.29.29.29:53", "223.5.5.5:53"]，也支持DoH格式的域名，例如：["https://dns.google/dns-query"]
        # dnsServer 也支持 mihomo的dns配置（后端版本至少为 4.6.5），经过base64编码后会发送给后端，后端支持解析： mihomo://ZG5zOgogIGVuYWJsZTogdHJ1ZQogIGRlZmF1bHQtbmFtZXNlcnZlcjoKICAgIC0gMjIzLjUuNS41
        apiVersion: 1 # 后端Api版本，设置为 0或者1可以适配旧版后端兼容性，默认为1，如无必要请勿修改。如果要对接其他分支miaospeed请设置为0或者1
        uploadURL: https://speed.cloudflare.com/__up # 旧版/其他分支不兼容，apiVersion=3 独有配置，上行速度测试的自定义URL
        uploadDuration: 8 # 旧版/其他分支不兼容，apiVersion=3 独有配置。上行速度测试的测速时长
        uploadThreading: 4 # 旧版/其他分支不兼容，apiVersion=3 独有配置。上行速度测试的测速线程
rules:
  - name: 订阅名1 # 规则名称
    url: https://www.google.com  # 订阅链接
    owner: 1111111111 # 规则创建者
    slaveid: [local] # 写你在后端配置里设置的后端id，如果用数组形式写多个后端id，就代表为多后端联测。
    runtime: null # 支持主配置runtime的所有值
    script: [] # 写你在后端配置里设置的脚本配置名称，也支持预保留的名称TEST_PING_RTT等
  - name: 订阅名2 # 规则名称2
    url: https://www.google2.com  # 订阅链接
    owner: 2222222222 # 规则创建者
subconverter: # 订阅转换对接配置，可以把base64格式转换bot测试需要的Clash格式
  enable: false # 是否启用
  mode: subconverter # 可选 subconverter / substore，仅用于推断默认 Host/Port/Target
  # subconverter 功能详情：https://github.com/tindy2013/subconverter
  # sub-store 功能详情：https://github.com/sub-store-org/Sub-Store
  template:
    backend: "http://$Host:$Port/sub?target=$Target&new_name=true&url=$EncodedURL"
    # sub-store 模板样例: "http://$Host:$Port/download/sub?target=$Target&url=$EncodedURL"
    # 协议兼容性提示：
    #   subconverter 对 anytls:// 等新协议可能直接丢弃（返回空 proxies）
    #   sub-store 对 anytls:// 可用，建议 target=ClashMeta
    # 占位符说明（推荐在 query 参数里使用 Encoded 版本）：
    #   $URL / $EncodedURL: 原始订阅链接 / URL编码后的订阅链接
    #   [强提醒] 当链接作为 query 参数值传递时（如 ...&url=XXX），请使用 $EncodedURL
    #            若误用 $URL，内层链接中的 ? & # % + 等字符会破坏外层参数解析，导致链接截断或失效
    #            示例：...&url=$EncodedURL  (推荐)
    #            示例：...&url=$URL         (仅在你确认无特殊字符时才可用，不推荐)
    #   $Content / $EncodedContent: 与 URL 同义，兼容部分后端(sub-store)参数名
    #   $Host / $Port / $Scheme: 后端地址参数（来自 defaults）
    #   $Target: 转换目标（来自 defaults.target）
    #   $Mode: 当前 mode 值（subconverter 或 substore）
    #   $Key / $EncodedKey: 读取 defaults.<Key> 的原值/编码值，键名大小写不敏感
    # 例如 defaults 里写 ua: clash-verge，可在模板里用 $UA 或 $EncodedUA
  defaults:
    target: ClashMeta
    # 可选：host/port/scheme 以及你自定义的任意键
    # 默认值规则：
    #   host 默认 127.0.0.1
    #   port 默认 25500；如果模板包含 /download/sub，默认端口会推断为 3000
    #   scheme 默认取 template.backend 的 scheme；模板没写 scheme 时回落到 http
    #   target 默认 clash；若 mode=substore 或模板包含 /download/sub，默认 ClashMeta
#callbacks: # http回调功能支持
#  onMessage: http://127.0.0.1:8080/onMessage # 回调地址，bot收到消息时,会向此地址发送POST请求，使用方法请看文档
#  onPreSend: http://127.0.0.1:8080/onPreSend # 回调地址，bot处理所有任务的前置动作后（比如选定后端、选定规则等），会向此地址发送POST请求，来完成一些操作，使用方法请看文档
#  onResult: http://127.0.0.1:8080/onResult # 回调地址，bot接受完测试结果后，会向此地址发送POST请求，可以用来添加/修改结果数据，使用方法请看文档
translation: # 翻译语言包
  lang: zh-CN # 启用哪个语言包，填的值为下面resources配置的键，默认zh-CN
  resources: # 翻译包在哪加载
    zh-CN: ./resources/i18n/zh-CN.yml # 键随便填，值填文件路径，文件内容格式为yaml，具体请看文档
log-level: INFO # 日志文件日志等级，共有以下日志等级： [DEBUG, INFO, WARNING, ERROR, CRITICAL, DISABLE]，越后的等级日志越严重，DISABLE会禁用日志文件，日志存放在logs目录下。控制台日志等级不受此配置影响，始终为DEBUG等级
user: [] # 用户权限名单，不用自己设，推荐使用 /grant 指令添加用户权限

```

</details>
