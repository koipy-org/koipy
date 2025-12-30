---
description: 这里的配置是关于绘图的
---

# image

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

## image.speedFormat

速度结果绘图格式，共有以下可用值： \["byte/binary", "byte/decimal", "bit/binary", "bit/decimal"]

解释如下：

```
byte/decimal 速度单位为兆字节/秒，并且使用人类可读的单位换算
绘图显示的速度单位为兆字节/秒，并且使用人类可读的十进制单位换算，例如 1000MB/s ==> 1GB/s ，
绘图会省略 /s，最后的结果为 1000MB ==> 1GB

bit/decimal 速度单位变成Mbps 兆比特每秒，并且换算基数为十进制，如：1000Mbps ==> 1Gpbs
byte/binary 速度单位变成MB/s 兆字节每秒，并且换算基数为二进制，如：1024MB ==> 1GB
bit/binary 速度单位变成Mbps 兆比特每秒，并且换算基数为二进制，如：1024Mbps ==> 1Gpbs
```

为什么有这个格式区别？

1. 传统计算机科学使用: 1024 (2^10) 作为换算基数。这种方法被称为二进制前缀。
2. 网络和存储设备制造商通常使用: 1000 作为换算基数。这种方法被称为十进制前缀。

在网络测速软件中：

* 大多数测速软件使用 1000 作为基数。这是因为网络速度通常以比特（bit）为单位，而不是字节（byte）。网络设备制造商和互联网服务提供商（ISP）也倾向于使用这种方式。
* 例如，当测速软件显示 100 Mbps（兆比特每秒）时，它通常表示 100,000,000 比特每秒，而不是 104,857,600 比特每秒。

当然koipy的默认值为byte/decimal，以确保与主流测速软件显示一致。
