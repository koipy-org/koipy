---
description: 这里的配置是关于绘图与结果文件输出的。
---

# image

这一页说明绘图相关配置。

<details>

<summary>image</summary>

{% code expandable="true" %}
```yaml
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
```
{% endcode %}

</details>

## image.speedFormat

{% tabs %}
{% tab title="解释" %}
1. 决定绘图中上行速度、下行速度的显示单位与换算基数。
2. 只有 4 个可选值：`["byte/binary", "byte/decimal", "bit/binary", "bit/decimal"]`。
3. 当值非法时，源码会自动回退到 `byte/decimal`。

```text
byte/decimal  速度单位按字节显示，基数 1000，例如 1000MB -> 1GB
byte/binary   速度单位按字节显示，基数 1024，例如 1024MB -> 1GB
bit/decimal   速度单位按比特显示，基数 1000，例如 1000Mbps -> 1Gbps
bit/binary    速度单位按比特显示，基数 1024，例如 1024Mbps -> 1Gbps
```
{% endtab %}

{% tab title="特性" %}
1. 类型：`str`
2. 该配置不仅影响文字显示，也影响速度柱状图内部的换算基数。
3. 主流测速软件通常偏向十进制，因此模板默认值是 `byte/decimal`。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
image:
  speedFormat: "byte/decimal"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## image.title

{% tabs %}
{% tab title="解释" %}
1. 绘图标题前缀。
2. 实际显示时，源码会把它拼接成 `image.title - 当前任务名`。
3. 当任务带有站点标识时，标题末尾还会追加 `| 站点名`。
{% endtab %}

{% tab title="特性" %}
1. 类型：`str`
2. 如果完全不写，程序内部默认值是 `Koipy`。
3. 这项配置只影响图上的标题文字，不影响 bot 指令标题或规则名称。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
image:
  title: "节点测试机器人"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## image.logo

{% tabs %}
{% tab title="解释" %}
1. 控制结果图“类型”列是否显示协议 logo。
2. 只对源码已识别的类型生效，例如：`vless`、`hysteria`、`shadowsocks`、`shadowsocksr`、`vmess`、`wireguard`、`ssh`、`sudoku`、`snell`。
3. 关闭后仍会显示文字版协议类型，只是不再绘制 logo。
{% endtab %}

{% tab title="特性" %}
1. 类型：`bool`
2. 程序内部默认值：`true`
3. 这项配置只影响绘图展示，不影响节点解析和测试结果。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
image:
  logo: true
```
{% endcode %}
{% endtab %}
{% endtabs %}

## image.pixelThreshold

{% tabs %}
{% tab title="解释" %}
1. 控制 Telegram 发送图片时，是走“照片”还是“文件”。
2. 配置格式固定为 `宽x高`，例如：`2500x3500`。
3. 最新源码中的判断条件是：
   1. 当图片宽和高都严格小于阈值时，优先按照片发送。
   2. 只要宽或高任意一边大于等于阈值，就按文件发送。
4. 按照片发送时，TG 客户端通常会更积极地自动预览与自动下载。
{% endtab %}

{% tab title="特性" %}
1. 类型：`str`
2. 程序内部默认值：`2500x3500`
3. 格式写错时，源码会回退到内部默认尺寸。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
image:
  pixelThreshold: 2500x3500
```
{% endcode %}
{% endtab %}
{% endtabs %}

## image.font

{% tabs %}
{% tab title="解释" %}
1. 指定绘图使用的字体文件。
2. 应填写一个本地字体路径，通常是 `.otf` 或 `.ttf` 文件。
3. 最新源码中，如果你填的字体文件不存在，但同路径下存在同名的 `.ttf/.otf` 对应文件，程序会自动尝试切换到那个后缀。
4. 如果字体仍无法加载，绘图阶段会退回到 PIL 的默认字体。
{% endtab %}

{% tab title="特性" %}
1. 类型：`str`
2. 程序内部默认值指向 `./resources/alibaba-Regular.otf`
3. 路径建议写成 koipy 工作目录下的相对路径，迁移环境时更方便。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
image:
  font: ./resources/alibaba-Regular.otf
```
{% endcode %}
{% endtab %}
{% endtabs %}

## image.emoji

{% tabs %}
{% tab title="解释" %}
1. 控制绘图时 emoji 的渲染方式。
2. `enable=true` 时，绘图会启用自定义 emoji 绘制源，以修复默认字体对 emoji 的兼容问题。
3. `source` 填写的是源码里导出的 emoji source 名称；如果填写了不存在的名称，源码会回退到 `TwemojiLocalSource`。
4. 当启用 `TwemojiLocalSource` 且本地尚未初始化资源包时，首次启动会自动下载资源到 `resources/emoji/twemoji`。
{% endtab %}

{% tab title="特性" %}
1. `image.emoji.enable` 类型：`bool`
2. `image.emoji.source` 类型：`str`
3. 程序内部默认值：`enable=true`、`source=TwemojiLocalSource`
4. 当前源码导出的 source 包括，但是只有 `source=TwemojiLocalSource` 经过生产环境验证：

```text
ApplePediaSource
GooglePediaSource
SamsungPediaSource
MicrosoftPediaSource
WhatsAppPediaSource
TwitterPediaSource
FacebookPediaSource
MicrosoftTeamsPediaSource
SkypePediaSource
JoyPixelsPediaSource
TossFacePediaSource
TwemojiLocalSource
OpenmojiLocalSource
```
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
image:
  emoji:
    enable: true
    source: TwemojiLocalSource
```
{% endcode %}
{% endtab %}
{% endtabs %}

## image.endColorsSwitch

{% tabs %}
{% tab title="解释" %}
1. 控制颜色块是否使用渐变。
2. 开启后，延迟块、解锁状态块、速度柱状块等会从 `value` 渐变到对应颜色对象的 `end-color`。
3. 关闭后，这些颜色块会直接使用纯色填充。
{% endtab %}

{% tab title="特性" %}
1. 类型：`bool`
2. 程序内部默认值：`false`
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
image:
  endColorsSwitch: true
```
{% endcode %}
{% endtab %}
{% endtabs %}

## image.speedEndColorSwitch

{% tabs %}
{% tab title="解释" %}
1. 这是一个保留配置项。
2. 在最新源码的主绘图流程里，没有发现单独读取 `image.speedEndColorSwitch` 的逻辑。
3. 也就是说，当前真正控制颜色块渐变的是 `image.endColorsSwitch`，不是这一项。
{% endtab %}

{% tab title="特性" %}
1. 类型：`bool`
2. 程序内部默认值：`false`
3. 目前更适合把它理解为兼容旧配置或后续扩展预留字段。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
image:
  speedEndColorSwitch: false
```
{% endcode %}
{% endtab %}
{% endtabs %}

## image.compress

{% tabs %}
{% tab title="解释" %}
1. 控制结果图是否在绘图阶段做颜色量化压缩。
2. 最新源码主流程中，开启后会把 PNG 图像量化为 256 色，以减小体积。
3. 这不会改变 TG 发送方式；发送方式仍然由 `image.pixelThreshold` 决定。
{% endtab %}

{% tab title="特性" %}
1. 类型：`bool`
2. 程序内部默认值：`false`
3. 它更像是“颜色压缩”而不是“尺寸压缩”。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
image:
  compress: true
```
{% endcode %}
{% endtab %}
{% endtabs %}

## image.invert

{% tabs %}
{% tab title="解释" %}
1. 控制图片是否反色。
2. 反色处理发生在水印绘制之后、图片保存之前。
3. 这个配置通常用于夜间模式，内置 `/nightshift` 指令切换的也是它。
{% endtab %}

{% tab title="特性" %}
1. 类型：`bool`
2. 程序内部默认值：`false`
3. 开启后，文字、背景、线条、色块都会一起参与反色。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
image:
  invert: false
```
{% endcode %}
{% endtab %}
{% endtabs %}

## image.save

{% tabs %}
{% tab title="解释" %}
1. 控制结果文件是否保留在本地。
2. 对图片和视频来说，绘图流程通常会先生成输出文件，再发送到 TG；当 `save=false` 时，发送完成后会删除本地文件。
3. 对 JSON 输出来说，`save=false` 表示只发送内存中的文档，不额外写入本地文件。
{% endtab %}

{% tab title="特性" %}
1. 类型：`bool`
2. 程序内部默认值：`true`
3. 这项配置影响的是“结果文件是否留档持久化”，不影响 TG 前端发送行为。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
image:
  save: true
```
{% endcode %}
{% endtab %}
{% endtabs %}

## image.color

{% tabs %}
{% tab title="解释" %}
1. 这是绘图配色的大项，下面包含背景色、延迟阈值配色、速度阈值配色、状态色、线条色、字体色等。
2. 大多数颜色对象都长这样：

```yaml
value: "#ffffff"      # 起始颜色
end-color: "#ffffff"  # 渐变结束颜色
alpha: 255            # 透明度
label: 0              # 阈值或保留字段
name: ""              # 保留字段
```

3. 由于 koipy 的配置加载器会自动把 YAML 中的 `-` 转成内部字段 `_`，所以 `end-color` 和 `end_color`、`row-spacing` 和 `row_spacing` 这种写法都能被识别。文档里仍然沿用模板常见的连字符写法。
{% endtab %}

{% tab title="特性" %}
1. `label` 对 `delay`、`speed` 这两类阈值列表最重要。
2. `name` 在最新主绘图逻辑里基本不参与实际绘制，更多是兼容或便于人工阅读。
3. 当 `image.endColorsSwitch=true` 时，颜色对象的 `end-color` 才会在色块渐变中体现出来。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
image:
  color:
    'yes':
      value: "#bee47e"
      end-color: "#bee47e"
      alpha: 255
    'no':
      value: "#ee6b73"
      end-color: "#ee6b73"
      alpha: 255
    font:
      value: "#000000"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## image.color.background

{% tabs %}
{% tab title="解释" %}
1. 这一组配置主要控制不同类型结果图的背景色。
2. 最新源码中，主结果图明确会读取：
   1. `background.script` 作为大背景色
   2. `background.scriptTitle` 作为标题栏和底部栏背景色
3. 在其他颜色回退场景中，还可能读取 `background.speed`、`background.inbound`、`background.outbound`。
4. `background.speedTitle` 和 `background.topoTitle` 仍然保留在配置结构中，但最新主绘图代码路径没有主动读取它们。
{% endtab %}

{% tab title="特性" %}
1. 类型：`dict`
2. 这组颜色对象通常主要使用 `value` 和 `alpha`。
3. 若你只想统一底色，通常改 `script` 与 `scriptTitle` 就够了。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
image:
  color:
    background:
      script:
        value: "#f8fafc"
        alpha: 255
      scriptTitle:
        value: "#e2e8f0"
        alpha: 255
```
{% endcode %}
{% endtab %}
{% endtabs %}

## image.color.delay

{% tabs %}
{% tab title="解释" %}
1. 控制延迟相关列的阈值配色。
2. 最新源码会先按 `label` 升序排序，再用“当前值命中最后一个不大于它的阈值”来取色。
3. 也就是说，配置顺序不一定等于最终生效顺序，真正起作用的是 `label` 数值本身。
{% endtab %}

{% tab title="特性" %}
1. 类型：`list[Color]`
2. 如果你把这一项留空，源码会回退到内部默认配色。
3. 默认阈值大致为：`0, 1, 50, 100, 200, 300, 500, 1000, 2000`。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
image:
  color:
    delay:
    - label: 0
      value: "#8d8b8e"
    - label: 50
      value: "#e4f8f9"
    - label: 200
      value: "#96e2e8"
    - label: 1000
      value: "#61b2bd"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## image.color.speed

{% tabs %}
{% tab title="解释" %}
1. 控制速度相关列和速度柱状块的阈值配色。
2. 和 `image.color.delay` 一样，源码会按 `label` 升序排序后再命中。
3. 速度值会先按 `image.speedFormat` 的换算基数解释，再决定命中哪个阈值。
{% endtab %}

{% tab title="特性" %}
1. 类型：`list[Color]`
2. 如果你把这一项留空，源码会回退到内部默认配色。
3. 程序内部默认阈值大致为：`0, 1, 10, 20, 50, 80, 100`。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
image:
  color:
    speed:
    - label: 0
      value: "#fae0e4"
    - label: 25
      value: "#f9bec7"
    - label: 100
      value: "#ff7096"
    - label: 200
      value: "#ff477e"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## image.color.yes / no / na / wait / warn

{% tabs %}
{% tab title="解释" %}
1. 这些是常见状态色：
   1. `yes`：解锁、允许、可用等正向结果
   2. `no`：失败、禁止、不可用等负向结果
   3. `na`：`N/A`
   4. `wait`：待解锁、送中等中间状态
   5. `warn`：超时、连接错误等告警状态
2. 这几项都是直接命中的固定颜色，不依赖 `label`。
{% endtab %}

{% tab title="特性" %}
1. 类型：`Color`
2. 如果开启 `image.endColorsSwitch`，这些状态块也会按 `value -> end-color` 渐变。
3. 文字颜色不受这几项控制，文字颜色由 `image.color.font` 决定。
4. 如果javascript测试脚本中返回了color字段，那么将优先选择脚本返回的颜色值
5. no 请加引号（单引号或双引号均可），否则会被yaml解释错误识别为bool类型
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
image:
  color:
    'yes':
      value: "#bee47e"
    'no':
      value: "#ee6b73"
    na:
      value: "#8d8b8e"
    wait:
      value: "#dcc7e1"
    warn:
      value: "#fcc43c"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## image.color.ipriskLow ~ image.color.ipriskVeryHigh

{% tabs %}
{% tab title="解释" %}
1. 这一组颜色用于 IP 风险结果展示。
2. 最新源码会按文本内容中的 `Low`、`Medium`、`High`、`Very` 去命中对应颜色。
3. 如果你的脚本或后端会输出 IP 风险分级，这几项就有意义；否则它们可能长期不会被命中。
{% endtab %}

{% tab title="特性" %}
1. 类型：`Color`
2. 默认模板通常把它们留成白色，需要你自己按喜好调整。
3. 和其他状态色一样，开启 `image.endColorsSwitch` 后也支持渐变。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
image:
  color:
    ipriskLow:
      value: "#d9f99d"
    ipriskMedium:
      value: "#fde68a"
    ipriskHigh:
      value: "#fca5a5"
    ipriskVeryHigh:
      value: "#ef4444"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## image.color.xline / yline / font

{% tabs %}
{% tab title="解释" %}
1. `xline` 控制横线颜色。
2. `yline` 控制竖线颜色。
3. `font` 控制标题、表头、正文、脚注等文字颜色。
{% endtab %}

{% tab title="特性" %}
1. 类型：`Color`
2. 这三项主要使用 `value` 字段。
3. `alpha`、`end-color` 在这些线条和文字主路径里通常没有明显意义。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
image:
  color:
    xline:
      value: "#E1E1E1"
    yline:
      value: "#EAEAEA"
    font:
      value: "#000000"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## image.color.outColor

{% tabs %}
{% tab title="解释" %}
1. 这是一个保留列表配置。
2. 最新源码中会解析并排序它，但主绘图流程里没有看到实际读取它来决定颜色的逻辑。
3. 因此目前不建议把关键视觉需求建立在这项配置上。
{% endtab %}

{% tab title="特性" %}
1. 类型：`list[Color]`
2. 当前更适合作为兼容旧配置或未来扩展保留。
3. 即使你填写了它，最新主绘图代码也可能完全不使用。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
image:
  color:
    outColor: []
```
{% endcode %}
{% endtab %}
{% endtabs %}

## image.watermark

{% tabs %}
{% tab title="解释" %}
1. 控制绘图水印。
2. 开启后，源码会把 `watermark.text` 以一定角度旋转后，多行平铺到图片上。
3. 如果 `trace=true`，水印文本后面会自动追加任务发起人的 `UID`。
4. 同时，在 TG 发送结果时还会额外附带 `#uid_xxx` 和 `#timestamp_xxx` 两个 tag。
{% endtab %}

{% tab title="特性" %}
1. `enable` 类型：`bool`
2. `text` 类型：`str`
3. `alpha` 类型：`int`
4. `angle` 类型：`float/int`
5. `size` 类型：`int`
6. `row-spacing` 类型：`int`
7. `start-y` 类型：`int`
8. `trace` 类型：`bool`
9. `shadow` 在最新源码里仍然没有真正实现，开启后当前主逻辑会直接返回原图，不绘制盲水印。
10. 最新源码真正用于颜色的是 `watermark.color.value`，真正用于透明度的是 `watermark.alpha`；`watermark.color.alpha` 当前主逻辑并不会拿来控制最终透明度。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
image:
  watermark:
    enable: true
    text: "koipy"
    alpha: 32
    angle: -16.0
    size: 64
    row-spacing: 0
    start-y: 0
    trace: false
    shadow: false
    color:
      value: "#000000"
```
{% endcode %}
{% endtab %}
{% endtabs %}
