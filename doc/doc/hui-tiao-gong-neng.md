---
description: 此页面将介绍koipy的回调细节
---

# 回调功能

koipy基于HTTP协议实现了基本的回调功能。HTTP回调功能可以让koipy程序不改动源码的情况下实现以下需求：

* 测试黑名单设立
* 为不同用户重定向后端选择
* 为测试结果进行数据分析和处理，并回传结果形成新的数据矩阵(新的列)
* 输出自定义的图片，而不再局限于bot的绘图
* 设立积分测试制度
* 进行测试统计，计算用户量
* 等等。。。

## 使用方法

在配置文件中加入如下配置(想开启哪个就取消注释)：

<pre class="language-yaml"><code class="lang-yaml">callbacks:
  onMessage: http://127.0.0.1:8080/onMessage # 回调地址，机器人收到消息时,会向此地址发送POST请求，使用方法请看文档
<strong>#  onPreSend: http://127.0.0.1:8080/onPreSend # 回调地址，机器人处理所有任务的前置动作后（比如选定后端、选定规则等），会向此地址发送POST请求，来完成一些操作，使用方法请看文档
</strong>#  onResult: http://127.0.0.1:8080/onResult # 回调地址，机器人接受完测试结果后，会向此地址发送POST请求，可以用来添加，使用方法请看文档
</code></pre>

这样，bot就会在特定时机发送POST请求到对应的回调地址，配置的三个回调地址的触发时机分别是：

* callbacks.onMessage  在bot收到来自使用者的测试指令时
* callbacks.onPreSend 在bot整理好所有的测试规则，即将发给后端时
* callbacks.onResult 在接收完后端的测试结果，但还没有进行最终处理时

## POST请求载荷

如无意外，bot向回调地址发送的POST请求的数据格式 **始终为** JSON格式，它的结构体定义如下（最终序列化成JSON字符串）：

```python
@dataclass
class KoiCallbackData(DictCFG, ConfigManager):
    message: dict = field(default_factory=dict) # 来自TG的消息
    config: KoiConfig = field(default_factory=lambda: KoiConfig()) # 你的配置文件
    slaveRequest: SlaveRequest = field(default_factory=lambda: SlaveRequest()) # 测试请求结构体，它包含测试的所有细节
    result: dict = field(default_factory=dict) # 测试结果
    addons: dict = field(default_factory=dict) # 保留字段，暂时无用
```



## 处理结果

你需要自己建立回调服务器，使用你任何喜欢的编程语言搭建HTTP服务器，让它处理来自bot的请求，并构造响应结果，并将遵循HTTP协议的响应体回传给bot，其中响应体应遵循以下约定：

1. 返回状态码

回调服务器应当返回HTTP状态码，根据状态码的不同，bot会作出以下操作：

* 204 - bot会继续执行测试的代码逻辑
* 200 - bot会继续执行测试的代码逻辑，并根据响应头的 "Content-Type" 字段，额外在TG发送不同的内容
* \>400 - bot将**拒绝执行**接下来的代码逻辑，并读取utf-8的文本内容作为错误提示回显给用户
* 其他状态码 - bot将无视这些状态码，继续执行测试的代码逻辑

2. 返回请求头的Content-Type字段

不论状态码是否是200，最好都返回Content-Type字段，bot会根据以下情况适配一些逻辑：

将发送额外的图片到Telegram，响应内容是一张图片:

```http
Content-Type: image/jpeg
Content-Type: image/png
```

将发送额外的提示文本：

```http
Content-Type: plain/text
```

将合并回调数据，修改或新增测试结果：

<pre class="language-http"><code class="lang-http"><strong>Content-Type: application/json
</strong></code></pre>

如果没有Content-Type字段，将会额外发送一个文件，并根据Content-Disposition字段设置文件名：

```http
Content-Disposition: attachment; filename="test.jpg"
```



## 测试例子

以下是一个HTTP回调服务器的例子，它将在本地的8080端口运行回调服务，并展示一个基本运行逻辑：



```python
# 请先安装aiohttp
# pip install -U aiohttp
from aiohttp import web
from PIL import Image, ImageDraw
import io
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def generate_test_image(text: str = "Test Image") -> bytes:
    """生成一个简单的测试图片"""
    # 创建一个300x200的白色背景图片
    width = 300
    height = 200
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)

    # 绘制一些文本和图形
    draw.rectangle([10, 10, width - 10, height - 10], outline='blue', width=2)
    draw.text((width // 2 - 50, height // 2), text, fill='black')

    # 添加时间戳
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    draw.text((10, height - 20), timestamp, fill='gray')

    # 转换为JPEG字节流
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='png')
    img_byte_arr = img_byte_arr.getvalue()

    return img_byte_arr


class ImageServer:
    @staticmethod
    async def handle_image(request: web.Request) -> web.Response:
        """处理图片请求并返回JPEG图片"""
        try:
            # 从请求中获取文本参数
            data = await request.json()
            text = data.get('text', 'Test Image')

            # 生成图片
            image_data = await generate_test_image(text)

            # 设置响应头
            headers = {
                'Content-Type': 'image/jpeg',
                'Content-Disposition': 'attachment; filename="test.jpg"'
            }

            logger.info(f"Generating image with text: {text}")

            return web.Response(body=image_data, headers=headers, status=403)

        except Exception as e:
            logger.error(f"Error generating image: {e}")
            return web.Response(
                status=500,
                text=f"Error generating image: {str(e)}"
            )


async def on_message(request):
    # 它将拉黑一个TG用户名为koipybot的用户
    # Get the JSON data from request
    data = await request.json()
    # Return the data as-is
    if str(data['message']['from_user']['username']).startswith('koipybot'):
        return web.Response(status=403, text='你已被拉黑！')
    return web.json_response()


async def on_pre_send(request):
    data = await request.json()
    return await ImageServer.handle_image(request)


async def on_result(request):
    data = await request.json()
    result: dict = data['result']
    result["NewKey"] = ["回调新增数据1" for _ in range(len(result["节点名称"]))]
    data['result'] = result
    return web.json_response(data)


async def init_app():
    _app = web.Application()
    # Setup routes
    _app.router.add_post('/onMessage', on_message)
    _app.router.add_post('/onPreSend', on_pre_send)
    _app.router.add_post('/onResult', on_result)

    return _app


if __name__ == '__main__':
    app = init_app()
    web.run_app(app, host='127.0.0.1', port=8080)

```



