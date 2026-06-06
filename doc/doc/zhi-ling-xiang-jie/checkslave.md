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

