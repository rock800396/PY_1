# -----------------------------------爬虫实践和代码练习,我要把它做成一个强大的爬虫!------------------------------------------ #
import requests                                                                                    # 导入requests库
import re                                                                                               # 导入正则表达式库
import sys                                                                                             # 导入sys库,用于系统操作
import os                                                                                              # 导入os库,用于文件和目录操作
import time                                                                                           # 导入time库
import random                                                                                     # 导入random库
import urllib.parse                                                                                # 导入urllib.parse库,用于解析URL,动态获取Host和Referer

# ----------------------------------- 引入Selenium库 ------------------------------------------ #
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent                                                       # 导入User-Agent池模块
# from lxml import etree                                                                                   # 导入lxml库,用于解析HTML/XML文档,这里主要用于XPath解析,备用
from webdriver_manager.chrome import ChromeDriverManager            # 自动管理ChromeDriver

# ----------------------------------- Selenium 辅助函数：设置反检测WebDriver ------------------------------------------ #
def setup_undetected_driver(user_agent_str, proxy_address=None, headless=True, window_size=(1920, 1080)):
    """
    设置并返回一个配置了反检测措施的Selenium Chrome WebDriver实例。

    参数:
        user_agent_str (str): 用于WebDriver的User-Agent字符串。
        proxy_address (str, optional): 代理服务器地址，格式如 "http://ip:port"。默认为None。
        headless (bool): 是否以无头模式运行浏览器。默认为True。
        window_size (tuple): 浏览器窗口大小，例如 (1920, 1080)。

    返回:
        webdriver.Chrome: 配置好的WebDriver实例，如果初始化失败则返回None。
    """
    chrome_options = Options()

    if headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu") # 某些系统上无头模式需要
        chrome_options.add_argument("--no-sandbox")  # 某些Linux环境可能需要

    chrome_options.add_argument(f"user-agent={user_agent_str}")
    chrome_options.add_argument(f"--window-size={window_size[0]},{window_size[1]}")

    # --- 核心反检测措施 ---
    # 1. 禁用 'enable-automation' 标志，防止网站检测到 Selenium 自动化
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # 2. 禁用自动化扩展，进一步隐藏自动化痕迹
    chrome_options.add_experimental_option('useAutomationExtension', False)
    # 3. 禁用 Blink 引擎的自动化控制特性，更深层次的反检测
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    if proxy_address:
        chrome_options.add_argument(f'--proxy-server={proxy_address}')

    driver = None                               # 初始化WebDriver变量为None

    try:
        service = Service(ChromeDriverManager().install())                                                      # 自动下载并安装最新的ChromeDriver
        driver = webdriver.Chrome(service=service, options=chrome_options)                    # 创建Chrome WebDriver实例

        # --- 在页面加载前执行 JavaScript，进一步隐藏 'navigator.webdriver' ---
        # 这段JS会在每个新文档加载时执行，确保 navigator.webdriver 始终为 undefined
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            """
        })
        return driver
    except Exception as e:
        print(f"初始化ChromeDriver失败: {e}")
        print("请检查网络连接或手动下载ChromeDriver并放置到系统PATH中.")
        return None

# ----------------------------------- Selenium 辅助函数：获取页面内容 ------------------------------------------ #
def get_page_with_selenium_fallback(target_url, user_agent_str, proxy_address=None):
    """
    当requests库遇到反爬虫时，作为备用方案，使用Selenium（无头浏览器）访问指定URL并返回页面源代码。
    参数:
        target_url (str): 需要访问的URL。
        user_agent_str (str): 用于Selenium请求的User-Agent字符串。
        proxy_address:接收传入的代理地址,如果没有传入,则默认值为None,表示不使用代理
    返回:
        bytes: 成功获取的页面内容（UTF-8编码的字节），如果失败则返回None。
    """
    # 调用辅助函数setup_undetected_driver来设置WebDriver
    # 默认以无头模式运行，可以通过修改 headless=False 来查看浏览器操作
    driver = setup_undetected_driver(user_agent_str, proxy_address, headless=True)
    if driver is None:
        return None # WebDriver初始化失败，直接返回

    try:
        print(f"正在尝试使用Selenium访问: {target_url},请稍候......")
        driver.get(target_url)

        # --- 模拟人类行为：随机滚动页面 ---
        # 这有助于模拟用户浏览行为，降低被检测为机器人的风险
        scroll_height = driver.execute_script("return document.body.scrollHeight")
        # 随机滚动到页面中间某个位置
        driver.execute_script(f"window.scrollTo(0, {random.uniform(0.2, 0.8) * scroll_height});")
        time.sleep(random.uniform(1, 2)) # 滚动后等待片刻
        # 随机滚动回顶部或另一个位置
        driver.execute_script(f"window.scrollTo(0, {random.uniform(0, 0.2) * scroll_height});")
        time.sleep(random.uniform(1, 2)) # 再次等待

        wait_timeout = 15 # 增加等待时间，给JavaScript更多时间执行和反爬虫逻辑处理
        WebDriverWait(driver, wait_timeout).until(ec.presence_of_element_located((By.TAG_NAME, 'body')))
        print(f"Selenium页面加载完成（等待最长{wait_timeout}秒）。")

        # 检查页面是否是验证码页面,如果是,还需要构建相关的反反爬措施,等待后续施工
        # 需要根据验证码页面的HTML结构来判断,例如，如果验证码页面有一个特定的ID或class,这里先用粗略的字符串判断,等待后续施工
        if "滑块验证" in driver.page_source or "captcha" in driver.current_url: # 粗略判断
            print("Selenium检测到验证码页面，无法自动绕过。")
            # driver.save_screenshot("captcha_page.png") # 可以选择保存截图以便分析
            return None

        selenium_html_content = driver.page_source
        print("Selenium成功获取页面！")
        return selenium_html_content.encode('utf-8')                # 将HTML内容编码为UTF-8字节串,这里是为了与requests的content保持一致,方便保存为文件
        # return selenium_html_content                                      # 如果需要直接返回字符串,可以去掉.encode('utf-8')部分,用这一句代替
    except Exception as e:
        print(f"Selenium访问失败: {e}")
        return None
    finally:
        if driver:
            driver.quit()
            print("Selenium浏览器已关闭。")


# ----------------------------------- 主程序入口 ------------------------------------------ #
if __name__ == "__main__":
    pattern = r'^(https?://)?([a-zA-Z0-9.-]+)(:[0-9]+)?(/.*)?$'                     # 检查网址合法性的正则表达式

    """
    根据计算机中的目录结构来构建以下存储变量,把获取/爬取的内容自动按照文件类型保存在对应目录中
    例如,当获取的是一首歌曲时,只需要修改file_name的值和file_type[0]中的脚标即可
    """
    file_dir = r"D:\Fetch resource"
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

    while True:                                                                                                 # 使用while循环,直到用户输入合法的URL,实践中需要限制输入次数,这里暂不考虑
        url = input("请输入需要爬取的URL:")                                                    # 接收用户输入的URL
        if re.match(pattern, url) is None:                                                          # 如果网址不合法,则抛出异常
            print("输入的网址不合法,请检查后重新输入!")
            continue                                                                                             # 继续下一轮循环，重新输入URL

        if not url.startswith(('http://', 'https://')):                                             # 默认添加http/https,确保网址包含协议头
            url = 'https://' + url

        # ---------------------- 解析URL,动态设置Host和Referer ----------------------- #
        parsed_url = urllib.parse.urlparse(url)                                                                 # urllib.parse.urlparse() 会将URL分解成多个组件 (协议, 域名, 路径, 参数等)
        dynamic_host = parsed_url.netloc                                                                       # 获取域名和端口，例如 www.baidu.com 或 example.com:8080
        dynamic_referer = f"{parsed_url.scheme}://{parsed_url.netloc}/"                     # 构造Referer，通常是协议+域名+斜杠，表示从网站根目录跳转而来

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
            "User-Agent": current_user_agent,                                                  # 使用随机User-Agent要特别注意,在多次请求同一网站并保持cookie时,User-Agent最好保持一致,否则可能会被网站识别为不同的用户
        }
        session.headers.update(headers)                                                        # 将headers设置到session中

        if use_selenium_directly:
            print("根据设置，直接使用Selenium获取页面。")
            final_content_to_save = get_page_with_selenium_fallback(url, current_user_agent, selenium_proxy_address)
            break                                                                                                 # 无论Selenium成功与否,都跳出while循环,转由while循环后面的逻辑来执行
        else:
            try:
                print(f"尝试使用requests访问: {url}")
                time.sleep(random.uniform(1, 3))                                     # 随机延时1到3秒,模拟人类行为,防止请求过快被封IP
                response = session.get(url,timeout=10,proxies=my_proxies)     # 使用session发送GET请求,比直接使用requests.get()更合适,session是会话级请求,会自动处理cookies,更适合需要多次请求的场景
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
                    print("Selenium也未能成功获取页面。请检查网络或反爬虫策略。")
                break                                                                                                                                           # 无论Selenium是否成功，都跳出while循环,上面的if语句只是用于跟踪程序执行情况,不影响逻辑

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
        print("未能成功获取或保存,请检查网络连接或反爬虫策略。")                                                         # 如果final_content_to_save仍然是None,说明没有成功获取内容