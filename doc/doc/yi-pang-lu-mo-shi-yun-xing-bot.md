# 以旁路模式运行bot

## 解释

旁路模式只是本项目对该功能的称呼，也可以叫消息透传、回调透传等。它的主要特点是可以让多个实例进程同时运行 bot。

## 原理

由于 bot 自身开发框架的优势，使用 MTProto 协议可以在多个 Telegram API 上运行 bot 实例。这意味着可以用同一个 bot-token 同时开多个主端，并且互不影响。但多个主端同时存在时，同一个指令会出现多次响应，于是需要让不同的 bot 实例只响应不重复的指令，旁路模式就此出现。

以旁路模式运行时，用户可以自定义当前实例进程启用的 bot 指令，未被启用的指令将不会响应。从内部机制上看，它是禁用了该指令的响应触发条件。

## 用法

想要启用旁路模式很简单，在配置中加入以下内容：

```yaml
bot:
  bypassMode: true # 是否将 bot 设置为旁路模式。启用后，bot 原本内置的所有指令都将失效，只生效下面 bot.commands 配置的指令。
```

## 效果

启动旁路模式后，只会对当前实例进程配置中的自定义指令生效。例如：

```yaml
bot:
  commands:
    - name: ping
      pin: true
      text: 📶 进行延迟测试
      rule: ping
      attachToInvite: false
      enable: true # 设置为 true，且处于旁路模式时，该指令会响应。
    - name: speed
      enable: false # 设置为 false，且处于旁路模式时，该指令不会响应
```

## 多开Bot

如果你有进一步需求，可以多开 bot 实例。具体做法是把 bot 程序所在文件夹原封不动地复制一份，然后在配置文件里更改 `bot.api-hash` 与 `bot.api-id`。

