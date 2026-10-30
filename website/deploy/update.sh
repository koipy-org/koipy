#!/usr/bin/env bash
# koipy 文档站：拉取仓库最新内容 -> 构建 -> 原子切换 web 目录
#
# 建议由 systemd timer 每分钟触发（见 deploy/koipy-docs.timer），
# 也可以手动执行或挂到 CI / webhook 上。
set -euo pipefail

REPO_DIR="${REPO_DIR:-/opt/koipy}"          # 仓库克隆位置
SITE_SUBDIR="${SITE_SUBDIR:-website}"        # 站点子目录
WEB_ROOT="${WEB_ROOT:-/var/www/koipy-docs}"  # nginx 的 root
BRANCH="${BRANCH:-master}"
REGISTRY="${REGISTRY:-https://registry.npmmirror.com}"

BUN="${BUN:-$(command -v bun || true)}"
if [ -z "$BUN" ]; then
  for candidate in /root/.bun/bin/bun /usr/local/bin/bun "$HOME/.bun/bin/bun"; do
    [ -x "$candidate" ] && BUN="$candidate" && break
  done
fi
[ -n "$BUN" ] || { echo "找不到 bun，请先安装：https://bun.sh" >&2; exit 1; }

log() { printf '[%s] %s\n' "$(date '+%F %T')" "$*"; }

cd "$REPO_DIR"
git fetch --prune origin "$BRANCH"
LOCAL="$(git rev-parse HEAD)"
REMOTE="$(git rev-parse "origin/$BRANCH")"

if [ "$LOCAL" = "$REMOTE" ]; then
  log "已是最新（${LOCAL:0:7}），跳过"
  exit 0
fi

log "发现更新 ${LOCAL:0:7} -> ${REMOTE:0:7}"
git pull --ff-only origin "$BRANCH"

cd "$REPO_DIR/$SITE_SUBDIR"

# 依赖没装过、或 package.json 更新过才重新装
if [ ! -d node_modules ] || [ package.json -nt node_modules ]; then
  log "安装依赖"
  "$BUN" install --registry "$REGISTRY"
fi

log "构建"
"$BUN" run build

# 原子切换，避免构建过程中出现半成品
NEW="$WEB_ROOT.new"
rm -rf "$NEW"
mkdir -p "$(dirname "$WEB_ROOT")"
cp -r .vitepress/dist "$NEW"
[ -d "$WEB_ROOT" ] && mv "$WEB_ROOT" "$WEB_ROOT.old"
mv "$NEW" "$WEB_ROOT"
rm -rf "$WEB_ROOT.old"

log "部署完成（$(git -C "$REPO_DIR" rev-parse --short HEAD)）"
