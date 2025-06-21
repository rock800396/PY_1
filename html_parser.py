# html_parser.py

import os
import shutil
from bs4 import BeautifulSoup


def extract_text_from_file(html_path, output_txt_path, target_tags=None):
    """
    从本地HTML文件中提取文本内容。

    参数:
        html_path (str): 源HTML文件的路径。
        output_txt_path (str): 保存提取文本的.txt文件的路径。
        target_tags (list, optional): 一个包含目标标签名的列表 (例如 ['p', 'h1'])。
                                      如果为None或空列表，则提取所有标签的文本。

    返回:
        str: 操作结果的描述信息。
    """
    try:
        # 使用 'utf-8' 编码打开HTML文件，这是最常见的网页编码
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return f"错误：源文件未找到 -> {html_path}"
    except Exception as e:
        return f"读取文件时发生错误: {e}"

    soup = BeautifulSoup(content, 'html.parser')

    # 如果没有指定目标标签，则查找所有标签
    # soup.find_all(True) 是一个技巧，可以匹配任何标签
    tags_to_process = soup.find_all(target_tags) if target_tags else soup.find_all(True)

    extracted_data = []
    for tag in tags_to_process:
        # 忽略脚本和样式标签，因为它们的内容不是我们想要的文本
        if tag.name in ['script', 'style']:
            continue

        # 获取标签内的纯文本，strip=True可以去除两端多余的空白
        text = tag.get_text(strip=True)

        # 如果标签内有有效文本，则记录下来
        if text:
            # 格式化输出，清晰地标明文本来源
            formatted_text = f"--- 来自标签: <{tag.name}> ---\n{text}\n\n"
            extracted_data.append(formatted_text)

    if not extracted_data:
        return "未在指定标签中找到任何可提取的文本。"

    try:
        # 将提取到的所有内容写入输出文件
        with open(output_txt_path, 'w', encoding='utf-8') as f:
            f.writelines(extracted_data)
        return f"文本提取成功！已保存到: {output_txt_path}"
    except Exception as e:
        return f"写入文件时发生错误: {e}"


def extract_images_from_file(html_path, output_dir):
    """
    从本地HTML文件中提取图片并保存到指定目录。
    假设图片路径是相对于HTML文件的相对路径。

    参数:
        html_path (str): 源HTML文件的路径。
        output_dir (str): 保存提取图片的目录。

    返回:
        str: 操作结果的描述信息。
    """
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return f"错误：源文件未找到 -> {html_path}"
    except Exception as e:
        return f"读取文件时发生错误: {e}"

    soup = BeautifulSoup(content, 'html.parser')

    # 找到所有的 <img> 标签
    img_tags = soup.find_all('img')

    if not img_tags:
        return "未在HTML文件中找到任何 <img> 标签。"

    # 获取HTML文件所在的目录，用于拼接图片的相对路径
    source_html_dir = os.path.dirname(html_path)

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    copied_count = 0
    errors = []

    for img in img_tags:
        # 获取图片的 src 属性
        src = img.get('src')
        if not src:
            continue

        # 假设 src 是相对路径，构建图片的完整源路径
        # os.path.join 会智能地处理路径分隔符（在Windows上是'\'）
        image_source_path = os.path.join(source_html_dir, src)

        # 检查图片文件是否存在
        if os.path.exists(image_source_path):
            try:
                # shutil.copy 会将文件从源路径复制到目标目录
                shutil.copy(image_source_path, output_dir)
                copied_count += 1
            except Exception as e:
                errors.append(f"无法复制图片 {src}: {e}")
        else:
            errors.append(f"图片文件未找到: {image_source_path}")

    result_message = f"操作完成。成功复制 {copied_count} 张图片。"
    if errors:
        result_message += "\n发生以下错误:\n" + "\n".join(errors)

    return result_message

