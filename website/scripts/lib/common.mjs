/**
 * 文档站公共工具。
 *
 * 目录约定（都在 koipy-public 仓库内）：
 *   doc/      旧 GitBook 文档（不再更新，仅作为迁移来源，只读）
 *   website/  新文档站（唯一真源，日常编辑这里）
 */
import fs from 'node:fs'
import path from 'node:path'

export const SITE_ROOT = path.resolve(import.meta.dirname, '..', '..')

/** 旧 GitBook 文档目录（只读），可用 KOIPY_DOC_SRC 覆盖 */
export const LEGACY_DOC_ROOT =
  process.env.KOIPY_DOC_SRC || path.resolve(SITE_ROOT, '..', 'doc')

export const VITEPRESS_DIR = path.join(SITE_ROOT, '.vitepress')
export const SIDEBAR_FILE = path.join(VITEPRESS_DIR, 'sidebar.json')

/** 文档配图目录（md 里用相对路径引用，GitHub 预览也能正常显示） */
export const ASSETS_DIR = path.join(SITE_ROOT, 'assets')

/** 生成/工具目录，不参与站点内容 */
export const KEEP_DIRS = new Set([
  '.vitepress',
  'scripts',
  'public',
  'deploy',
  'node_modules'
])
export const KEEP_FILES = new Set(['README.md'])
export const SKIP_FILES = new Set(['SUMMARY.md', 'LANGS.md'])

/** `image (1).png` -> `image-1.png` */
export function safeName(file) {
  return file
    .replace(/\s*\((\d+)\)/g, '-$1')
    .replace(/[^A-Za-z0-9._-]+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '')
}

export function decode(str) {
  try {
    return decodeURIComponent(str)
  } catch {
    return str
  }
}

export function stripHtml(str) {
  return str.replace(/<[^>]+>/g, '').trim()
}

/** 相对源根目录的 posix 路径 -> 站点路径 */
export function toSitePath(rel) {
  let p = path.posix.normalize(rel.replace(/\\/g, '/'))
  if (p.endsWith('.md')) {
    const dir = path.posix.dirname(p)
    const base = path.posix.basename(p)
    if (base.toLowerCase() === 'readme.md') {
      return dir === '.' ? '/' : '/' + dir + '/'
    }
    p = p.slice(0, -3)
  }
  return '/' + p.replace(/^\/+/, '')
}

export function walk(dir, out = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name.startsWith('.')) continue
    const full = path.join(dir, entry.name)
    if (entry.isDirectory()) walk(full, out)
    else out.push(full)
  }
  return out
}

/** 站点里所有 md（相对 SITE_ROOT 的 posix 路径） */
export function listSiteDocs() {
  return walk(SITE_ROOT)
    .filter((f) => f.endsWith('.md'))
    .map((f) => path.relative(SITE_ROOT, f).replace(/\\/g, '/'))
    .filter((rel) => {
      const top = rel.split('/')[0]
      return !KEEP_DIRS.has(top) && !KEEP_FILES.has(rel)
    })
    .sort()
}
