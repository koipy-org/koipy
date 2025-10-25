# 快速开始

## 前提

**没有一丁点的计算机知识，建议放弃，建议放弃，建议放弃。**

首先需要准备以下信息：

*   去 [@BotFather](https://t.me/BotFather) 那里创建一个机器人，获得该机器人的bot\_token，应形如：

    bot\_token = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"

    这步不会请Google。

可选信息：

⚠️koipy从1.2版本开始内置api\_hash, api\_id，你仅需要bot\_token即可开始玩耍。当然你想用自己的api也可以。

* Telegram 的api\_id 、api\_hash [获取地址](https://my.telegram.org/apps) 不会请Google。(部分TG账号已被拉黑，无法正常使用，尝试更换代理IP，IP干净成功率高，用机场节点就自求多福吧🙃)

## 配置文件

在项目根目录创建config.yaml

以下是最基本的必需配置：

<pre class="language-yaml"><code class="lang-yaml"><strong>license: xxxxxxxxxxx  # 激活码，必填。否则无法使用
</strong><strong>bot:
</strong>  bot-token: 123456:abcdefg # bot的token, 首次启动必填，替换你自己的
  #api-id:  # telegram的 api_id 选填
  #api-hash:  # telegram的 api_hash 选填
</code></pre>

v1.9.1版本开始支持环境变量：

KOIPY\_LICENSE=激活码

KOIPY\_BOT\_TOKEN=bot-token

KOIPY\_BOT\_PROXY=bot运行代理

使用例子:

export KOIPY\_LICENSE=激活码

激活码获取请查看：

{% content-ref url="ji-huo.md" %}
[ji-huo.md](ji-huo.md)
{% endcontent-ref %}

首次启动会加载一些资源文件，如果需要代理加速，请在配置文件加上：

```yaml
#config.yaml
network: # 网络
  httpProxy: "http://host:port" # http代理，如果设置的话，bot会用这个拉取订阅
  socks5Proxy: "socks5://host:port" # socks5代理， bot的代理在下面bot那一栏填
# 如果bot需要代理：
bot:
  proxy: socks5://127.0.0.1:11112 # socks5代理
  bot-token: 123456:abcdefg # bot的token, 首次启动必填，替换你自己的
  #proxy: http://127.0.0.1:11112 # http代理也支持
  #api-id:  # telegram的 api_id 选填
  #api-hash:  # telegram的 api_hash 选填


```

## 常规启动

以下操作均在linux的bash环境下运行，提示找不到命令请自行安装对应软件包

解压打包好的文件:

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

检查是否成功启动：



```bash
docker logs -f koipy-app
```

不出意外你将看到类似提示：

<figure><img src=".gitbook/assets/image (10).png" alt=""><figcaption></figcaption></figure>

更多配置设置请查看：

{% content-ref url="pei-zhi-mu-ban.md" %}
[pei-zhi-mu-ban.md](pei-zhi-mu-ban.md)
{% endcontent-ref %}

{% content-ref url="doc/pei-zhi-xiang-jie/" %}
[pei-zhi-xiang-jie](doc/pei-zhi-xiang-jie/)
{% endcontent-ref %}

配置文件示例位于 ./resources/config.example.yaml

## 快速体验

想要立马开测看看效果？

