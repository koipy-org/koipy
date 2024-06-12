import bisect
import math
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Union, Tuple, List

from PIL import Image, ImageDraw, ImageFont, ImageColor
from pilmoji import Pilmoji

from utils import myemoji, __version__, HOME_DIR
from utils.types.config import Color, KoiConfig
from utils.algorithm import atoi
from utils.types.draw import DrawConfig

_clock_emoji_list = ["🕛", "🕐", "🕑", "🕒", "🕓", "🕔", "🕕", "🕖", "🕗", "🕘", "🕙", "🕚"]


def get_clock_emoji() -> str:
    current_hour = time.localtime().tm_hour % 12
    emoji_time = _clock_emoji_list[current_hour]
    return emoji_time


def getrgb(hexcolor: str):
    """
    转换16进制格式的颜色值到RGB格式
    """
    _t = list()
    if hexcolor.startswith('#'):
        for i in (0, 2, 4):
            _t.append(int(hexcolor.lstrip('#')[i:i + 2], 16))
        return _t[0], _t[1], _t[2]
    else:
        raise ValueError("颜色值必须为十六进制")


def color_block(size: Tuple[int, int], c: Color):
    """
    颜色块，颜色数值推荐用十六进制表示如: #ffffff 为白色
    :param size: tuple: (length,width)
    :param c: 颜色类
    :return: Image
    """
    rgba = getrgb(c.value) + (c.alpha,)
    rgba = rgba[:3]
    return Image.new('RGBA', size, rgba)


def c_block_grad(size: Tuple[int, int], c: Color, enable_grad: bool = True):
    """
    生成渐变色块
    :param enable_grad: 启用渐变
    :param c: 颜色类
    :param size: tuple: (length, width) 图像尺寸
    :return: Image
    """
    if not enable_grad:
        return color_block(size, c)
    image = Image.new('RGBA', size)
    draw = ImageDraw.Draw(image)
    start_rgb = getrgb(c.value)
    end_rgb = getrgb(c.end_color)

    for y in range(size[1]):
        r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * (y / size[1]))
        g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * (y / size[1]))
        b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * (y / size[1]))
        rgba = (r, g, b, c.alpha)
        draw.line([(0, y), (size[0], y)], fill=rgba)

    return image


def unlock_stats(raw: dict) -> dict:
    temp_dict = {}
    for k, v in raw.items():
        if isinstance(v, list) and v and not isinstance(v[0], list):
            new_dict = {}
            ct = Counter(v)
            for k0, v0 in ct.items():
                if isinstance(k0, str):
                    if "待解" in k0:
                        new_dict['待解'] = new_dict.get('待解', 0) + v0
                    elif "解锁" in k0 or "允许" in k0 or "Low" in k0:
                        new_dict['解锁'] = new_dict.get('解锁', 0) + v0
                    else:
                        new_dict[k0] = new_dict.get(k0, 0) + v0
            temp_dict[k] = new_dict
    return temp_dict


class BaseExport:
    def __init__(self, primarykey: Union[int, str], allinfo: dict):
        """
        所有绘图类的基类，primarykey为主键，计算主键的长度，主键决定整张图片的高度
        """
        self.primarykey = str(primarykey)
        self.basedata = list(allinfo.pop(primarykey))
        self.allinfo = allinfo
        self.info = self.get_printinfo()

    def get_printinfo(self):
        """
        为了统一长度，self.info 一定和主键长度对齐
        """
        new_info = {"序号": [str(i + 1) for i in range(len(self.basedata))], self.primarykey: self.basedata}
        for k, v in self.allinfo.items():
            if isinstance(v, list) and len(v) == len(self.basedata):
                new_info[k] = v
        return new_info


class KoiDraw(BaseExport):
    """
    一种通用的绘图数据表格类，连通性测试一般是用这个。
    init:
        primarykey: 将一个列表的数据作为基底，来决定整张图片的高度
        allinfo: 所有的数据传入，它应该是一个字典
        config: 具有较为严格类型定义的配置文件对象
    """

    def __init__(self, primarykey: Union[str, int], allinfo: dict, config: "KoiConfig"):
        super().__init__(primarykey, allinfo)
        self.koicfg = config
        self.cfg = DrawConfig()
        self.cfg.basedataNum = len(self.basedata) if self.basedata else 0
        self._filter = self.allinfo.pop('filter', {})

        self._font = ImageFont.truetype(self.koicfg.image.font, self.cfg.frontsize)
        self._end_color_flag = self.koicfg.image.endColorsSwitch
        self.color = self.koicfg.image.color
        self.color.delay.sort(key=lambda x: x.label)  # 初始化时做排序
        self.color.speed.sort(key=lambda x: x.label)
        self.color.outColor.sort(key=lambda x: x.label)
        self.emoji_enable = self.koicfg.image.emoji.enable
        _source = self.koicfg.image.emoji.source
        self.emoji_source = getattr(myemoji, _source) if _source in myemoji.__all__ else myemoji.TwemojiLocalSource
        self.width, self.width_list = self.get_width()  # width_list包含主键和序号
        self.height = self.get_height()

    def text_width(self, text: str) -> int:
        """
        得到字符串在图片中的绘图长度
        :param text: 文本内容
        :return: int
        """
        draw = ImageDraw.Draw(Image.new("RGBA", (1, 1), (255, 255, 255, 255)))
        return int(draw.textlength(text, font=self._font))

    def matrix_width(self, strlist: list) -> int:
        """
        得到列表中最长字符串的绘图长度
        :param strlist:
        :return: int
        """
        max_width = max(self.text_width(str(i)) for i in strlist) if strlist else 0
        return max_width

    def get_key_list(self) -> list:
        """
        得到测试项名称，即字典里所有键的名称
        :return: list
        """
        return list(self.info.keys())

    def calc_block(self, key):
        key_width = self.text_width(key) + 40
        if key != "每秒速度":
            return key_width
        max_width = key_width
        speedblock_num = max(len(lst) for lst in self.info[key]) if self.info[key] else 0
        if speedblock_num > 0:
            speedblock_total_width = speedblock_num * self.cfg.speedBlockWidth
            if speedblock_total_width >= key_width:  # 如果每秒速度的速度块宽度总和大于主键的宽度，那么取较大的
                max_width = speedblock_total_width
            else:  # 相反，如果小于，那么也要调整，保证观感 54 / 10
                self.cfg.speedBlockWidth = math.ceil(float(key_width / speedblock_num))
                max_width = speedblock_num * self.cfg.speedBlockWidth
        return max_width

    def key_width_list(self) -> list:
        """
        得到所有测试项列的大小
        :return: list
        """
        key_list = self.get_key_list()  # 得到每个测试项便签绘图的大小[100,80]
        width_list = []
        for i in key_list:
            key_width = self.text_width(i)  # 键的长度
            if i == "每秒速度":
                max_width = self.calc_block(i)
            else:
                value_width = self.matrix_width(self.info[i])  # 键所对应值的长度
                max_width = max(key_width, value_width) + 65  # 65为缓冲值，为了不让字距离边界那么近
            width_list.append(max_width)
        return width_list  # 测试项列的大小

    def get_height(self) -> int:
        """
        获取图片高度
        :return: int
        """
        return (self.cfg.basedataNum + 5) * self.cfg.linespace

    def get_basedata_width(self):
        """
        获取主键对于矩阵的宽度
        :return:
        """
        basedata_width = self.matrix_width(self.basedata)
        basedata_width = max(basedata_width, 500) + 150
        return basedata_width

    def get_width(self) -> Tuple[int, List[int]]:
        """
        获得整个图片的宽度
        :return: 返回图片宽度和每列矩阵的宽度
        """
        infolist_width = self.key_width_list()
        infolist_width[1] = max(infolist_width[1], 500) + 150  # 索引1为主键的内容
        width_list = infolist_width

        img_width = sum(width_list)

        maxwidth = max(img_width, self.text_width(self.get_footer(1)), self.text_width(self.get_footer(2)))
        if list(self.info.keys())[-1] != "每秒速度":
            maxwidth += 28
        width_list[-1] += maxwidth - img_width
        img_width = maxwidth
        return int(img_width), width_list

    def get_mid(self, start_x: Union[int, float], end_x: Union[int, float], str_name: str) -> int:
        """
        居中对齐的起始位置
        :param start_x:
        :param end_x:
        :param str_name:
        :return:
        """
        mid_xpath = (end_x + start_x) / 2
        strname_width = self.text_width(str_name)
        xpath = mid_xpath - strname_width / 2
        xpath = int(xpath)
        return xpath

    def draw_watermark(self, original_image: Image.Image) -> Image.Image:
        """
        绘制水印
        """
        watermark = self.koicfg.image.watermark
        uid = self.allinfo.get('task', {}).get('initiator', '')
        if uid and uid not in self.koicfg.user:
            watermark = self.koicfg.image.nonCommercialWatermark
        if not watermark.enable:
            return original_image
        watermark_text = watermark.text
        shadow = bool(watermark.shadow)  # 是否是盲水印
        trace_enable = bool(watermark.trace)
        if trace_enable:
            watermark_text += f" UID:{uid}"
        if not shadow:
            font = ImageFont.truetype(self.koicfg.image.font, int(watermark.size))
            _, __, wm_width, wm_height = font.getbbox(watermark_text)
            text_image = Image.new('RGBA', (wm_width, wm_height), (255, 255, 255, 0))
            text_draw = ImageDraw.Draw(text_image)

            rgb = ImageColor.getrgb(watermark.color.value)
            rgba = (rgb[0], rgb[1], rgb[2], (int(watermark.alpha)))
            text_draw.text((0, 0), watermark_text, rgba, font=font)

            angle = float(watermark.angle)
            rotated_text_image = text_image.rotate(angle, expand=True, fillcolor=(0, 0, 0, 0),
                                                   resample=Image.BILINEAR)
            watermarks_image = Image.new('RGBA', original_image.size, (255, 255, 255, 0))
            x = original_image.size[0] // 2 - rotated_text_image.size[0] // 2
            row_spacing = int(watermark.row_spacing)
            if row_spacing < 0:
                row_spacing = 0
            y = int(watermark.start_y)
            while True:
                watermarks_image.paste(rotated_text_image, (x, y))
                y += rotated_text_image.size[1] + row_spacing
                if y >= original_image.size[1]:
                    break
            return Image.alpha_composite(original_image, watermarks_image)
        else:
            return original_image

    def draw_background(self) -> Image.Image:
        """
        背景图绘制
        :return:
        """
        bkgcfg = self.koicfg.image.color.background
        B1_color = bkgcfg.script
        alphas = bkgcfg.script.alpha
        B1_rgba = getrgb(B1_color.value) + (alphas,)
        img = Image.new("RGBA", (self.width, self.height), B1_rgba)
        titlet = bkgcfg.speedTitle.value
        titlet_alpha = getrgb(titlet) + (alphas,)
        bkg = Image.new('RGBA', (self.width, self.cfg.linespace * 2), titlet_alpha)  # 首尾部填充
        img.paste(bkg, (0, 0))
        img.paste(bkg, (0, self.height - self.cfg.linespace * 2))
        return img

    def get_footer(self, style: int) -> str:
        if style == 1:
            _wtime = self.allinfo.get('wtime', 0)
            _default_slavename = 'Local'
            _slavename = self.allinfo.get('slave', {}).get('comment', _default_slavename)
            _sort = self.allinfo.get('sort', '订阅原序')
            _traffic_used = self.allinfo.get('消耗流量', "")
            _traffic_used = f"消耗流量={_traffic_used:.1f}MB" if _traffic_used else ''
            _filter_include = self._filter.get('include', '')
            _filter_exclude = self._filter.get('exclude', '')
            _thread = self.allinfo.get('线程', '')
            _thread = f"线程={_thread}" if _thread else ''
            footer = (f"🧬版本={__version__}  "
                      f"后端={_slavename}  " + f"{_traffic_used}  " + f"{_thread}  " +
                      f"排序={_sort}  "
                      f"耗时={_wtime}s  "
                      f"过滤器={_filter_include} <-> {_filter_exclude}"
                      )
            return footer
        elif style == 2:
            _e_time = get_clock_emoji()
            _export_time = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
            sys_timezone = datetime.now(timezone.utc).astimezone().tzinfo
            footer = f"{_e_time}测试时间: {_export_time} ({sys_timezone})  测试结果仅供参考，以实际情况为准"
            return footer
        else:
            return ""

    def draw_info(self, idraw: Union[ImageDraw.ImageDraw, Pilmoji]):
        """
        绘制标题栏和结尾栏信息
        """
        _width = self.width
        _height = self.height
        _title = f"{self.koicfg.image.title} - 连通性测试"

        _footer = self.get_footer(1)
        _footer2 = self.get_footer(2)
        _footer3 = "📊解锁占比:"
        idraw.text((self.get_mid(0, _width, _title), 3), _title, font=self._font, fill=(0, 0, 0))  # 标题
        if isinstance(idraw, Pilmoji):
            idraw.text((10, _height - (self.cfg.linespace - 4) * 2), _footer, font=self._font, fill=(0, 0, 0),
                       emoji_position_offset=(0, 8))  # 版本信息
            idraw.text((10, _height - (self.cfg.linespace - 5)), _footer2, font=self._font, fill=(0, 0, 0),
                       emoji_position_offset=(0, 8))  # 测试时间

            idraw.text((10, _height - (self.cfg.linespace - 2) * 3), _footer3, font=self._font, fill=(0, 0, 0),
                       emoji_position_offset=(0, 8))
        else:
            idraw.text((10, _height - (self.cfg.linespace - 4) * 2), _footer, font=self._font, fill=(0, 0, 0))
            idraw.text((10, _height - (self.cfg.linespace - 5)), _footer2, font=self._font, fill=(0, 0, 0))
            idraw.text((10, _height - (self.cfg.linespace - 2) * 3), _footer3, font=self._font, fill=(0, 0, 0))

    def draw_label(self, idraw):
        """
        绘制标签,效果图：
        ---------------------------
        |节点名称|节点类型|HTTP(S)延迟...|
        --------------------------
        """
        _nodename_width = self.get_basedata_width()
        _info_list_width = self.width_list
        _key_list = self.get_key_list()
        if "HTTP(S)延迟" in _key_list:
            # key标签值重命名
            new_text = "HTTPS延迟" if self.koicfg.runtime.pingURL.startswith("https") else "HTTP延迟"
            _key_list[_key_list.index("HTTP(S)延迟")] = new_text
        text_list = []
        start_x = 0
        for i, info_width in enumerate(_info_list_width):
            end_x = start_x + info_width
            text_list.append((_key_list[i], self.get_mid(start_x, end_x, _key_list[i])))
            start_x = end_x
        for text, x in text_list:
            idraw.text((x, self.cfg.linespace + self.cfg.ctofs - 5), text, fill=(0, 0, 0))

    def draw_line(self, idraw):
        # 绘制横线
        _lspace = self.cfg.linespace
        _image_width = self.width
        _nodename_width = self.get_basedata_width()
        _info_list_width = self.width_list
        for t in range(self.cfg.basedataNum + 3):
            idraw.line([(0, _lspace * (t + 1)), (_image_width, _lspace * (t + 1))], fill="#e1e1e1", width=2)
        # 绘制竖线
        start_x = _info_list_width[0] + _info_list_width[1]
        for i in _info_list_width[2:]:
            x = start_x
            end = start_x + i
            idraw.line([(x, _lspace), (x, self.height - _lspace * 3)], fill="#EAEAEA", width=2)
            start_x = end

    def draw_content(self, draw: Union[Pilmoji, ImageDraw.ImageDraw], xy: Tuple[int, int], ct: str, fill=(0, 0, 0)):
        """
        绘制具体内容
        ct: content内容
        """
        try:
            if isinstance(draw, Pilmoji):
                # 自定义emoji源可能出错，所以捕捉了异常
                draw.text(xy, ct, fill, font=self._font, emoji_position_offset=(0, 6))
            else:
                draw.text(xy, ct, fill, font=self._font)
        except Exception as e:
            print(e)
            # raise KoiError("绘图错误:" + str(e)) from e
            draw.text(xy, ct, fill, font=self._font)

    def draw_percent(self, img: Image.Image, idraw: Union[ImageDraw.ImageDraw, Pilmoji]):
        """
        绘制百分比统计
        :param img:
        :param idraw:
        :return:
        """
        _info_list_width = self.width_list

        _ignore = self.allinfo.get('percent_ignore', [self.primarykey, '序号', '类型',
                                                      '平均速度', '每秒速度', '最大速度'
                                                      'HTTP(S)延迟', 'TLS RTT', '延迟RTT', 'HTTP延迟'])
        _key_list = self.get_key_list()
        _stats = unlock_stats(self.info)
        _height = self.get_height()
        ls = self.cfg.linespace
        y = _height - (ls - 2) * 3
        start = 0
        for _i, _k in enumerate(_key_list):
            if _k in _ignore:
                start += _info_list_width[_i]
                continue
            else:
                raw_percent = _stats.get(_k, {}).get('解锁', 0) / self.cfg.basedataNum
                _percent = int(raw_percent * 100)
                if _percent == 0:
                    start += _info_list_width[_i]
                    continue
                _percent_str = f"{_percent}%"
                x = self.get_mid(start, start + _info_list_width[_i], _percent_str)
                block = c_block_grad((_info_list_width[_i], int(raw_percent * ls)), self.koicfg.image.color.yes,
                                     self._end_color_flag)
                img.alpha_composite(block, (start, y - 7))
                idraw.text((x, y), str(_percent_str), fill=(0, 0, 0), font=self._font)
                start += _info_list_width[_i]

    def hit_speed_color(self, speed_v: int):
        pass

    def hit_color(self, key: str, content: Union[str, int, float]) -> "Color":
        """
        根据文本内容命中配置里的Color对象
        :param key:
        :param content:
        :return:
        """
        content = str(content)
        interval = [int(i.label) for i in self.color.delay]
        speed_interval = [int(i.label) for i in self.color.speed]
        if "延迟" in key or "RTT" in key:
            # rtt = float(content[:-2])
            # 使用了二分法（bisection）算法，这里是确定rtt比interval中的哪个值大
            # bisect.bisect_right(interval, rtt) 减去1 就拿到了指定的值，最后max函数防止j为负
            rtt = atoi(content)
            j = max(bisect.bisect_right(interval, rtt) - 1, 0)
            return self.color.delay[j]
        elif "速度" in key:
            speed_v = atoi(content)
            j = max(bisect.bisect_right(speed_interval, speed_v) - 1, 0)
            return self.color.speed[j]
        elif '国创' in content or '海外' in content:
            return self.color.ipriskMedium
        elif ('解锁' in content or '允许' in content or "货币" in content) and '待' not in content:
            return self.color.yes
        elif '失败' in content or '禁止' in content or '不' in content or '无' in content:
            return self.color.no
        elif '待解' in content or '送中' in content:
            return self.color.wait
        elif 'N/A' in content:
            return self.color.na
        elif 'Low' in content:
            return self.color.ipriskLow
        elif 'Medium' in content:
            return self.color.ipriskMedium
        elif 'High' in content and 'Very' not in content:
            return self.color.ipriskHigh
        elif 'Very' in content:
            return self.color.ipriskVeryHigh
        elif '超时' in content or '连接错误' in content:
            return self.color.warn
        else:
            return Color()

    def draw_speed_block(self, img: Image.Image, t: int, start_x: int, speed_v_list, resize: Union[int, float] = 1):
        """
        绘制每秒速度块
        :param: t 迭代的index
        :param: resize 放大/缩放倍数
        :return:
        """
        max_speed = max(speed_v_list) if speed_v_list else 0
        plain_speed = 50 * resize
        speed_interval = [int(i.label) for i in self.color.speed]
        speedblock_x = start_x
        for speed_v in speed_v_list:
            if max_speed < plain_speed:
                speedblock_ratio_height = int(self.cfg.linespace * speed_v / plain_speed)
            else:
                speedblock_ratio_height = int(self.cfg.linespace * speed_v / max_speed)
            if speedblock_ratio_height > self.cfg.linespace:
                speedblock_ratio_height = self.cfg.linespace
            speedblock_y = self.cfg.linespace * (t + 2) + (self.cfg.linespace - speedblock_ratio_height)
            j = max(bisect.bisect_right(speed_interval, speed_v) - 1, 0)
            c = self.color.speed[j]
            block = c_block_grad((self.cfg.speedBlockWidth, speedblock_ratio_height), c, self._end_color_flag)
            img.alpha_composite(block, (speedblock_x, speedblock_y))
            speedblock_x += self.cfg.speedBlockWidth

    def draw_block(self, img: Image.Image, index: int, _key_list, _width_list):
        """
        绘制颜色块
        """
        t = index
        ls = self.cfg.linespace
        if len(_key_list) < 3:
            return
        # width = 序号 + 主键
        width = _width_list[0] + _width_list[1]
        _width_list = _width_list[2:]
        _key_list = _key_list[2:]
        for i, t1 in enumerate(_key_list):
            content = self.info[t1][t]
            if "延迟" in t1 or "RTT" in t1:
                content = atoi(content)
            if "每秒速度" == t1:
                self.draw_speed_block(img, t, width, content)
            else:
                color_obj = self.hit_color(t1, content)
                block = c_block_grad((_width_list[i], ls), color_obj, self._end_color_flag)
                img.alpha_composite(block, (width, ls * (t + 2)))
            width += _width_list[i]

    def draw(self, debug=False) -> Tuple[str, Tuple[int, int]]:
        """
        绘制图像主要函数
        :param debug为True时仅输出图片到桌面环境窗口
        :return 返回这个图片的文件位置（debug=True时无意义），以及返回图片的大小（长x宽）
        """
        ls = self.cfg.linespace
        ctofs = self.cfg.ctofs - 5  # 行间距改变时的补偿偏移量,Compensation offsets
        _nodename_width = self.get_basedata_width()
        _width_list = self.width_list
        _key_list = self.get_key_list()

        img = self.draw_background()  # 1.首先绘制背景图
        idraw = ImageDraw.Draw(img)
        idraw.font = self._font  # 设置字体，之后就不用一直在参数里传入字体实例啦
        pilmoji = Pilmoji(img, source=self.emoji_source)  # emoji表情修复，emoji必须在参数手动指定字体。

        self.draw_info(pilmoji)  # 绘制标题等相关信息
        self.draw_label(idraw)  # 3.绘制标签
        self.draw_percent(img, idraw)  # 绘制百分比
        # 在一个大循环里绘制，主要思路是按行绘制
        for t in range(self.cfg.basedataNum):
            # 序号
            self.draw_content(idraw,
                              (self.get_mid(0, _width_list[0], str(t + 1)), int(ls * (t + 2) + ctofs)),
                              str(t + 1))
            # 主键内容
            self.draw_content(pilmoji, (_width_list[0] + 10, int(ls * (t + 2) + ctofs)), self.basedata[t])
            # 绘制颜色块
            self.draw_block(img, t, _key_list, _width_list)
            # 其他文本内容
            width = _width_list[0] + _width_list[1]  # 从第三个开始
            if len(_key_list) < 3:
                continue
            for i, t2 in enumerate(_key_list[2:]):
                i2 = i + 2
                if t2 == "每秒速度":
                    continue
                else:
                    x = self.get_mid(width, width + _width_list[i2], self.info[t2][t])
                    self.draw_content(idraw, (x, int(ls * (t + 2) + ctofs)), self.info[t2][t])
                width += _width_list[i2]

        self.draw_line(idraw)  # 绘制线条
        img = self.draw_watermark(img)  # 绘制水印
        if self.koicfg.image.compress:
            img = img.quantize(256, kmeans=1)  # 压缩图片
        _export_time = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime()).replace(":", "-")
        save_path = Path(HOME_DIR).joinpath(f"results/{_export_time}.png")
        if debug:
            img.show("debug image view")
        else:
            img.save(save_path)
            print(f"图片输出位置：results/{_export_time}.png")
        return str(save_path), img.size
