# 导入语言包

只需要在配置文件中设置语言包路径：

```yaml
translation: # 翻译语言包
  lang: zh-CN # 系统要使用的语言包
  resources: # 翻译包在哪加载
    zh-CN: ./resources/localization/zh-CN.yml # 键随便填，值填文件路径
```

`resources` 下可以同时配置多个语言包，`lang` 决定实际使用哪一个。

## 切换与刷新

修改 `lang` 后无需重启，使用管理员指令 `/lang` 即可在已加载的语言包之间切换。切换会就地刷新所有模块引用的文本，日志中会输出 `refresh_lang` 对应的提示。

{% hint style="info" %}
`/lang` 只能在程序**启动时已加载**的语言包之间切换，语言包内容也是启动时一次性读入内存的。因此无论是新增 `resources` 条目，还是修改语言包文件本身，都需要**重启程序**才会生效。
{% endhint %}
