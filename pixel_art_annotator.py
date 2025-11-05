#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
pixel_art_annotator.py
像素画标注程序
"""

import argparse
import json
import math
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageColor


# -----------------------------
# 工具函数
# -----------------------------
def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_contrast_color(rgb):
    r, g, b = rgb[:3]
    luminance = 0.299 * r + 0.587 * g + 0.114 * b
    return (0, 0, 0) if luminance > 128 else (255, 255, 255)


def color_distance(c1, c2, mode="euclidean"):
    if mode == "euclidean":
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))
    elif mode == "manhattan":
        return sum(abs(a - b) for a, b in zip(c1, c2))
    else:
        raise ValueError("Unsupported merge mode")


def merge_similar_colors(color_counts, tolerance=10, mode="euclidean"):
    merged = []
    for color, count in color_counts:
        merged_flag = False
        for i, (ref_color, ref_count) in enumerate(merged):
            if color_distance(color, ref_color, mode) <= tolerance:
                merged[i] = (
                    tuple(
                        round((ref_color[j] * ref_count + color[j] * count) / (ref_count + count))
                        for j in range(3)
                    ),
                    ref_count + count,
                )
                merged_flag = True
                break
        if not merged_flag:
            merged.append((color, count))
    return merged


def auto_crop_image(img):
    bbox = img.getbbox()
    return img.crop(bbox) if bbox else img


# -----------------------------
# 标签生成器 (支持A-Z, AA-ZZ等)
# -----------------------------
def generate_labels(count):
    """生成字母标签，支持超过26个颜色"""
    labels = []
    for i in range(count):
        if i < 26:
            labels.append(chr(97 + i))  # A-Z
        else:
            # AA, AB, ... AZ, BA, BB, ... 等
            first_letter = chr(97 + (i // 26 - 1))
            second_letter = chr(97 + (i % 26))
            labels.append(first_letter + second_letter)
    return labels


# -----------------------------
# 图例排序函数
# -----------------------------
def sort_legend_items(legend_items, sort_method):
    """根据指定方法对图例项进行排序"""
    if sort_method == "by_index":
        # 按原始索引顺序（即颜色出现的顺序）
        return legend_items
    elif sort_method == "by_count":
        # 按颜色出现次数降序排列
        return sorted(legend_items, key=lambda x: x[2], reverse=True)
    elif sort_method == "by_color":
        # 按颜色值排序（RGB）
        return sorted(legend_items, key=lambda x: (x[1][0], x[1][1], x[1][2]))
    elif sort_method == "by_label":
        # 按标签字母顺序
        return sorted(legend_items, key=lambda x: (len(x[0]), x[0]))
    elif sort_method == "by_luminance":
        # 按亮度排序
        def luminance(color):
            return 0.299 * color[0] + 0.587 * color[1] + 0.114 * color[2]

        return sorted(legend_items, key=lambda x: luminance(x[1]))
    else:
        print(f"⚠️  未知的排序方法: {sort_method}, 使用默认顺序")
        return legend_items


# -----------------------------
# 字体适配计算
# -----------------------------
def fit_font_size(draw, text_lines, font_path, cell_width, cell_height, padding=2, label_scale_factor=1.5,
                  max_line_spacing=10):
    """
    适配字体大小，支持为标签和坐标设置不同的大小
    label_scale_factor: 标签字体相对于坐标字体的大小比例
    max_line_spacing: 最大允许的行间距
    """
    max_font_size = cell_height

    # 尝试不同的字体大小
    for size in range(max_font_size, 4, -1):
        # 计算标签字体大小（较大）
        label_font_size = int(size * label_scale_factor)
        label_font = ImageFont.truetype(font_path, label_font_size)

        # 计算坐标字体大小（较小）
        coord_font_size = size
        coord_font = ImageFont.truetype(font_path, coord_font_size)

        # 计算文本高度和宽度
        label_bbox = draw.textbbox((0, 0), text_lines[0], font=label_font)
        label_height = label_bbox[3] - label_bbox[1]
        label_width = label_bbox[2] - label_bbox[0]

        coord_height = 0
        coord_width = 0
        if len(text_lines) > 1:
            coord_bbox = draw.textbbox((0, 0), text_lines[1], font=coord_font)
            coord_height = coord_bbox[3] - coord_bbox[1]
            coord_width = coord_bbox[2] - coord_bbox[0]

        # 计算总高度（包括行间距）
        total_height = label_height + coord_height
        max_width = max(label_width, coord_width)

        # ========== 关键修改：使用固定地行间距 ==========
        # 不再将行间距限制在字体大小范围内，而是使用固定的最大行间距
        line_spacing = min(max_line_spacing, cell_height - total_height - padding * 2)

        # 确保行间距至少为2像素
        if line_spacing < 2:
            line_spacing = 2

        total_height += line_spacing

        # 检查是否适合单元格
        if total_height <= cell_height - padding * 2 and max_width <= cell_width - padding * 2:
            return label_font, coord_font, line_spacing

    # 如果找不到合适的大小，返回最小的字体
    min_label_font = ImageFont.truetype(font_path, max(6, int(6 * label_scale_factor)))
    min_coord_font = ImageFont.truetype(font_path, 6)
    return min_label_font, min_coord_font, 2


def draw_centered_text(draw, cx, cy, text_lines, label_font, coord_font, fill, line_spacing=4):
    """
    绘制居中对齐的文本，标签使用大字体，坐标使用小字体
    line_spacing: 行间距参数，可以调整字母和坐标之间的距离
    """
    heights, widths = [], []

    for i, t in enumerate(text_lines):
        # 第一行使用标签字体，其他行使用坐标字体
        font = label_font if i == 0 else coord_font
        bbox = draw.textbbox((0, 0), t, font=font)
        widths.append(bbox[2] - bbox[0])
        heights.append(bbox[3] - bbox[1])

    total_height = sum(heights) + line_spacing * (len(text_lines) - 1)
    y_start = cy - total_height / 2

    for i, t in enumerate(text_lines):
        font = label_font if i == 0 else coord_font
        w = widths[i]
        h = heights[i]
        draw.text((cx - w / 2, y_start), t, font=font, fill=fill)
        y_start += h + line_spacing


# -----------------------------
# 坐标格式化函数
# -----------------------------
def format_coordinates(x, y, max_x, max_y):
    """格式化坐标显示，从1开始到999"""
    # 计算需要的数字位数
    x_digits = len(str(max_x + 1))
    y_digits = len(str(max_y + 1))

    # 格式化坐标，从1开始计数
    formatted_x = str(x + 1)
    formatted_y = str(y + 1)

    return f"{formatted_x},{formatted_y}"

# 在 generate_pixel_art_preview 函数中，在绘制像素格的循环之前添加这个函数定义

def blend_colors(base, blend, alpha):
    """简单的颜色混合"""
    r = int(base[0] * (1 - alpha) + blend[0] * alpha)
    g = int(base[1] * (1 - alpha) + blend[1] * alpha)
    b = int(base[2] * (1 - alpha) + blend[2] * alpha)
    return (r, g, b)

# 然后在绘制像素格的循环中使用它

# -----------------------------
# 主函数
# -----------------------------
def generate_pixel_art_preview(
        image_path,
        scale=100,
        margin=80,
        background_color="white",
        show_coordinates=True,
        font_path="arial.ttf",
        auto_contrast_text=True,
        show_grid=True,
        show_color_value=False,
        legend_position="top",
        legend_sort="by_index",
        title="auto",
        output_suffix="_withGrid",
        auto_crop=True,
        debug_mode=False,
        color_tolerance=10,
        merge_mode="euclidean"
):
    img = Image.open(image_path).convert("RGBA")
    if auto_crop:
        img = auto_crop_image(img)
    w, h = img.size
    cell = scale
    pixels = img.load()

    # 统计颜色
    color_counts = {}
    for y in range(h):
        for x in range(w):
            c = pixels[x, y]
            color_counts[c] = color_counts.get(c, 0) + 1
    color_counts = sorted(color_counts.items(), key=lambda kv: kv[1], reverse=True)
    merged_colors = merge_similar_colors(color_counts, color_tolerance, merge_mode)

    # 为每个颜色分配标签
    labels = generate_labels(len(merged_colors))

    # 创建颜色到标签的映射
    color_to_label = {}
    for i, (color, count) in enumerate(merged_colors):
        color_to_label[color] = labels[i]

    # 创建颜色映射函数（找到最接近的颜色）
    def find_closest_color(target_color):
        min_distance = float('inf')
        closest_color = None
        for color, _ in merged_colors:
            distance = color_distance(target_color, color, merge_mode)
            if distance < min_distance:
                min_distance = distance
                closest_color = color
        return closest_color

    enlarged_w = w * cell
    enlarged_h = h * cell

    # 预绘制画布（稍后再加上图例）
    enlarged = Image.new("RGB", (enlarged_w, enlarged_h), background_color)
    draw = ImageDraw.Draw(enlarged)

    # 字体自适配 - 使用新的坐标格式测试字体大小
    # ========== 这里设置标签字体大小比例 ==========
    label_scale_factor = 2.5  # 标签字体大小相对于坐标字体大小的比例，可以调整这个值

    # ========== 这里设置行间距参数 ==========
    # 您可以通过调整下面的值来改变字母和坐标之间的距离
    # 现在可以设置更大的值，最大为20
    desired_line_spacing = 20 # 可以调整这个值来改变行间距，最大可以到20
    # =========================================

    label_font, coord_font, actual_line_spacing = fit_font_size(
        draw, ["AA", "999,999"], font_path, cell, cell,
        label_scale_factor=label_scale_factor,
        max_line_spacing=desired_line_spacing  # 传入最大允许的行间距
    )

    if debug_mode:
        print(f"标签字体大小 = {label_font.size}")
        print(f"坐标字体大小 = {coord_font.size}")
        print(f"字体大小比例 = {label_font.size / coord_font.size:.2f}")
        print(f"实际使用的行间距 = {actual_line_spacing}")
        print(f"颜色数量: {len(merged_colors)}")
        print(f"标签分配: {list(zip(labels, [color[:3] for color, _ in merged_colors]))}")

    # 绘制像素格
    for y in range(h):
        for x in range(w):
            original_color = pixels[x, y]
            # 找到最接近的合并颜色
            closest_color = find_closest_color(original_color)
            label = color_to_label[closest_color]

            fill = closest_color[:3]
            x0, y0 = x * cell, y * cell
            x1, y1 = x0 + cell, y0 + cell

            # 计算当前像素块的亮度
            luminance = 0.299 * fill[0] + 0.587 * fill[1] + 0.114 * fill[2]

            # 根据亮度选择网格线颜色
            if luminance > 128:  # 浅色块
                # 向深色混合
                grid_color = blend_colors(fill, (50, 50, 50), 0.5)  # 30%向黑色混合
            else:  # 深色块
                # 向浅色混合
                grid_color = blend_colors(fill, (250, 250, 250), 0.8)  # 30%向白色混合

            draw.rectangle([x0, y0, x1, y1], fill=fill, outline=grid_color if show_grid else None)
            # draw.rectangle([x0, y0, x1 - 0.0, y1 - 0], fill=fill, outline=(240, 128, 128) if show_grid else None)
            cx, cy = x0 + cell / 2, y0 + cell / 2
            fill_text = get_contrast_color(fill) if auto_contrast_text else (0, 0, 0)
            # 在所有像素绘制完成后，绘制完整的外边框
            if show_grid and x == w - 1 and y == h - 1:  # 只在最后一个像素执行一次
                # 绘制外边框
                draw.rectangle([0, 0, enlarged_w - 1, enlarged_h - 1], outline=grid_color)

            # 使用新的坐标格式化函数
            if show_coordinates:
                coord_text = format_coordinates(x, y, w, h)
                lines = [label, coord_text]
                draw_centered_text(draw, cx, cy, lines, label_font, coord_font, fill_text, actual_line_spacing)
            # 在绘制像素格的循环中，找到这个else分支：
            else:
                draw.text((cx, cy), label, font=label_font, fill=fill_text, anchor="mm")

    # 构建图例（自动换行）
    legend_items = []
    for i, (color, count) in enumerate(merged_colors):
        label = labels[i]
        legend_items.append((label, color, count))

    # 根据排序方式排序图例
    if debug_mode:
        print(f"排序前: {[(label, count) for label, color, count in legend_items]}")

    legend_items = sort_legend_items(legend_items, legend_sort)

    if debug_mode:
        print(f"排序后 ({legend_sort}): {[(label, count) for label, color, count in legend_items]}")

    legend_font = ImageFont.truetype(font_path, max(8, int(cell * 0.6)))
    draw_legend = ImageDraw.Draw(enlarged)

    # ========== 修复图例重叠问题 ==========
    # 动态计算每个图例项所需的宽度
    max_item_width = 0
    for label, color, count in legend_items:
        text = f"{label} {count}"
        if show_color_value:
            text += f" #{color[0]:02X}{color[1]:02X}{color[2]:02X}"
        bbox = draw_legend.textbbox((0, 0), text, font=legend_font)
        item_width = cell + (bbox[2] - bbox[0]) + 12  # 色块宽度 + 文字宽度 + 间距
        max_item_width = max(max_item_width, item_width)

    # 根据最大宽度计算每行可以放置的图例项数量
    available_width = enlarged_w - margin * 2
    max_per_row = max(1, available_width // max_item_width)
    # ===================================

    legend_rows = math.ceil(len(legend_items) / max_per_row)
    legend_height = int(legend_rows * (cell * 1.5))  # 增加行高以适应更长的文本
    new_h = enlarged_h + legend_height + margin * 2
    new_img = Image.new("RGB", (enlarged_w + margin * 2, new_h), background_color)
    new_img.paste(enlarged, (margin, margin + (legend_height if legend_position == "top" else 0)))
    draw_final = ImageDraw.Draw(new_img)

    # 转换为 rgb 元组
    background_color = ImageColor.getrgb(background_color)
    # luminance = 0.299 * background_color[0] + 0.587 * background_color[1] + 0.114 * background_color[2]

    textcolor = get_contrast_color(background_color) if auto_contrast_text else (0, 0, 0)
    # 绘制标题
    if title == "auto":
        title = os.path.basename(image_path)
    title_font = ImageFont.truetype(font_path, max(10, int(cell * 0.6)))
    tbbox = draw_final.textbbox((0, 0), title, font=title_font)
    tw = tbbox[2] - tbbox[0]
    draw_final.text(((new_img.width - tw) / 2, 10), title, fill=textcolor, font=title_font)

    # 绘制图例
    start_y = margin if legend_position == "top" else enlarged_h + margin * 1.5
    x_cursor, y_cursor = margin, start_y



    for i, (label, color, count) in enumerate(legend_items):
        # 绘制色块
        draw_final.rectangle([x_cursor, y_cursor, x_cursor + cell, y_cursor + cell], fill=color[:3], outline=textcolor)

        # 绘制文本
        text = f"{label} {count}"
        if show_color_value:
            text += f" #{color[0]:02X}{color[1]:02X}{color[2]:02X}"

        tbbox = draw_final.textbbox((0, 0), text, font=legend_font)
        text_y = y_cursor + (cell - (tbbox[3] - tbbox[1])) / 2
        draw_final.text((x_cursor + cell + 6, text_y), text, fill=textcolor, font=legend_font)

        # 移动到下一个位置
        x_cursor += max_item_width

        # 换行检查
        if x_cursor + max_item_width > enlarged_w + margin:
            x_cursor = margin
            y_cursor += cell * 1.5

    # 输出文件
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    # output_path = f"{os.path.splitext(image_path)[0]}{output_suffix}_{ts}.png"
    output_path = f"{os.path.splitext(image_path)[0]}{output_suffix}.png"
    new_img.save(output_path)
    print(f"✅ 输出文件: {output_path}")
    if debug_mode:
        print(f"🎨 颜色统计:")
        for label, color, count in legend_items:
            print(f"  {label}: RGB{color[:3]} - {count}次")


# -----------------------------
# CLI
# -----------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="像素画放大标注工具")
    parser.add_argument("image_path", help="输入图片路径")
    parser.add_argument("--config", help="JSON配置文件路径", required=True)
    args = parser.parse_args()

    config = load_config(args.config)
    config["image_path"] = args.image_path

    print("🧩 当前配置：")
    for k, v in config.items():
        print(f"  {k}: {v}")

    generate_pixel_art_preview(**config)