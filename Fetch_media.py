# -----------------------------------爬虫实践和代码练习,我要把它做成一个强大的爬虫!------------------------------------------ #
from fake_useragent import UserAgent                                            # 导入User-Agent池模块
import requests                                                                                    # 导入requests库
import re                                                                                               # 导入正则表达式库
import sys                                                                                             # 导入sys库,用于系统操作
import os                                                                                              # 导入os库,用于文件和目录操作
import time                                                                                           # 导入time库
import random                                                                                     # 导入random库
import urllib.parse                                                                                 # 导入urllib.parse库,用于解析URL,动态获取Host和Referer

# ----------------------------------- 引入Selenium库 ------------------------------------------ #
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager            # 自动管理ChromeDriver

# ----------------------------------- Selenium 辅助函数 ------------------------------------------ #
def get_page_with_selenium_fallback(target_url, user_agent_str,proxy_address=None):
    """
    当requests库遇到反爬虫时，作为备用方案，使用Selenium（无头浏览器）访问指定URL并返回页面源代码。
    参数:
        target_url (str): 需要访问的URL。
        user_agent_str (str): 用于Selenium请求的User-Agent字符串。
        proxy_address:接收传入的代理地址,如果没有传入,则默认值为None,表示不使用代理
    返回:
        bytes: 成功获取的页面内容（UTF-8编码的字节），如果失败则返回None。
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")                                         # 无头模式，不显示浏览器界面
    chrome_options.add_argument("--disable-gpu")                                   # 禁用GPU加速，某些系统上可能需要
    chrome_options.add_argument("--no-sandbox")                                   # 禁用沙箱模式，某些Linux环境可能需要
    chrome_options.add_argument(f"user-agent={user_agent_str}")         # 设置传入的User-Agent
    if proxy_address:                                                                                              # 如果提供了代理地址(通过形参传入),则配置代理
        chrome_options.add_argument(f'--proxy-server={proxy_address}')
        print(f"Selenium将使用代理: {proxy_address}")

    driver = None                                                                                             # 初始化driver为None，确保在finally块中可以用来安全检查

    try:                                                                                                                # 使用webdriver_manager自动下载并管理ChromeDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        print(f"初始化ChromeDriver失败: {e}")
        print("请检查网络连接或手动下载ChromeDriver并放置到系统PATH中.")
        return None                                                                                             # 初始化失败,结束函数执行并返回None

    try:
        print(f"尝试使用Selenium访问: {target_url}")
        driver.get(target_url)
        # time.sleep(random.uniform(3, 7))                                            # 增加等待时间，确保页面加载和JavaScript执行完成，随机延时更自然,已经用下面的显式等待替换
        wait_timeout = 10                                                                               # 定义显式等待的最大超时时间
        WebDriverWait(driver, wait_timeout).until(ec.presence_of_element_located((By.TAG_NAME, 'body')))                           # 等待页面中的<body>标签出现
        print(f"Selenium页面加载完成（等待最长{wait_timeout}秒）。")
        selenium_html_content = driver.page_source                                      # Selenium获取的是字符串
        print("Selenium成功获取页面！")                                                           # 执行到这里都没有发生异常,说明成功获取页面
        return selenium_html_content.encode('utf-8')                                      # 将字符串编码转为二进制返回,主要是为了与response.content格式一致,可以被with open语句处理
    except Exception as e:
        print(f"Selenium访问失败: {e}")
        return None                                                                                             # 访问失败,结束函数执行并返回None
    finally:
        if driver:                                                                                                   # 确保driver对象已创建才尝试退出
            driver.quit()                                                                                         # 确保关闭浏览器


# ----------------------------------- 主程序入口 ------------------------------------------ #
if __name__ == "__main__":
    pattern = r'^(https?://)?([a-zA-Z0-9.-]+)(:[0-9]+)?(/.*)?$'                     # 检查网址合法性的正则表达式

    """
    根据计算机中的目录结构来构建以下存储变量,把获取/爬取的内容自动按照文件类型保存在对应目录中
    例如,当获取的是一首歌曲时,只需要修改file_name的值和file_type[0]中的脚标即可
    """
    file_dir = r"E:\Fetch resource"
    file_type = ["Music", "Video", "Picture", "Text", "HTML", "Other"]
    file_name = "测试.html"
    file_path = os.path.join(file_dir, file_type[4], file_name)

    final_content_to_save = None                                                                  # 定义一个变量来存储最终要保存的内容，无论是来自requests还是Selenium
    session = requests.Session()                                                                    # 创建一个Session对象

    # ----------------------------------- 配置代理 ------------------------------------ #
    my_proxies = {
        "http": "http://127.0.0.1:10090",  # 你的本地HTTP代理地址
        "https": "http://127.0.0.1:10090", # HTTPS请求也通过这个HTTP代理
    }
    selenium_proxy_address = "http://127.0.0.1:10090"                            # Selenium使用的代理地址,在调用Selenium辅助函数get_page_with_selenium_fallback函数时作为实参传入

    # ----------默认设置为False,保持现有逻辑,如果设置为 True ,直接跳过request尝试,使用Selenium---------- #
    use_selenium_directly = False

    while True:                                                                                                 # 使用while循环,直到用户输入合法的URL
        url = input("请输入需要爬取的URL:")                                                    # 接收用户输入的URL
        if re.match(pattern, url) is None:                                                         # 如果网址不合法,则抛出异常
            print("输入的网址不合法,请检查后重新输入!")
            continue                                                                                             # 继续下一轮循环，重新输入URL

        if not url.startswith(('http://', 'https://')):                                                 # 默认添加http/https,确保网址包含协议头
            url = 'https://' + url

        # ---------------------- 解析URL,动态设置Host和Referer ----------------------- #
        parsed_url = urllib.parse.urlparse(url)                                                                   # urllib.parse.urlparse() 会将URL分解成多个组件 (协议, 域名, 路径, 参数等)
        dynamic_host = parsed_url.netloc                                                                       # 获取域名和端口，例如 www.baidu.com 或 example.com:8080
        dynamic_referer = f"{parsed_url.scheme}://{parsed_url.netloc}/"                          # 构造Referer，通常是协议+域名+斜杠，表示从网站根目录跳转而来

        # ----------------------------------- 构建请求头 ------------------------------------ #
        current_user_agent = UserAgent().random                                        # 为本次请求生成一个随机User-Agent，requests和Selenium都使用它
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Host": dynamic_host,                                                                    # 根据URL解析,动态构造域名
            "Pragma": "no-cache",
            "Referer": dynamic_referer,                                                             # 根据URL解析,动态构造跳转来源
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",                                                      # 或者 "none" 如果是直接访问
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": current_user_agent,                                                  # 使用随机User-Agent
        }
        session.headers.update(headers)                                                        # 将headers设置到session中

        if use_selenium_directly:
            print("根据设置，直接使用Selenium获取页面。")
            final_content_to_save = get_page_with_selenium_fallback(url, current_user_agent, selenium_proxy_address)
            break                                                                                           # 无论Selenium成功与否,都跳出while循环,转由while循环后面的逻辑来执行
        else:
            try:
                print(f"尝试使用requests访问: {url}")
                time.sleep(random.uniform(1, 3))                                     # 随机延时1到3秒,模拟人类行为,防止请求过快被封IP
                response = session.get(url,timeout=10,proxies=my_proxies)         # 使用session发送GET请求,比直接使用requests.get()更合适,session是会话级请求,会自动处理cookies,更适合需要多次请求的场景
                response.raise_for_status()                                                              # 如果状态码不是2xx,会抛出HTTPError异常,注意,30X重定向会被request模块自动处理,不会抛出异常
                final_content_to_save = response.content                                     # 保存获取的内容
                print("requests成功获取页面！")                                                      # 到这里都没有发生异常,说明成功获取页面
                break                                                                                                  # requests成功，跳出循环

            except requests.exceptions.RequestException as e:
                print(f"requests请求失败 ({type(e).__name__}): {e}。尝试使用Selenium回退...")                      # 利用魔法属性打印具体的异常类型和信息
                final_content_to_save = get_page_with_selenium_fallback(url, current_user_agent, selenium_proxy_address)
                """
                final_content_to_save的判断逻辑:
                能执行到这里,说明requests是失败的,那么final_content_to_save在这个except块执行之前就是初始的空值None
                get_page_with_selenium_fallback函数如果失败,也是返回None
                只有当Selenium成功获取到内容,才会返回非空的二进制数据,赋值给final_content_to_save
                """
                if final_content_to_save:
                    break                                                                                                                                       # Selenium成功，跳出while循环
                else:
                    print("Selenium也未能成功获取页面。请检查网络或反爬虫策略。")
                    break                                                                                                                                       # 即使失败了也跳出循环,如果想从头开始下一轮循环,这里改成continue即可
            except Exception as e:                                                                                                                   # 捕获其他未知异常
                print(f"发生未知错误: {e}")                                                                                                          # 打印异常信息
                sys.exit(2)                                                                                                                                    # 退出程序,错误码2用来跟踪未知错误

    # while循环结束后，如果成功获取到内容（有可能来自requests,也有可能来自Selenium），则保存文件
    if final_content_to_save:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)                                                            # 确保目录存在,不存在则创建,exist_ok=True表示如果目录已经存在也不报错
        with open(file_path, "wb") as f:                                                                                                     # 保存爬取的文件
             f.write(final_content_to_save)
        print(f"恭喜大侠!文件已成功下载,位置: {file_path}")
    else:
        print("未能成功获取任何内容并保存。")