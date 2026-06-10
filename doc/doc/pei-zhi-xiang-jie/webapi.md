---
description: 这里的配置用于启用内置 Web 配置 API。
---

# webapi

这一页说明内置 Web 配置 API。当前源码里它主要提供 `/api/*` 配置读写接口，适合配合本地面板或你自己的工具使用。

<details>

<summary>webapi</summary>

{% code expandable="true" %}
```yaml
webapi:
  enable: false
  address: 127.0.0.1:8899
  password: ""
  tls: false
  tlsCertFile: ""
  tlsKeyFile: ""
  allowOrigins:
    - http://127.0.0.1:8899
    - http://localhost:8899
    - https://127.0.0.1:8899
    - https://localhost:8899
```
{% endcode %}

</details>

{% hint style="warning" %}
`webapi.enable=true` 之后，`webapi.password` 也必须是非空字符串。当前实现会直接拒绝启动一个“无密码”的管理 API。
{% endhint %}

## webapi.enable

{% tabs %}
{% tab title="解释" %}
1. 这项配置用于启用 koipy 内置的 Web 配置 API 服务。
2. 服务会在 bot 启动初始化阶段一起启动，不是单独的外部进程。
3. 关闭时，相关监听端口和 `/api/*` 接口都不会启动。
{% endtab %}

{% tab title="特性" %}
1. 类型：`bool`
2. 默认值：`false`
3. 只有在 `enable=true` 且 `password` 非空时，服务才会真正监听端口。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
webapi:
  enable: true
  password: "change-this-password"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## webapi.address

{% tabs %}
{% tab title="解释" %}
1. 这项配置用于指定 API 服务监听地址。
2. 当前解析器支持多种写法：`host:port`、纯端口号、完整 URL、IPv6 地址（例如 `[::1]:8899`）。
3. 如果你写的是完整 URL，它只会被用来提取主机和端口；真正使用 `http` 还是 `https`，仍然由 `webapi.tls` 决定。
{% endtab %}

{% tab title="特性" %}
1. 类型：`str`
2. 默认值：`127.0.0.1:8899`
3. 如果只写 `8899`，当前实现会自动绑定到 `127.0.0.1:8899`。
4. 空值或非法值最终会回退到默认地址。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
webapi:
  enable: true
  address: "[::1]:8899"
  password: "change-this-password"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## webapi.password

{% tabs %}
{% tab title="解释" %}
1. 这是管理 API 的访问密码。
2. 当前接口鉴权方式是请求头 `X-Access-Password`，没有用户名这一层。
3. `/api/health` 是唯一默认不要求密码的接口，方便做健康检查。
{% endtab %}

{% tab title="特性" %}
1. 类型：`str`
2. `enable=true` 时必须非空，否则服务拒绝启动。
3. 同一IP请求在 60 秒内连续认证失败达到 8 次后，会被临时锁定 300 秒。
4. 建议使用强随机密码，不要直接暴露到公网。
5. 暴露到公网时请配合反向代理（Nginx、Caddy等）使用，否则后果自负
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
webapi:
  enable: true
  password: "a-very-long-random-password"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## webapi.tls / tlsCertFile / tlsKeyFile

{% tabs %}
{% tab title="解释" %}
1. 这三项用于把管理 API 从 `http` 切到 `https`。
2. 当 `tls=true` 时，`tlsCertFile` 必填；`tlsKeyFile` 可选，如果证书文件里已经包含私钥，可以留空。
3. 当前实现会把相对路径按 `config.yaml` 所在目录解析，而不是按浏览器当前目录解析。
4. 如果证书文件不存在、私钥文件不存在，或 TLS 上下文构建失败，服务会直接启动失败。
{% endtab %}

{% tab title="特性" %}
1. 类型：`bool` + `str`
2. 默认值：`tls=false`、`tlsCertFile=""`、`tlsKeyFile=""`
3. `address` 写成 `https://127.0.0.1:9443` 本身不会自动开启 TLS，仍然需要 `tls=true`。
4. 如果你启用了 HTTPS，浏览器端跨域来源也要同步改成 `https://...`。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
webapi:
  enable: true
  address: "127.0.0.1:9443"
  password: "change-this-password"
  tls: true
  tlsCertFile: "./certs/webapi.pem"
  tlsKeyFile: "./certs/webapi.key"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## webapi.allowOrigins

{% tabs %}
{% tab title="解释" %}
1. 这是浏览器跨域访问时的 CORS 白名单。
2. 当前实现按 `Origin` 精确匹配，`协议 + 主机 + 端口` 必须完全一致。
3. 如果你把前端页面放到了别的域名、端口，或者把 `address` 改掉了，这里通常也要同步修改。
{% endtab %}

{% tab title="特性" %}
1. 类型：`list[str]`
2. 默认值是 4 个本地回环地址：`127.0.0.1` / `localhost` 的 `http` 与 `https` 版本。
3. `"*"` 在当前实现里会被直接忽略，并记录一条不安全配置警告。
4. 它只影响浏览器跨域请求，不影响本机 `curl` 或同源请求。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
webapi:
  enable: true
  address: "127.0.0.1:9443"
  password: "change-this-password"
  tls: true
  tlsCertFile: "./certs/webapi.pem"
  tlsKeyFile: "./certs/webapi.key"
  allowOrigins:
    - "https://127.0.0.1:9443"
    - "https://localhost:9443"
    - "https://panel.example.com"
```
{% endcode %}
{% endtab %}
{% endtabs %}
