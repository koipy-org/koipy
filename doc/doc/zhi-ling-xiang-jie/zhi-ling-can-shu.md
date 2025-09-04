# 指令参数

koipy的大部分用于测试的指令，如 /test /speed /invite /re 等，都支持以下扩展形式：

/test?\<option1=value1>&\<option2=value2>

目前支持以下option和value组合:

```markdown
slave=<后端id> 后端选择
s=<后端id>  同上效果
sort=<排序字符串> 排序字符串就是选择按钮显示的那些
include=<正则文本> 包含过滤器
exclude=<排除文本> 排除过滤器
duration=<整数> 单个节点测速的测速时长
thread=<整数>  测速线程指定  
output=<json/image> 输出测试结果的格式，默认输出图片，可用值：["image", "json"]
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
最大速度降序
最大速度降序
```

## 特性

* 如果在指令里提前指定了后端id，那么不会弹出选择后端页面
* 如果在指令里提前指定了排序方式，那么不会弹出选择排序页面
* 其他参数若指定，则会覆写后端配置里的默认值
* 无法在公开群使用类似这样带有bot名字的指令：/invite@koipybot?s=local\&sort=订阅原序 ，需改成：/invite?s=local\&sort=订阅原序
