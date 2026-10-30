# koipy 文档站

VitePress 站点。**这里是文档的唯一真源**，日常只改这个目录。

仓库里的 `doc/` 是旧的 GitBook 文档，已经停止更新，仅作为迁移来源保留（只读，不要动）。

## 目录结构

```
website/
├── .vitepress/
│   ├── config.mts        # 站点配置：导航、侧边栏、搜索
│   ├── sidebar.json      # 侧边栏（手工维护，也可由迁移脚本生成）
│   └── theme/            # 默认主题 + 少量自定义样式
├── public/               # 静态资源（logo、favicon、文档配图）
├── scripts/
│   ├── import-from-gitbook.mjs   # 一次性迁移工具（会覆盖 md，谨慎）
│   └── lib/common.mjs
├── deploy/               # 服务器部署套件
├── index.md              # 首页
├── doc/                  # 正文（配置详解 / 指令详解 / …）
└── *.md                  # 快速开始、配置模板、激活、友情链接
```

## 本地开发

```bash
cd website
bun install            # 首次
bun run dev            # http://localhost:5173，改 md 实时热更新
bun run build          # 产物在 .vitepress/dist
bun run preview        # 预览构建结果
```

> 依赖锁定 `vitepress@2.0.0-alpha.21`，和仓库根目录无关，服务器上装出来的版本与本地一致。
> 内网/代理环境装不动的话加镜像：`bun install --registry https://registry.npmmirror.com`

## 发布流程

```bash
# 1. 改 md（或新增页面，记得同步 .vitepress/sidebar.json）
# 2. 本地构建自检：死链会直接让构建失败（ignoreDeadLinks: false）
bun run build
# 3. 提交推送，服务器自动拉取重建
git add website && git commit -m "docs: ..." && git push
```

新增页面时三件事：

1. 在 `doc/` 下新建 `xxx.md`
2. 在 `.vitepress/sidebar.json` 里加条目（`link` 写 `/doc/xxx`，不带扩展名）
3. 需要的话在 `.vitepress/config.mts` 的 `nav` 里加入口

## 服务器部署

见 `deploy/README.md`。核心是 `deploy/update.sh`：拉取 → 构建 → 原子切换，
由 systemd timer 每分钟触发，效果就是「push 后一分钟内自动上线」。

## 写作约定

- 站内链接用绝对路径：`[配置模板](/pei-zhi-mu-ban)`、`[network](/doc/pei-zhi-xiang-jie/network)`
- 目录首页写 `index.md`，链接写 `/doc/xxx/`
- 图片放 `public/assets/`，引用 `/assets/xxx.png`
- 提示块用 VitePress 容器：`::: tip 提示` / `::: warning 注意` / `::: danger 警告`
- 表格、代码块、任务列表都是标准 Markdown，直接写
