---
description: 此页面将介绍koipy的回调细节
---

# 回调功能

koipy 基于 HTTP 协议实现了基本的回调功能，可以在不改动源码的情况下实现以下需求：

* 测试黑名单设立
* 为不同用户重定向后端选择
* 为测试结果进行数据分析和处理，并回传结果形成新的数据矩阵(新的列)
* 输出自定义的图片，而不再局限于bot的绘图
* 设立积分测试制度
* 进行测试统计，计算用户量
* 等等。。。

## 使用方法

在配置文件中加入如下配置，按需取消注释：

```yaml
callbacks:
  onMessage: http://127.0.0.1:8080/onMessage # 机器人收到消息时发送请求
  # onPreSend: http://127.0.0.1:8080/onPreSend # 处理完前置动作后发送请求
  # onResult: http://127.0.0.1:8080/onResult # 接收完测试结果后发送请求
```

这样，bot就会在特定时机发送POST请求到对应的回调地址，配置的三个回调地址的触发时机分别是：

- `callbacks.onMessage`：在 bot 收到来自使用者的测试指令时触发
- `callbacks.onPreSend`：在 bot 整理好所有测试规则，即将发给后端时触发
- `callbacks.onResult`：在接收完后端测试结果，但还没有进行最终处理时触发

## POST请求载荷

如无意外，bot向回调地址发送的POST请求的数据格式 **始终为** JSON格式，它的结构体定义如下（最终序列化成JSON字符串）：

```python
@dataclass
class KoiCallbackData(DictCFG, ConfigManager):
    message: dict = field(default_factory=dict) # 来自 TG 的消息
    config: KoiConfig = field(default_factory=lambda: KoiConfig()) # 你的配置文件
    slaveRequest: SlaveRequest = field(default_factory=lambda: SlaveRequest()) # 测试请求结构体，包含测试的所有细节
    result: dict = field(default_factory=dict) # 测试结果
    addons: dict = field(default_factory=dict) # 保留字段，当前无用
```



## 处理结果

你需要自己建立回调服务器，使用你任何喜欢的编程语言搭建HTTP服务器，让它处理来自bot的请求，并构造响应结果，并将遵循HTTP协议的响应体回传给bot，其中响应体应遵循以下约定：

1. 返回状态码

回调服务器应当返回HTTP状态码，根据状态码的不同，bot会作出以下操作：

- `204` - bot 会继续执行测试逻辑
- `200` - bot 会继续执行测试逻辑，并根据响应头的 `Content-Type` 发送额外内容
- `>400` - bot 会**拒绝执行**后续逻辑，并读取 UTF-8 文本作为错误提示回显给用户
- 其他状态码 - bot 会无视这些状态码，继续执行测试逻辑

2. 返回请求头的Content-Type字段

不论状态码是否是200，最好都返回Content-Type字段，bot会根据以下情况适配一些逻辑：

将发送额外的图片到Telegram，响应内容是一张图片:

```http
Content-Type: image/jpeg
Content-Type: image/png
```

将发送额外的提示文本：

```http
Content-Type: text/plain
```

将合并回调数据，修改或新增测试结果：

```http
Content-Type: application/json
```

如果没有Content-Type字段，将会额外发送一个文件，并根据Content-Disposition字段设置文件名：

```http
Content-Disposition: attachment; filename="test.jpg"
```



## 测试例子

以下是一个HTTP回调服务器的例子，它将在本地的8080端口运行回调服务，并展示一个基本运行逻辑：



```python
# pip install -U aiohttp pillow
from aiohttp import web
from PIL import Image, ImageDraw
import io
from datetime import datetime


async def generate_test_image(text: str = "Test Image") -> bytes:
    width = 300
    height = 200
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle([10, 10, width - 10, height - 10], outline="blue", width=2)
    draw.text((80, 90), text, fill="black")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    draw.text((10, height - 20), timestamp, fill="gray")

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


class ImageServer:
    @staticmethod
    async def handle_image(request: web.Request) -> web.Response:
        data = await request.json()
        text = data.get("text", "Test Image")
        image_data = await generate_test_image(text)
        headers = {
            "Content-Type": "image/png",
            "Content-Disposition": 'attachment; filename="test.png"',
        }
        return web.Response(body=image_data, headers=headers, status=200)


async def on_message(request):
    data = await request.json()
    if str(data["message"]["from_user"].get("username", "")).startswith("koipybot"):
        return web.Response(status=403, text="你已被拉黑！", content_type="text/plain")
    return web.Response(status=204)


async def on_pre_send(request):
    return await ImageServer.handle_image(request)


async def on_result(request):
    data = await request.json()
    result: dict = data.get("result", {})
    result["NewKey"] = ["回调新增数据1" for _ in range(len(result.get("节点名称", [])))]
    data["result"] = result
    return web.json_response(data)


async def init_app():
    app = web.Application()
    app.router.add_post("/onMessage", on_message)
    app.router.add_post("/onPreSend", on_pre_send)
    app.router.add_post("/onResult", on_result)
    return app


if __name__ == "__main__":
    app = init_app()
    web.run_app(app, host="127.0.0.1", port=8080)

```



