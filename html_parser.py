# html_parser.py (最终版 v4.0 - 融合精华)

import os
import shutil
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import defaultdict
from PIL import Image  # 重新导入Pillow库用于图片处理
from io import BytesIO


# 确保你已经安装了所有必要的库:
# pip install requests beautifulsoup4 lxml Pillow

def extract_text_from_file(html_filepath, output_txt_path, target_tags=None):
    """
    从HTML文件中提取文本，并按标签分类保存。
    (融合了你喜欢的GitHub增强版逻辑)
    """
    try:
        with open(html_filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'lxml')
    except FileNotFoundError:
        return f"错误: 源文件未找到 {html_filepath}"
    except Exception as e:
        return f"读取文件时发生错误: {e}"

    tags_to_process = soup.find_all(target_tags) if target_tags else soup.find_all(True)

    # 使用 defaultdict 按标签名对文本进行分类
    texts_by_tag = defaultdict(list)
    for tag in tags_to_process:
        if tag.name in ['script', 'style', 'meta', 'link', 'head', 'title']:
            continue
        text = tag.get_text(strip=True)
        if text:
            texts_by_tag[tag.name].append(text)

    if not texts_by_tag:
        return "未在指定标签中找到任何可提取的文本。"

    # 格式化并准备写入文件的最终数据
    final_output_data = []
    for tag_name, texts in sorted(texts_by_tag.items()):  # 按标签名排序，更整洁
        final_output_data.append(f"--- 来自所有 <{tag_name}> 标签的文本 ---\n\n")
        final_output_data.append("\n\n".join(texts))  # 段落间用双换行分隔，更清晰
        final_output_data.append("\n\n" + "=" * 40 + "\n\n")

    try:
        with open(output_txt_path, 'w', encoding='utf-8') as f:
            f.writelines(final_output_data)
        return f"文本提取成功！已分类保存到: {output_txt_path}"
    except Exception as e:
        return f"写入文件时发生错误: {e}"


def extract_images_generator(html_filepath, output_dir, min_width=320, min_height=240):
    """
    这是一个生成器函数，用于提取、过滤(按分辨率)并下载图片。
    (融合了你喜欢的GitHub增强版逻辑)
    """
    saved_count = 0
    skipped_count = 0

    yield "任务开始：正在解析HTML文件..."

    try:
        with open(html_filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'lxml')
    except FileNotFoundError:
        yield f"错误: 源文件未找到 {html_filepath}"
        return
    except Exception as e:
        yield f"解析HTML时出错: {e}"
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        yield f"已创建输出目录: {output_dir}"

    base_url = 'file:///' + os.path.abspath(html_filepath).replace('\\', '/')
    images = soup.find_all('img')

    if not images:
        yield "未在文件中找到任何 <img> 标签。"
    else:
        yield f"共找到 {len(images)} 个 <img> 标签，开始处理..."
        yield f"将跳过分辨率小于 {min_width}x{min_height} 的图片。"

    for img_tag in images:
        src = img_tag.get('src')
        if not src:
            skipped_count += 1
            yield "跳过：一个<img>标签没有src属性。"
            continue

        try:
            abs_url = urljoin(base_url, src)
            parsed_path = urlparse(abs_url).path
            filename = os.path.basename(parsed_path) if parsed_path else None

            if not filename:
                skipped_count += 1
                yield f"跳过：无法从URL解析出文件名 -> {src}"
                continue

            # --- 融合逻辑：下载并检查分辨率 ---
            yield f"检查: {filename} ..."

            image_data_bytes = None
            # 判断是网络图片还是本地文件
            if abs_url.startswith('http'):
                response = requests.get(abs_url, timeout=10)
                response.raise_for_status()
                image_data_bytes = response.content
            else:
                source_path = urlparse(abs_url).path
                if os.name == 'nt' and source_path.startswith('/'):
                    source_path = source_path[1:]
                if os.path.exists(source_path):
                    with open(source_path, 'rb') as f:
                        image_data_bytes = f.read()
                else:
                    skipped_count += 1
                    yield f"跳过(未找到): 本地文件 {source_path}"
                    continue

            if not image_data_bytes:
                skipped_count += 1
                yield f"跳过: 未能获取图片数据 -> {filename}"
                continue

            # 使用Pillow在内存中检查图片
            image_stream = BytesIO(image_data_bytes)
            with Image.open(image_stream) as img_obj:
                width, height = img_obj.size

            yield f"  > 分辨率: {width}x{height}"

            # 判断分辨率
            if width < min_width or height < min_height:
                skipped_count += 1
                yield f"  > 跳过 (尺寸太小)"
                continue

            # 分辨率符合，保存图片
            save_path = os.path.join(output_dir, filename)
            with open(save_path, 'wb') as f:
                f.write(image_data_bytes)

            saved_count += 1
            yield f"  > 已保存: {filename}"

        except Exception as e:
            skipped_count += 1
            # 简化错误信息，避免刷屏
            error_type = type(e).__name__
            yield f"失败: 处理 {src} 时出错 ({error_type})"

    yield f"\n--- 任务完成 ---\n共保存 {saved_count} 张图片，跳过 {skipped_count} 张。"
