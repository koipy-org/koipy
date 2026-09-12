---
description: 关于此 bot
---

# /about

## 解释

展示 koipy 的授权说明与第三方许可信息。

## 用法

```
/about
```

## 特性

* 任何人都可以使用，不需要权限。
* 输出内容为 koipy 的授权声明，以及 `resources/THIRD-PARTY-LICENSES.md` 里的第三方组件许可信息。
* 如果程序目录下找不到许可文件，会提示「未找到许可文件，请尝试重新安装」。
* 内容较长，bot 会以 Markdown 形式发送。

## 相关页面

{% content-ref url="license.md" %}
[license.md](license.md)
{% endcontent-ref %}
