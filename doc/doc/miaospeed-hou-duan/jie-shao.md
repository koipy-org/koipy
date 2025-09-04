# 介绍

miaospeed是一款开源的通用代理服务器测试工具，它基于前后端模式运行，它作为后端实现，通常以websocket服务器后端运行。

Github仓库如下（已停止维护）：

{% @github-files/github-code-block url="https://github.com/miaokobot/miaospeed" %}

由于作者于2024年正式对项目进行归档，不再进行维护。所以我们推荐使用还在维护的miaospeed分支：

* 本项目在维护的分支（完全兼容）：

{% @github-files/github-code-block url="https://github.com/AirportR/miaospeed" %}

* moshaoli分支（兼容）：

{% @github-files/github-code-block url="https://github.com/moshaoli688/miaospeed" %}

* paimonhub（兼容存疑？）：

{% @github-files/github-code-block url="https://github.com/Paimonhub/miaospeed_community" %}

支持测试的出站代理协议有：

| 代理协议               | 代理实现上游             |
| ------------------ | ------------------ |
| SOCKS (4/4a/5)     | Mihomo(Clash.Meta) |
| HTTP(S)            | Mihomo(Clash.Meta) |
| Shadowsocks        | Mihomo(Clash.Meta) |
| Vmess              | Mihomo(Clash.Meta) |
| Trojan             | Mihomo(Clash.Meta) |
| Snell（v1\~v3）      | Mihomo(Clash.Meta) |
| VLESS              | Mihomo(Clash.Meta) |
| TUIC               | Mihomo(Clash.Meta) |
| Hysteria/Hysteria2 | Mihomo(Clash.Meta) |
| Wireguard(需自主编译后端) | Mihomo(Clash.Meta) |
| ShadowsocksR（即将弃用） | Mihomo(Clash.Meta) |
| Mieru              | Mihomo(Clash.Meta) |
| SSH                | Mihomo(Clash.Meta) |
| AnyTLS             | Mihomo(Clash.Meta) |

