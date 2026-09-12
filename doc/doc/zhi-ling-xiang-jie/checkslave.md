# /checkslave

## 解释

检查后端在线情况。

## 别名

* /checkslaves

## 用法

* 检查所有后端

```
/checkslave
```

* 筛选后端 `comment` 值包含 `1Gbps` 的后端

```
/checkslave?include=1Gbps
```

* 筛选后端 `comment` 值排除 `海外` 的后端

```
/checkslave?exclude=海外
```

* 后端列表 `comment` 里包含 `1G`、排除 `电信` 关键字的后端

```
/checkslave?include=1G&exclude=电信
```

* 检查单个后端，后端 ID 为 `GDCM` 的在线情况

```
/checkslave?slave=GDCM
```

## v1.8.7 变化

此版本起将支持 `?output=<value>` 指令参数

```
/checkslave?output=image
```

可选值如下：

* `output=image`：输出结果为图片，这是默认选项
* `output=json`：输出结果为 JSON 文件
* `output=text`：输出结果为文本，属于 v1.8.7 版本以前的输出风格

## v1.12.0 变化

* 结果中会显示**后端版本**，方便你确认后端是不是需要升级。
* 后端选择页面显示的是**真延迟**，而不是握手耗时。

## 结果说明

图片结果里每个后端一行，包含以下几类信息：

* 后端备注与 id
* 网络测量指标（采样自 `slaveConfig.healthCheck.numSamples` 次 PING 数据）
* 与后端握手的延迟
* 后端版本

## 相关配置

`/checkslave` 的行为受 `slaveConfig.healthCheck` 控制：

```yaml
slaveConfig:
  healthCheck:
    numSamples: 10 # 采样次数
    showStatusStyle: "default" # 后端选择页面的状态样式：emoji / number / default
    autoHideOnFailure: false # 健康检查失败时是否自动隐藏该后端
```

{% hint style="warning" %}
反向连接（msr-v1）的后端由后端主动连接 koipy，没有可探测的地址，因此它不参与网络测量，结果里只会保留一行占位信息。
{% endhint %}

{% content-ref url="../pei-zhi-xiang-jie/slaveconfig.md" %}
[slaveconfig.md](../pei-zhi-xiang-jie/slaveconfig.md)
{% endcontent-ref %}

