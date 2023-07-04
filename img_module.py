
import math

from PIL import Image, ImageDraw, ImageFont

# 定义颜色常量
COLOR_RGBA_TRANSPARENT = (0, 0, 0, 0)
COLOR_RGB_WHITE = (255, 255, 255)
COLOR_RGB_BLACK = (0, 0, 0)


def __make_watermark(text,
                     size: tuple,
                     space: tuple=None,
                     angle=0,
                     alpha=255,
                     font_path="arial.ttf",
                     font_size=24,
                     font_color=COLOR_RGB_BLACK) -> Image.Image:
    if not space:
        space = (font_size, font_size)
    # 创建新的图像
    image = Image.new('RGBA', size, color=COLOR_RGBA_TRANSPARENT)

    def horizontal_text_watermarking():
        height, width = size
        space_x, space_y = space
        watermark_img = Image.new('RGBA', size, color=COLOR_RGBA_TRANSPARENT)
        draw = ImageDraw.Draw(watermark_img)
        font = ImageFont.truetype(font_path, size=font_size)
        # 计算文本框尺寸
        _, _, text_height, text_width = font.getbbox(text)
        # 计算水印框能容纳几个文本框（向上取整）
        h = text_height + space_y
        w = text_width + space_x
        y_num = height // h + 1
        x_num = width // w + 1
        for y in range(y_num):
            for x in range(x_num):
                draw.text((y * h, x * w), text, font=font, fill=(*font_color,alpha))
        return watermark_img

    # 计算旋转后的贴图尺寸，确保能覆盖原图
    s = int(math.sqrt(size[0] ** 2 + size[1] ** 2)) + 1
    size = (s, s)
    watermark_img = horizontal_text_watermarking()
    rotated_watermark_img = watermark_img.rotate(angle)
    # 计算粘贴到中心的坐标
    x1, y1 = rotated_watermark_img.size
    x2, y2 = image.size
    x = int((x2 - x1) / 2)
    y = int((y2 - y1) / 2)

    image.paste(rotated_watermark_img, (x, y))
    return image


def add_watermark(img: Image.Image, text, **kwargs):
    watermark_img = __make_watermark(text, img.size, **kwargs)
    img = img.copy()
    img.paste(watermark_img, (0, 0), watermark_img)
    return img


