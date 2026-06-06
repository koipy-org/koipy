# 自定义指令

如果你不满足于现有指令，可以 DIY 自己的专属测试指令。下面会一步步说明常见的使用场景。

## 配置样例

如果要自定义指令，这是一份配置样例：

```yaml
bot:
  commands: # bot的指令设置
    - name: "ping" # 指令名称
      enable: true # 是否启用该指令，默认 true。未启用时，无法使用该指令
      rule: "ping" # 将该指令升级为测试指令，写对应的规则名，会读取你配置好的规则，读取不到则判定该指令为普通指令，而非测试指令。普通指令相当于 /help /version 这些，等于仅修改描述文本，而无实际测试功能
      pin: true # 是否固定指令，固定指令后会始终显示在 TG 客户端的指令列表中，默认 false
      text: "" # 指令的提示文本，默认空时自动使用name的值
      attachToInvite: true # 是否附加到 invite 指令中选择的按钮，让 invite 也能享受到此规则背后的 script 选择，默认 true
```

## 指令是否启用

该值影响这条指令能否工作

## 升级为测试指令

如果 `commands[0].rule` 被设置，那么 bot 会认为这是一个测试指令，测试指令可以发起测试任务。会读取规则名对应的规则，如果你知道什么是规则，请查看：

{% content-ref url="guan-yu-gui-ze/" %}
[guan-yu-gui-ze](guan-yu-gui-ze/)
{% endcontent-ref %}

⚠️ 注意，如果规则里面设置有 url，将会应用此 url 作为节点解析链接，不受 `rule.owner` 所有者保护，意味着所有用户权限均可以测。

## 固定在 TG 前端页面

类似于这样的效果：

![固定在 TG 前端页面](../.gitbook/assets/image%20%2811%29.png)

## 附加到 invite 的按钮中

可实现这样的效果：

![附加到 invite 的按钮中](../.gitbook/assets/image%20%2812%29.png)

