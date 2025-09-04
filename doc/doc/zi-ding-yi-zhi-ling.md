# 自定义指令

是否不满足于现有指令，你可以DIY自己的专属测试指令，接下来笔者会一步步带你了解一些使用场景



1. 配置样例

如果要自定义指令，这是一份配置样例：

```yaml
bot:
  commands: # bot的指令设置
    - name: "ping" # 指令名称
      enable: true # 是否启用该指令， 默认true。未启用时，无法使用该指令
      rule: "ping" # 将该指令升级为测试指令，写对应的规则名，会读取你配置好的规则，读取不到则判定该指令为普通指令，而非测试指令。普通指令相当于 /help /version 这些，等于仅修改描述文本，而无实际测试功能
      pin: true # 是否固定指令，固定指令后会始终显示在TG客户端的指令列表中，默认false
      text: "" # 指令的提示文本，默认空时自动使用name的值
      attachToInvite: true # 是否附加到invite指令中选择的按钮，让invite也能享受到此规则背后的script选择，默认true
```

2. 指令是否启用

该值影响这条指令能否工作

3. 升级为测试指令

如果commands\[0].rule被设置，那么bot会认为这是一个测试指令，测试指令可以发起测试任务。会读取规则名对应的规则，如果你知道什么是规则，请查看：

{% content-ref url="guan-yu-gui-ze/" %}
[guan-yu-gui-ze](guan-yu-gui-ze/)
{% endcontent-ref %}

⚠️注意，如果规则里面设置有url，将会应用此url作为节点解析链接，不受rule.owner所有者保护，意为者所有的用户权限均可以测。

4. 固定在TG前端页面

类似于这样的效果：

<figure><img src="../.gitbook/assets/image (11).png" alt=""><figcaption></figcaption></figure>

5. 附加到invite的按钮中

可实现这样的效果：

<figure><img src="../.gitbook/assets/image (12).png" alt=""><figcaption></figcaption></figure>

