# 指令参数

koipy的大部分用于测试的指令，如 /test /speed /uspeed /topo /invite /re 等，都支持以下扩展形式：

/test?\<option1=value1>&\<option2=value2>

目前支持以下option和value组合:

```markdown
s=<后端id> 后端选择，可写多个，详见下文「多后端指定」
slave=<后端id>  同上效果
sg=<后端id>  同上效果，可写多个
slaves=<后端id>  同上效果，可写多个
r=<规则名> 直接指定要使用的规则，（还在开发，敬请期待）
sort=<排序字符串> 排序字符串就是选择按钮显示的那些
include=<正则文本> 包含过滤器
exclude=<排除文本> 排除过滤器
duration=<整数> 单个节点测速的测速时长，范围 1~60
d=<整数>  duration 的短别名
thread=<整数>  测速线程指定
t=<整数>  thread 的短别名
script=<脚本名> 指定测试项，多个用逗号隔开
output=<image/json/video> 输出测试结果的格式，默认输出图片
realtime=<true/false> 是否实时渲染测试结果，默认false
nocvt=<true/false> 是否临时禁用订阅转换，不论是否在配置里设置了订阅转换，默认false
```

排序字符串有以下值：

```
订阅原序
HTTP升序
HTTP降序
平均速度升序
平均速度降序
最大速度升序
最大速度降序
RTT升序
RTT降序
```

为方便手打，排序字符串还支持以下简写：

```
origin / o       订阅原序
h / http         HTTP升序
rh / rhttp       HTTP降序
as / aspeed      平均速度升序
ras / arspeed / raspeed   平均速度降序
ms / mspeed      最大速度升序
rms / rmspeed / mrspeed   最大速度降序
rtt              RTT升序
rrtt             RTT降序
```

例如 `sort=o` 表示订阅原序。

## 多后端指定

从 v2.0.0 起支持多后端联测。指定多个后端有两种写法，效果相同：

```
/test?s=local&s=jp-1 订阅名
/test?s=local,jp-1 订阅名
```

也可以使用 `slaves=` 或 `sg=`：

```
/test?slaves=local,jp-1 订阅名
```

重复的后端 id 会被自动去重。

## 特性

* 如果在指令里提前指定了后端id，那么不会弹出选择后端页面
* 如果在指令里提前指定了排序方式，那么不会弹出选择排序页面
* 其他参数若指定，则会覆写后端配置里的默认值
* `duration` 只有在 1~60 之间才会被接受，超出的值会被忽略
* `output=video` 只适合单后端、含测速项、节点数不过大的任务；不满足条件时会回退到 `image`
* 访客模式下不允许实时渲染，`realtime=true` 会被直接拒绝
* 无法在公开群使用类似这样带有bot名字的指令：/invite@koipybot?s=local\&sort=订阅原序 ，需改成：/invite?s=local\&sort=订阅原序
