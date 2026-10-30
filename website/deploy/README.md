# 服务器部署

目标：`git push` 之后一分钟内网站自动更新，全程不用手动登服务器。

## 一次性准备

```bash
# 1. 装 bun（构建用）
curl -fsSL https://bun.sh/install | bash
# 国内网络可换镜像：https://gitee.com/mirrors/bun 或直接用 npm 装 bun

# 2. 克隆仓库
git clone https://github.com/koipy-org/koipy.git /opt/koipy

# 3. 首次构建，确认能跑通
cd /opt/koipy/website
bun install --registry https://registry.npmmirror.com
bun run build
```

## 配置 nginx

```bash
cp deploy/nginx.conf /etc/nginx/conf.d/koipy-docs.conf
# 改 server_name 和 root
nginx -t && systemctl reload nginx
```

注意 `try_files $uri $uri.html $uri/ =404;` 不能少——站点开了 `cleanUrls`，
`/kuai-su-kai-shi` 实际对应 `kuai-su-kai-shi.html`。

## 开启自动更新

```bash
chmod +x /opt/koipy/website/deploy/update.sh

cp /opt/koipy/website/deploy/koipy-docs.service /etc/systemd/system/
cp /opt/koipy/website/deploy/koipy-docs.timer   /etc/systemd/system/

systemctl daemon-reload
systemctl enable --now koipy-docs.timer

# 看效果
systemctl list-timers koipy-docs.timer
journalctl -u koipy-docs.service -f
```

`update.sh` 的逻辑：`git fetch` 比对 HEAD，没变化直接退出（几乎零开销）；
有变化才 `git pull` → 装依赖（package.json 变了才装）→ 构建 → 原子切换目录。

可调环境变量：`REPO_DIR` `SITE_SUBDIR` `WEB_ROOT` `BRANCH` `REGISTRY` `BUN`。

## 手动触发一次

```bash
systemctl start koipy-docs.service
```

## 换成 GitHub Actions / webhook

如果不想让服务器轮询，把 `update.sh` 挂到 push 触发的 CI 里即可，
或者服务器跑一个轻量 webhook（如 `adnanh/webhook`）收到 GitHub 推送后执行同一脚本。

## 常见问题

| 现象 | 原因 |
| --- | --- |
| 页面 404 | nginx 少了 `$uri.html` 回退 |
| 构建报 dead link | 站内链接写错，`ignoreDeadLinks: false` 会直接失败 |
| 依赖装不动 | 加 `--registry https://registry.npmmirror.com` |
| 更新了但页面没变 | HTML 被缓存，检查 nginx 的 `Cache-Control` 配置 |
