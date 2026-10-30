---
description: re是repeat的缩写
---

# /re

快速重测上一次构建的测试任务。支持参数覆写，用来改变某些测速请求参数。



## 例子

```markdown
# 覆写测试订阅地址
/re https://www.google.com

# 覆写后端
/re?s=local

# 更改包含过滤器为"HK"，排除过滤器为"直连"
/re 随便写 HK 直连

#覆写测速线程为1（如果是测速任务）
/re?thread=1

/re 支持?后面的所有参数

```
