import fs from 'node:fs'

const sidebar = JSON.parse(
  fs.readFileSync(new URL('./sidebar.json', import.meta.url), 'utf-8')
)

export default {
  lang: 'zh-CN',
  title: 'koipy',
  description: 'koipy —— 专注于代理平台的连通性测试工具（Telegram Bot）文档',
  cleanUrls: true,
  ignoreDeadLinks: false,
  srcExclude: ['README.md', 'scripts/**', 'deploy/**', 'node_modules/**'],
  head: [
    ['link', { rel: 'icon', href: '/favicon.ico', sizes: '256x256' }],
    ['link', { rel: 'apple-touch-icon', href: '/logo.png' }]
  ],

  themeConfig: {
    logo: '/logo.png',
    outline: { level: [2, 3], label: '本页目录' },
    nav: [
      { text: '开始', link: '/kuai-su-kai-shi' },
      { text: '配置详解', link: '/doc/pei-zhi-xiang-jie/' },
      { text: '指令详解', link: '/doc/zhi-ling-xiang-jie/' },
      { text: '更新日志', link: '/doc/geng-xin-ri-zhi/' }
    ],
    sidebar,
    search: { provider: 'local' },
    docFooter: { prev: '上一篇', next: '下一篇' },
    outlineTitle: '本页目录',
    darkModeSwitchLabel: '主题',
    sidebarMenuLabel: '目录',
    returnToTopLabel: '回到顶部',
    lastUpdated: {
      text: '最后更新于',
      formatOptions: { dateStyle: 'short', timeStyle: 'short' }
    },
    footer: {
      message: '文档内容同步自 koipy-public',
      copyright: 'koipy'
    }
  }
}
