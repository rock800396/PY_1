# ------------代码练习:使用beautifulsoup解析已爬取的html文件------------
from bs4 import BeautifulSoup
file_path = r"E:\Fetch resource\Html\测试.html"
file_local = None
try:
    # 1. 使用 "rb" 模式打开文件，表示以二进制模式读取
    with open(file_path, "rb") as f:
        # 2. 读取文件所有内容，得到的是bytes类型，decode('utf-8')将bytes解码为str（文本格式）
        file_local = f.read().decode('utf-8')
except FileNotFoundError:
    print(f"错误：文件未找到，请检查路径: {file_path}")
except UnicodeDecodeError as e:
    print(f"错误：解码文件时发生问题，可能是编码不匹配。错误信息: {e}")
    print("请尝试使用其他编码，例如 'gbk' 或 'latin-1'，或者在decode时添加 errors='ignore'")
except Exception as e:
    print(f"读取文件时发生未知错误: {e}")

if file_local:
    # 3. 将解码后的字符串传递给BeautifulSoup进行解析
    print("\n--- 使用BeautifulSoup解析本地HTML内容 ---")
    soup = BeautifulSoup(file_local, 'lxml')

    # 这个模块是获取便签span中的文本,文本是商品名称
    product_name = []
    product_items = soup.find_all('div', class_='info-wrapper-title')
    for item in product_items:
        item_name = item.find('span', class_='info-wrapper-title-text').text
        product_name.append(item_name)
    # 打印获取的元素,每5个元素换行,以便查看
    chunk_size = 5
    for i in range(0, len(product_name), chunk_size):
        chunk = product_name[i:i + chunk_size]
        print(" ".join(chunk))
    print(f"\n总共解析到 {len(product_name)} 个产品名称。")

    # 这个模块是获取链接地址,注意地址必须以http开头,否则跳过
    product_url = soup.find_all('a',attrs={'data-nid': True, 'href': True})
    url_all = []
    for url in product_url:
        url_herf = url.get("href")
        # 如果url为空,进入下一轮for循环
        if url_herf is None or url_herf.strip() == "":
            continue
        # 如果url不是以http或者https开头,进入下一轮for循环
        if not url_herf.startswith('http://') and not url_herf.startswith('https://'):
            continue
        url_all.append(url_herf)
        # 直接打印出来,默认会自动换行,同时url_all已保存了网址
        print(url_herf)
else:
    print("未能成功读取或解码HTML内容，无法进行解析。")