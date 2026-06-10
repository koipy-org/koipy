---
description: 这里的配置用于切换和加载 koipy 的语言包。
---

# translation

这一页说明语言包配置。`translation` 决定 bot 当前使用哪套文案，以及额外语言文件从哪里加载。

<details>

<summary>translation</summary>

{% code expandable="true" %}
```yaml
translation:
  lang: zh_CN
  resources:
    zh_CN: "./resources/i18n/zh_CN.yml"
    en_us: "./resources/i18n/en_us.yml"
```
{% endcode %}

</details>

{% hint style="warning" %}
`translation.lang` 会把 `-` 自动转成 `_`，但 `translation.resources` 的键不会跟着自动改。也就是说，自定义语言包更推荐直接写 `zh_CN`、`en_us` 这类最终键名，不要继续沿用 `zh-CN` 这种旧示例。
{% endhint %}

## translation.lang

{% tabs %}
{% tab title="解释" %}
1. 这项配置用于指定当前启用哪套语言包。
2. 当前实现会先把这里的值做一次 `- -> _` 归一化，例如 `zh-CN` 会变成 `zh_CN`。
3. 如果最终找不到对应语言键，程序会回退到内置默认语言对象。
{% endtab %}

{% tab title="特性" %}
1. 类型：`str`
2. 默认值：`zh_CN`
3. 内置 `zh_CN` 一定会预加载。
4. 如果工作目录下存在 `resources/localization/en-us.yml`，当前实现还会额外预加载一个 `en_us`。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
translation:
  lang: en_us
  resources:
    en_us: "./resources/i18n/en_us.yml"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## translation.resources

{% tabs %}
{% tab title="解释" %}
1. 这是自定义语言资源映射表，格式是“语言键 -> 文件路径”。
2. 当前实现只会保留值为字符串的条目，其它类型会被忽略。
3. 如果你提供的键和 `lang` 最终归一化后的值一致，就能选中这套自定义语言包。
{% endtab %}

{% tab title="特性" %}
1. 类型：`dict[str, str]`
2. 加载顺序是：内置 `zh_CN` -> 可选内置 `en_us` -> 你在这里定义的资源
3. 如果你在这里重复定义了 `zh_CN` 或 `en_us`，后加载的文件会覆盖前面的内置版本。
4. 路径既可以是相对路径，也可以是绝对路径；相对路径通常按 koipy 工作目录解析。
{% endtab %}

{% tab title="配置示例" %}
{% code title="config.yaml" lineNumbers="true" %}
```yaml
translation:
  lang: zh_CN
  resources:
    zh_CN: "./resources/i18n/custom-zh_CN.yml"
    en_us: "./resources/i18n/custom-en_us.yml"
```
{% endcode %}
{% endtab %}
{% endtabs %}

## 语言键命名建议

{% tabs %}
{% tab title="解释" %}
1. 如果你只是想覆盖中文，最稳妥的键名就是 `zh_CN`。
2. 如果你想覆盖英文，最稳妥的键名就是 `en_us`。
3. 你当然也可以自定义成 `myteam`、`private_pack` 这类键，但 `lang` 必须最终也写成同一个字符串。
4. 需要特别避开的坑是：`lang: zh-CN` + `resources: { zh-CN: ... }` 这组写法，在当前实现里很可能选不中你的自定义文件。
{% endtab %}

{% tab title="特性" %}
1. 推荐优先使用下划线风格：`zh_CN`、`en_us`
2. 如果你必须用带连字符的写法，请同时确认 `lang` 归一化后的值和资源键是否仍然一致。
3. 键名本身不需要和文件名一致，真正重要的是“`lang` 最终选中的键名”。
{% endtab %}

{% tab title="配置示例" %}
{% code title="自定义键示例" lineNumbers="true" %}
```yaml
translation:
  lang: myteam
  resources:
    myteam: "./resources/i18n/myteam.yml"
```
{% endcode %}
{% endtab %}
{% endtabs %}

语言包的导入与制作，可继续看：

{% content-ref url="../yu-yan-bao/dao-ru-yu-yan-bao.md" %}
[dao-ru-yu-yan-bao.md](../yu-yan-bao/dao-ru-yu-yan-bao.md)
{% endcontent-ref %}

以及：

{% content-ref url="../yu-yan-bao/zhi-zuo-yu-yan-bao.md" %}
[zhi-zuo-yu-yan-bao.md](../yu-yan-bao/zhi-zuo-yu-yan-bao.md)
{% endcontent-ref %}
