# 必填配置

koipy目前需要必填两个配置项，分别是 license 和 bot-token。其中bot-token隶属于 'bot' 这一父项。



## license

koipy需要激活码（授权码）才能使用，关于如何获取激活码，请参阅：

{% content-ref url="../../ji-huo.md" %}
[ji-huo.md](../../ji-huo.md)
{% endcontent-ref %}

配置示例如下：

```yaml
license: AZpJpMwQrg3uKGl6LN67riQuqtqbCE4IuMhJwpwkkoM3GJX9SxFTw2YnpwApIlyNDwBb7DA0v_A6Ayrq3A5KfJy18AJF4ozR3tvrpqfsIZBfkGeIdesnUHVvF1vXZVwphG8NQCGT6gV28HSUmJIAmM5hStaxCLDMeCkg0Ncrdpqn08J38AM-1EKUDVnKc8kDyEaHM8_A8ECwZ3ZUuS9FhzLk6gKr0UgVHKwgeETLN8I1I01tmMsFN_hmoPlabQA0eyUkhsauB8HQ23u8ceorZlqqBeNeUtOE6A1EJK6UPEMMvqJ6EXjz46dXW7B0QUfHgTb9ODvw6kO2JMc7fwoZgyeL7nvWakBsrzOBwqLXry-38rvB8P-MF4GImsVv5ppYPKHSdyPJLSQs_2OvsxFBySQtW35k_q3rhkQqogMXo08dtrdLB2UaP3nfz6w2AF-rwY8SThIpjHZpbj-U58-NLhg2NrAVs0yC5Xw6w7ym7DGhuOF9wsUFQM_unlOY9QqvFa32QbVMNDuOnQdcyvdObi3QQg_BYFIfCV1iny2Z7sN9WmU1Oz34bQgFceMSCeQHRa2bIMq7ni2p2I3qUlE-XaIi0i9EbigrKOzDu1ro0gnobdsWkbcF2LruNvEARo6XqynlRjFEjdM8mlPNae4wYkPvTOEHusDLmXltli8brlw=.CXXs2wBVqj_pdTqSd3DDmEuOq2O5Tkh4GjEiG_UIbCDHP66cHlPAOJfss6P_HO2LcZS43mcVqBOLmkaH2lRHLw==
```

## bot.bot-token

你要生成一个Telegram bot，然后获得它的bot-token

配置bot-token如下：

```yaml
bot:
 bot-token: 123456:abcdfegsda121212121
```

你可能已经注意到了，bot-token 上面还有一行'bot' ，这是因为bot-token是在bot的这一层级下的配置。
