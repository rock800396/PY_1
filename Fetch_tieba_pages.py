# 这是针对百度贴吧翻页操作爬取的爬虫测试
# https://tieba.baidu.com/f?kw=flai&ie=utf-8&pn=50                  # 这是贴吧网址样式,用于构建参数字典,ie参数可以用,也可以带上
import requests
import urllib.parse
import os
from fake_useragent import UserAgent

# ----------------------------------- 引入Selenium库 ------------------------------------------ #
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager            # 自动管理ChromeDriver

url = 'https://tieba.baidu.com/f?'                                                  # 这是网址的基础格式
search_kw = input("请输入你要获取的贴吧名字:")                            # 这是贴吧的具体名字
pages = 10                                                                                  # 这你想要爬取的页数,代表想要在这个吧中爬取几页

# ----------------------------------- 配置代理 ------------------------------------ #
proxy_address = "http://127.0.0.1:10090"

# ---------------------- 解析URL,动态设置Host和Referer ----------------------- #
parsed_url = urllib.parse.urlparse(url)                                           # urllib.parse.urlparse() 会将URL分解成多个组件 (协议, 域名, 路径, 参数等)
dynamic_host = parsed_url.netloc                                               # 获取域名和端口，例如 www.baidu.com 或 example.com:8080
dynamic_referer = f"{parsed_url.scheme}://{parsed_url.netloc}/"  # 构造Referer，通常是协议+域名+斜杠，表示从网站根目录跳转而来

# ----------------------------------- 构建请求头 ------------------------------------ #
current_user_agent = UserAgent().random                                 # 为本次请求生成一个随机User-Agent，requests和Selenium都使用它
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": dynamic_host,                                                           # 根据URL解析,动态构造域名
    "Pragma": "no-cache",
    "Referer": dynamic_referer,                                                    # 根据URL解析,动态构造跳转来源
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",                                            # 或者 "none" 如果是直接访问
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": current_user_agent,                                        # 使用随机User-Agent
}
session = requests.Session()                                                        # 创建一个Session对象
session.headers.update(headers)                                             # 将headers设置到session中

chrome_options = Options()
chrome_options.add_argument("--headless")                                       # 无头模式，不显示浏览器界面
chrome_options.add_argument("--disable-gpu")                                 # 禁用GPU加速，某些系统上可能需要
chrome_options.add_argument("--no-sandbox")                                 # 禁用沙箱模式，某些Linux环境可能需要
chrome_options.add_argument(f"user-agent=current_user_agent")     # 设置User-Agent

for i in range(pages):                                                                          # 构建params参数,这是字典类型
    selenium_html_content = None                                                      # 用于存储获取二进制内容,每次循环开始重置为空
    pn = i * 50
    params = {
        'kw': search_kw,
        'ie': 'utf-8',
        'pn': pn
    }
    print(f"正在尝试进行第{i+1}个页面的获取...")                                        # 跟踪进度
    driver = None                                                                                   # 初始化driver为None，确保在finally块中可以用来安全检查

    try:  # 使用webdriver_manager自动下载并管理ChromeDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        print(f"初始化ChromeDriver失败: {e}")
        print("请检查网络连接或手动下载ChromeDriver并放置到系统PATH中.")

    try:
        driver.get(url)
        wait_timeout = 10                                                                                                                                   # 定义显式等待的最大超时时间
        WebDriverWait(driver, wait_timeout).until(ec.presence_of_element_located((By.TAG_NAME, 'body')))        # 等待页面中的<body>标签出现
        selenium_html_content = driver.page_source                                                                                           # Selenium获取的是字符串
    except Exception as e:
        print(f"Selenium访问失败: {e}")

    finally:
        if driver:                                                                                                                                                    # 确保driver对象已创建才尝试退出
            driver.quit()                                                                                                                                           # 确保关闭浏览器

    if selenium_html_content :
        file_name = f"{search_kw}_{i}.html"
        file_save = os.path.join(r"E:\Fetch resource\HTML", file_name)
        with open(f"") as f:
            f.write(selenium_html_content)