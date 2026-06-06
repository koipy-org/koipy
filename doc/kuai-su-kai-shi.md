# 快速开始

## 前提

**没有一丁点的计算机知识，建议放弃，建议放弃，建议放弃。**

首先需要准备以下信息：

* 去 [@BotFather](https://t.me/BotFather) 创建一个机器人，获得该机器人的 `bot_token`，应形如：

  ```text
  bot_token = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
  ```

  这步不会请 Google。

可选信息：

⚠️ koipy 从 1.2 版本开始内置 `api_hash`、`api_id`，你仅需要 `bot_token` 即可开始玩耍。当然你想用自己的 API 也可以。

* Telegram 的 `api_id`、`api_hash` [获取地址](https://my.telegram.org/apps)，不会请 Google。（部分 TG 账号已被拉黑，无法正常使用，尝试更换代理 IP，IP 干净成功率高，用机场节点就自求多福吧🙃）

## 配置文件

在项目根目录创建 `config.yaml`。

以下是最基本的必需配置：

```yaml
license: xxxxxxxxxxx  # 激活码，必填。否则无法使用
bot:
  bot-token: 123456:abcdefg  # bot 的 token，首次启动必填，替换你自己的
  # api-id:  # Telegram 的 api_id 选填
  # api-hash:  # Telegram 的 api_hash 选填
```

v1.9.1 版本开始支持环境变量：

```bash
KOIPY_LICENSE=激活码
KOIPY_BOT_TOKEN=bot-token
KOIPY_BOT_PROXY=bot运行代理

export KOIPY_LICENSE=激活码
```

激活码获取请查看：

{% content-ref url="ji-huo.md" %}
[ji-huo.md](ji-huo.md)
{% endcontent-ref %}

首次启动会加载一些资源文件。如果需要代理加速，请在配置文件中加上：

```yaml
# config.yaml
network:  # 网络
  httpProxy: "http://host:port"  # http 代理，如果设置的话，bot 会用这个拉取订阅
  socks5Proxy: "socks5://host:port"  # socks5 代理，bot 的代理在下面 bot 那一栏填
# 如果 bot 需要代理：
bot:
  proxy: socks5://127.0.0.1:11112  # socks5 代理
  bot-token: 123456:abcdefg  # bot 的 token，首次启动必填，替换你自己的
  # proxy: http://127.0.0.1:11112  # http 代理也支持
  # api-id:  # Telegram 的 api_id 选填
  # api-hash:  # Telegram 的 api_hash 选填
```

## 常规启动

以下操作均在 Linux 的 bash 环境下运行，提示找不到命令请自行安装对应软件包。

解压打包好的文件：

```bash
unzip koipy-linux-amd64.zip
```

赋予执行权限并执行：

```bash
sudo chmod +x koipy && ./koipy
```

## Docker启动

挂载配置文件启动：

```bash
docker run -itd \
--name=koipy-app \
--network=host \
--restart=always \
-v ./config.yaml:/app/config.yaml \
koipy/koipy
```

* arm64 架构镜像：

```bash
docker run -itd \
--name=koipy-app \
--network=host \
--restart=always \
-v ./config.yaml:/app/config.yaml \
koipy/koipy:arm64
```

{% hint style="info" %}
Windows 用户注意

在 Windows 上使用 Docker 时，需要自己解决网络路由问题，否则可能无法连接后端。
{% endhint %}

检查是否成功启动：

```bash
docker logs -f koipy-app
```

不出意外你将看到类似提示：

![](.gitbook/assets/image%20%2810%29.png)

更多配置设置请查看：

{% content-ref url="pei-zhi-mu-ban.md" %}
[pei-zhi-mu-ban.md](pei-zhi-mu-ban.md)
{% endcontent-ref %}

{% content-ref url="doc/pei-zhi-xiang-jie/" %}
[pei-zhi-xiang-jie](doc/pei-zhi-xiang-jie/)
{% endcontent-ref %}

更多配置细节请查看配置模板页。

## 快速体验

想要立马开测看看效果？

参阅：

{% content-ref url="doc/miaospeed-hou-duan/kuai-su-ti-yan.md" %}
[kuai-su-ti-yan.md](doc/miaospeed-hou-duan/kuai-su-ti-yan.md)
{% endcontent-ref %}

