#!/usr/bin/env node
/**
 * 一次性迁移工具：把旧 GitBook 文档（../doc）转换成 VitePress 站点内容。
 *
 * ⚠️ 新文档已经是唯一真源，本脚本会覆盖 website/ 下的同名 md。
 *    除非你确实想从 GitBook 重新拉一遍，否则不要运行。
 *
 * 用法：
 *   bun scripts/import-from-gitbook.mjs --force          # 覆盖 md
 *   bun scripts/import-from-gitbook.mjs --force --sidebar # 顺便按 SUMMARY.md 重建侧边栏
 *
 * 处理：
 *  - README.md -> index.md，站内 .md 链接改写为 clean URL
 *  - .gitbook/assets/* 复制到 public/assets/*（文件名安全化）
 *  - {% hint %} / {% tabs %} / {% tab %} / {% code %} / {% content-ref %} / {% embed %}
 *    -> VitePress 容器 / 标签 / 普通链接
 */
import fs from 'node:fs'
import path from 'node:path'
import {
  ASSETS_DIR,
  KEEP_DIRS,
  KEEP_FILES,
  LEGACY_DOC_ROOT,
  SIDEBAR_FILE,
  SITE_ROOT,
  SKIP_FILES,
  decode,
  safeName,
  stripHtml,
  toSitePath,
  walk
} from './lib/common.mjs'

const FORCE = process.argv.includes('--force')
const REBUILD_SIDEBAR = process.argv.includes('--sidebar')

if (!FORCE) {
  console.error(
    '拒绝执行：新文档是唯一真源，本脚本会覆盖 website/ 下的 md。\n' +
      '确认要从 GitBook 重新迁移，请加 --force。'
  )
  process.exit(1)
}

if (!fs.existsSync(LEGACY_DOC_ROOT)) {
  console.error(`找不到旧文档目录：${LEGACY_DOC_ROOT}`)
  process.exit(1)
}

/* -------------------------------------------------- 1. SUMMARY -> sidebar */

const titleMap = new Map()

function parseSummary(md) {
  const groups = []
  let cur = { text: '开始', items: [] }
  groups.push(cur)
  const stack = []

  for (const raw of md.split(/\r?\n/)) {
    const h = raw.match(/^##\s+(.+)$/)
    if (h) {
      cur = { text: stripHtml(h[1]), items: [] }
      groups.push(cur)
      stack.length = 0
      continue
    }
    const li = raw.match(/^(\s*)[*+-]\s+\[([^\]]+)\]\(([^)\s]+)\)/)
    if (!li) continue

    const indent = li[1].replace(/\t/g, '  ').length
    const text = stripHtml(li[2])
    const link = toSitePath(li[3])
    titleMap.set(link, text)

    const item = { text, link }
    while (stack.length && stack[stack.length - 1].indent >= indent) stack.pop()
    if (stack.length) {
      const parent = stack[stack.length - 1].item
      parent.items ??= []
      parent.items.push(item)
    } else {
      cur.items.push(item)
    }
    stack.push({ indent, item })
  }

  return groups.filter((g) => g.items.length)
}

/* ------------------------------------------------------- 2. 语法转换 */

const HINT_MAP = {
  info: '::: info 说明',
  warning: '::: warning 注意',
  danger: '::: danger 警告',
  success: '::: tip 提示',
  tip: '::: tip 提示'
}

const RE = {
  hintOpen: /^\{%\s*hint\s+style="([^"]*)"\s*%\}$/,
  hintClose: /^\{%\s*endhint\s*%\}$/,
  tabsOpen: /^\{%\s*tabs\s*%\}$/,
  tabsClose: /^\{%\s*endtabs\s*%\}$/,
  tabOpen: /^\{%\s*tab\s+title="([^"]*)"\s*%\}$/,
  tabClose: /^\{%\s*endtab\s*%\}$/,
  codeOpen: /^\{%\s*code\b[^%]*%\}$/,
  codeClose: /^\{%\s*endcode\s*%\}$/,
  refOpen: /^\{%\s*content-ref\s+url="([^"]*)"\s*%\}$/,
  refClose: /^\{%\s*endcontent-ref\s*%\}$/,
  embed: /^\{%\s*embed\s+url="([^"]*)"\s*%\}$/,
  ghBlock: /^\{%\s*@github-files\/github-code-block\s+url="([^"]*)"\s*%\}$/
}

function convertGitbook(text) {
  const out = []
  let inCodeFence = false
  // {% code title="config.yaml" %} 的标题在 VitePress 里没有对应语法，
  // 塞进代码围栏的 meta（shiki 忽略未知 meta），信息不至于丢失。
  let pendingTitle = null

  for (const raw of text.split(/\r?\n/)) {
    const line = raw
    const t = line.trim()

    if (/^(```|~~~)/.test(t)) {
      if (!inCodeFence && pendingTitle) {
        out.push(`${t} title="${pendingTitle}"`)
        pendingTitle = null
      } else {
        out.push(line)
      }
      inCodeFence = !inCodeFence
      continue
    }
    if (inCodeFence) {
      out.push(line)
      continue
    }

    let m
    if ((m = t.match(RE.hintOpen))) {
      out.push(HINT_MAP[m[1]] ?? '::: tip 提示', '')
      continue
    }
    if (RE.hintClose.test(t)) {
      out.push(':::', '')
      continue
    }
    if (RE.tabsOpen.test(t) || RE.tabsClose.test(t)) continue
    if (RE.tabClose.test(t)) {
      out.push('')
      continue
    }
    if ((m = t.match(RE.tabOpen))) {
      out.push(`<p class="gb-tab">${m[1]}</p>`, '')
      continue
    }
    if ((m = t.match(RE.codeOpen))) {
      const title = t.match(/title="([^"]*)"/)
      if (title) pendingTitle = title[1]
      continue
    }
    if (RE.codeClose.test(t)) continue
    if (RE.refOpen.test(t)) {
      out.push('::: tip 相关内容', '')
      continue
    }
    if (RE.refClose.test(t)) {
      out.push('', ':::', '')
      continue
    }
    if ((m = t.match(RE.embed))) {
      out.push(`<${m[1]}>`, '')
      continue
    }
    if ((m = t.match(RE.ghBlock))) {
      out.push(`<${m[1]}>`, '')
      continue
    }

    out.push(line)
  }

  return out.join('\n')
}

/* --------------------------------------------------- 3. 链接与图片改写 */

function rewriteLinks(text, fileRel) {
  const dir = path.posix.dirname(fileRel)
  // 配图放在站点根的 assets/，md 里按自身位置写相对路径
  const assetPrefix = path.posix.relative(dir === '.' ? '' : dir, 'assets')

  return text.replace(
    /(!?)\[([^\]]*)\]\(([^()\s]+(?:\s[^()]*)?)\)/g,
    (all, bang, label, href) => {
      if (/^(?:https?:|mailto:|tel:|#|\/\/|\/)/i.test(href)) return all

      const [rawPath, anchor] = href.split('#')
      const abs = path.posix.normalize(path.posix.join(dir === '.' ? '' : dir, decode(rawPath)))

      if (bang) {
        const name = safeName(path.posix.basename(abs))
        const prefix = assetPrefix.startsWith('.') ? assetPrefix : './' + assetPrefix
        return `![${label}](${prefix}/${name})`
      }
      if (!/\.md$/i.test(abs)) return all

      const sitePath = toSitePath(abs)
      const finalLabel =
        /^[\w.\-/]+\.md$/i.test(label.trim()) && titleMap.has(sitePath)
          ? titleMap.get(sitePath)
          : label
      return `[${finalLabel}](${sitePath}${anchor ? '#' + anchor : ''})`
    }
  )
}

/* --------------------------------------------------------------- 主流程 */

function main() {
  const summaryPath = path.join(LEGACY_DOC_ROOT, 'SUMMARY.md')
  if (fs.existsSync(summaryPath)) {
    const sidebar = parseSummary(fs.readFileSync(summaryPath, 'utf-8'))
    for (const group of sidebar) {
      if (group.text === '开始') continue
      for (const item of group.items) {
        if (item.items?.length) item.collapsed = true
      }
    }
    if (REBUILD_SIDEBAR) {
      fs.writeFileSync(SIDEBAR_FILE, JSON.stringify(sidebar, null, 2), 'utf-8')
      console.log('✓ 已按 SUMMARY.md 重建侧边栏')
    }
  }

  const files = walk(LEGACY_DOC_ROOT).filter(
    (f) => f.endsWith('.md') && !SKIP_FILES.has(path.basename(f))
  )

  let converted = 0
  for (const file of files) {
    const rel = path.relative(LEGACY_DOC_ROOT, file).replace(/\\/g, '/')
    let body = fs.readFileSync(file, 'utf-8')
    body = convertGitbook(body)
    body = rewriteLinks(body, rel)

    let outRel = rel
    if (path.posix.basename(rel).toLowerCase() === 'readme.md') {
      const d = path.posix.dirname(rel)
      outRel = d === '.' ? 'index.md' : `${d}/index.md`
    }

    const target = path.join(SITE_ROOT, outRel)
    fs.mkdirSync(path.dirname(target), { recursive: true })
    fs.writeFileSync(target, body, 'utf-8')
    converted++
  }

  const assetDir = path.join(LEGACY_DOC_ROOT, '.gitbook', 'assets')
  let assets = 0
  if (fs.existsSync(assetDir)) {
    fs.mkdirSync(ASSETS_DIR, { recursive: true })
    for (const f of fs.readdirSync(assetDir)) {
      const src = path.join(assetDir, f)
      if (!fs.statSync(src).isFile()) continue
      fs.copyFileSync(src, path.join(ASSETS_DIR, safeName(f)))
      assets++
    }
  }

  console.log(`✓ 转换 ${converted} 篇文档`)
  console.log(`✓ 复制 ${assets} 个资源 -> assets/`)
  console.log(
    `  提示：KEEP_DIRS = ${[...KEEP_DIRS].join(', ')}；已存在的 ${[...KEEP_FILES].join(', ')} 不会被覆盖`
  )
}

main()
