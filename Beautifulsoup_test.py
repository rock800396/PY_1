# ------------代码练习:使用beautifulsoup解析已爬取的html文件------------
from bs4 import BeautifulSoup
from bs4 import Tag
import requests
file_path = r"E:\Fetch resource\Html\测试.html"
file_local = None
try:
    # 使用 "rb" 模式打开文件，表示以二进制模式读取,encoding="utf-8"表示将在读取时进行解码file_local为字符串
    with open(file_path, "r", encoding="utf-8") as f:
        file_local = f.read()
except FileNotFoundError:
    print(f"错误：文件未找到，请检查路径: {file_path}")
except UnicodeDecodeError as e:
    print(f"错误：解码文件时发生问题，可能是编码不匹配。错误信息: {e}")
    print("请尝试使用其他编码，例如 'gbk' 或 'latin-1'，或者在decode时添加 errors='ignore'")
except Exception as e:
    print(f"读取文件时发生未知错误: {e}")

headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"}

if file_local:
    # 将解码后的字符串传递给BeautifulSoup进行解析
    print("\n--- 使用BeautifulSoup解析本地HTML内容 ---")
    soup = BeautifulSoup(file_local, 'lxml')
    # 这里可以根据实际情况设置检索条件
    img_tags = soup.find_all("img")
    img_serial = 1
    for img_tag in img_tags:
        img_url = str(img_tag.get("src")) if isinstance(img_tag, Tag) and img_tag.get("src") else None
        if img_url:
            try:
                filename = fr"E:\Fetch resource\Picture\IMG_{img_serial}.jpg"
                img_serial += 1
                response = requests.get(img_url, headers=headers)
                response.raise_for_status()
                with open(filename, "wb") as f:
                    f.write(response.content)
                print(f"图片已保存在: {filename}")
            except requests.exceptions.RequestException as e:
                print(f"下载图片 {img_url} 失败: {e}")
            except IOError as e:
                filename = 'unknown_file_path'
                print(f"保存图片 {filename} 失败: {e}")
else:
    print("未能成功读取或解码HTML内容，无法进行解析。")