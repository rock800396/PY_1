# ================================================================================== #
#                                                                                    #
#                      一个强大的、智能的、通用的动态网页爬虫框架                      #
#                             --- 完美主义最终版 v2.0 ---                              #
#                                                                                    #
# ================================================================================== #

"""
本脚本是一个智能网页爬虫框架，旨在通用地处理静态和动态网页的抓取任务。

核心特性:
1.  智能调度: 默认优先使用轻量级的 `requests` 库进行快速尝试。如果失败或用户判断内容不完整，
    可自动或手动切换到功能强大的 `Selenium` 进行深度抓取。
2.  动态内容处理: 利用 `Selenium` 和 `undetected-chromedriver` 模拟真人浏览器行为，
    能够有效执行JavaScript，等待AJAX加载，并模拟滚动以触发懒加载内容，从而获取最完整的页面HTML。
3.  反爬虫对抗:
    - 使用 `undetected-chromedriver` 绕过常见的Cloudflare、Akamai等爬虫检测。
    - 使用 `fake-useragent` 动态生成随机的User-Agent，避免被服务器识别为固定脚本。
    - 支持配置HTTP/HTTPS代理，隐藏真实IP地址。
4.  智能分析: 在 `Selenium` 模式下，脚本能自动分析页面结构，通过启发式规则（如语义化标签、
    常用ID/class关键词）来定位关键内容区域，并以此作为动态内容加载完成的判断依据。
5.  高度可配置: 所有核心参数，如保存路径、代理、运行模式（是否无头）、超时时间等，
    均在全局配置中心统一设置，方便用户根据不同任务进行调整。
"""

# ----------------------------------- 基础与核心库导入 ------------------------------------------ #
import os
import random
import re
import sys
import time
# from urllib.parse import urlparse
import requests

# ----------------------------------- 强大的Selenium与相关模块导入 ------------------------------------------ #
# 使用undetected_chromedriver来增强Selenium的隐蔽性，使其更难被网站检测到
import undetected_chromedriver as uc
# WebDriverWait和expected_conditions用于实现智能等待，是处理动态网页的关键
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# By模块提供了多种定位网页元素的方式（如ID, CSS_SELECTOR等）
from selenium.webdriver.common.by import By
# fake_useragent库可以方便地生成各种浏览器的User-Agent字符串
from fake_useragent import UserAgent
# webdriver_manager可以自动下载和管理与当前Chrome浏览器版本匹配的ChromeDriver
from webdriver_manager.chrome import ChromeDriverManager
# 导入Beautifulsoup和lxml模块用于后续数据解析
# from bs4 import BeautifulSoup
# from lxml import etree
# ActionChains用于模拟更复杂的用户操作，如鼠标悬停、拖拽等（本脚本暂未深度使用）
# from selenium.webdriver.common.action_chains import ActionChains

# ================================================================================== #
#                                                                                    #
#                      --- 全局配置中心 (可在此处修改所有手动设置) ---                      #
#                                                                                    #
# ================================================================================== #

# --- 1. 文件与路径配置 ---
# 爬取文件保存的基础目录，请确保该路径存在或程序有权限创建
SAVE_DIR_BASE = r"E:\Fetch resource"
# 文件分类子目录列表 (仅供参考，用于规范化命名)
SAVE_SUB_DIRS = ["Music", "Video", "Picture", "Text", "HTML", "Other"]
# **【新配置】** 指定本次运行要使用的子目录名称，必须是上面列表中的一个
SAVE_SUB_DIR_TARGET = "HTML"
# 当无法从URL中解析出文件名时，使用的默认保存文件名
DEFAULT_FILENAME = "测试.html"

# --- 2. 代理配置 ---
# 如果不需要代理，请将下面的值设为 None。如果需要，请填写完整的代理地址
# 示例: "http://127.0.0.1:10090" 或 "socks5://127.0.0.1:1080"
PROXY_ADDRESS = "http://127.0.0.1:10090"

# --- 3. 核心策略与行为配置 ---
# 是否直接使用Selenium模式。True: 跳过requests，直接用Selenium；False: 优先用requests，失败或不满意再用Selenium
USE_SELENIUM_DIRECTLY = True
# Selenium是否以无头模式运行。True: 不会弹出浏览器窗口，在后台运行；False: 会弹出真实的浏览器窗口，方便调试
RUN_HEADLESS = True
# Selenium等待关键动态元素加载的超时时间（秒）。如果页面加载很慢，可以适当增加此值
SELENIUM_WAIT_TIMEOUT = 20
# 模拟滚动页面时，每次滚动操作后等待内容加载的随机时间范围（秒），模拟人类行为
SCROLL_WAIT_TIME_RANGE = (1.5, 2.5)


# ================================================================================== #
#                                                                                    #
#                            --- 核心功能函数 (请勿轻易修改) ---                           #
#                                                                                    #
# ================================================================================== #

def setup_undetected_driver(user_agent_str, proxy_address=None):
    """
    初始化并配置一个undetected_chromedriver实例。

    Args:
        user_agent_str (str): 要设置的User-Agent字符串。
        proxy_address (str, optional): 代理服务器地址。如果提供，则为浏览器配置代理。Defaults to None.

    Returns:
        uc.Chrome: 配置好的Chrome浏览器驱动实例，如果初始化失败则返回None。
    """
    chrome_options = uc.ChromeOptions()

    # 根据全局配置决定是否以无头模式运行
    if RUN_HEADLESS:
        chrome_options.add_argument("--headless=new")  # "new"是推荐的无头模式参数

    # 设置自定义的User-Agent
    chrome_options.add_argument(f"user-agent={user_agent_str}")
    # 设置一个较大的窗口尺寸，避免因窗口太小导致页面布局变化，影响元素定位
    chrome_options.add_argument("--window-size=1920,1080")

    # 如果提供了代理地址，则为浏览器添加代理配置
    if proxy_address:
        chrome_options.add_argument(f'--proxy-server={proxy_address}')

    try:
        # 使用webdriver_manager自动安装或查找匹配的chromedriver
        print("正在检查并准备ChromeDriver...")
        driver_path = ChromeDriverManager().install()
        print("ChromeDriver准备就绪。")
        # 返回初始化后的uc.Chrome实例
        return uc.Chrome(driver_executable_path=driver_path, options=chrome_options)
    except Exception as e:
        print(f"初始化undetected-chromedriver失败: {e}")
        print("请检查：1. Chrome浏览器是否已安装。 2. 网络连接是否正常。 3. 代理是否影响了ChromeDriver的下载。")
        return None


def generate_site_config(driver, url):
    """
    智能分析给定URL的页面结构，生成用于等待关键内容加载的定位器配置。
    这是一种启发式方法，通过查找常见的语义化标签和关键词来确定页面的主要内容区域。

    Args:
        driver (uc.Chrome): Selenium浏览器驱动实例。
        url (str): 需要分析的页面URL。

    Returns:
        dict: 包含等待定位器列表的配置字典，例如 {"wait_locators": [(By.TAG_NAME, 'main'), ...]}.
              如果分析失败，则返回None。
    """
    print("\n--- 进入智能分析模式 ---")
    try:
        # 首次访问页面以获取DOM结构
        driver.get(url)
        time.sleep(5)  # 等待一个初步的渲染时间
        print("正在智能分析页面结构，寻找关键内容区域...")

        # 定义用于启发式搜索的关键词和HTML标签
        keywords = ['main', 'content', 'container', 'list', 'article', 'search', 'app', 'footer']
        semantic_tag = ['main', 'footer', 'article', 'aside']

        found_locators = []

        # 优先查找具有明确语义的HTML5标签
        for tag in semantic_tag:
            if driver.find_elements(By.TAG_NAME, tag):
                print(f"  [启发式命中] 发现语义化标签: <{tag}>")
                found_locators.append((By.TAG_NAME, tag))

        # 其次，通过CSS选择器查找ID或class属性中包含常见关键词的元素
        for keyword in keywords:
            # 构造两个CSS选择器：一个匹配id，一个匹配class
            selectors = [f'[id*="{keyword}"]', f'[class*="{keyword}"]']
            for selector in selectors:
                if driver.find_elements(By.CSS_SELECTOR, selector):
                    print(f"  [启发式命中] 发现含关键词 '{keyword}' 的元素 (选择器: {selector})")
                    found_locators.append((By.CSS_SELECTOR, selector))

        # 如果没有找到任何可用的定位器，则分析失败
        if not found_locators:
            print("智能分析失败：未能根据启发式规则找到任何可用于等待的关键元素。")
            return None

        # 对找到的定位器进行去重，并返回最终配置
        unique_locators = list(set(found_locators))
        print("\n智能分析成功！生成以下等待定位器:")
        for loc in unique_locators:
            print(f"  - {loc}")
        return {"wait_locators": unique_locators}
    except Exception as e:
        print(f"智能分析过程中发生错误: {e}")
        return None


def fetch_page_with_selenium(url, user_agent_str, proxy_address=None):
    """
    使用Selenium完整地抓取一个动态网页。
    流程包括：启动浏览器 -> 智能分析 -> 正式访问 -> 智能等待 -> 模拟滚动 -> 获取最终HTML。

    Args:
        url (str): 目标网页URL。
        user_agent_str (str): 用于浏览器实例的User-Agent。
        proxy_address (str, optional): 代理服务器地址。Defaults to None.

    Returns:
        bytes: 成功抓取到的、经过UTF-8编码的页面HTML内容。如果失败则返回None。
    """
    try:
        # 使用with语句管理浏览器实例，确保任务结束或出错时浏览器能被自动关闭
        with setup_undetected_driver(user_agent_str, proxy_address) as driver:
            if driver is None: return None  # 如果驱动初始化失败，直接返回

            # 调用智能分析函数，获取等待策略
            site_config = generate_site_config(driver, url)
            if not site_config: return None  # 如果分析失败，也直接返回

            print(f"\n--- 开始正式爬取 ---")
            print(f"正在访问: {url}, 请稍候......")
            driver.get(url)

            print(f"页面初步加载，现在开始等待关键动态内容（最长{SELENIUM_WAIT_TIMEOUT}秒）...")
            # 根据智能分析的结果，构建一个等待条件列表
            wait_conditions = [EC.presence_of_element_located(loc) for loc in site_config["wait_locators"]]
            # 使用EC.any_of，只要满足列表中的任意一个条件（即任意一个关键元素出现），等待就结束
            WebDriverWait(driver, SELENIUM_WAIT_TIMEOUT).until(EC.any_of(*wait_conditions))
            print("关键动态内容已加载！")

            print("正在模拟滚动页面，以触发所有惰性加载内容...")
            # 获取当前页面的总高度
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                # 执行JavaScript将页面滚动到底部
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # 等待一段随机时间，让懒加载的内容有时间呈现
                time.sleep(random.uniform(SCROLL_WAIT_TIME_RANGE[0], SCROLL_WAIT_TIME_RANGE[1]))
                # 获取滚动后的新高度
                new_height = driver.execute_script("return document.body.scrollHeight")
                # 如果新旧高度相同，说明已经滚动到底，无法再加载更多内容，退出循环
                if new_height == last_height:
                    break
                last_height = new_height
            print("已滚动至页面底部。")

            # 获取经过所有动态加载和滚动后最终渲染完成的页面源代码
            final_html_content = driver.page_source
            print("Selenium成功获取渲染后的完整页面！")
            # 将字符串编码为bytes，与requests.content的类型保持一致
            return final_html_content.encode('utf-8')
    except Exception as e:
        # 捕获在整个Selenium流程中可能发生的任何异常（如超时、元素找不到等）
        print(f"在Selenium主流程中发生错误: {e}")
        return None


# ----------------------------------- 主函数逻辑 ------------------------------------------ #
def main():
    """
    程序的主执行函数，负责整个爬取流程的调度。
    包括用户交互、请求头构建、智能策略选择（requests或Selenium）、结果保存等。
    """
    # --- 1. 初始化路径和代理 ---
    # 使用os.path.join来安全地拼接路径，它会自动处理不同操作系统下的路径分隔符
    file_path = os.path.join(SAVE_DIR_BASE, SAVE_SUB_DIR_TARGET, DEFAULT_FILENAME)
    # 为requests库准备代理字典，如果PROXY_ADDRESS为None，则proxies也为None
    requests_proxies = {"http": PROXY_ADDRESS, "https": PROXY_ADDRESS} if PROXY_ADDRESS else None

    # --- 2. 用户交互 ---
    url = input("请输入需要爬取的URL: ")
    # 简单的URL格式校验和补全，确保URL以http://或https://开头
    if not re.match(r'^(https?://)', url):
        url = 'https://' + url

    # --- 3. 构建通用请求头 ---
    # 每次运行时都生成一个随机的User-Agent
    current_user_agent = UserAgent().random
    print(f"本次使用的User-Agent: {current_user_agent}")
    # 构建一个通用的请求头，模拟真实浏览器的行为
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "User-Agent": current_user_agent,
    }

    final_content_to_save = None  # 用于存储最终需要保存的页面内容（bytes类型）
    use_selenium_fallback = False  # 标志位，控制是否需要从requests回退到Selenium

    # --- 4. 智能调度核心逻辑 ---
    # 如果全局配置不是“直接使用Selenium”，则执行“requests优先”策略
    if not USE_SELENIUM_DIRECTLY:
        try:
            print("\n--- 模式: 优先使用 Requests ---")
            print(f"正在尝试使用requests访问: {url}")
            # 创建一个Session对象，可以保持cookies等状态
            session = requests.Session()
            session.headers.update(headers)
            # 发起GET请求，设置超时和代理
            response = session.get(url, timeout=10, proxies=requests_proxies)
            # 如果HTTP状态码不是2xx，则抛出异常
            response.raise_for_status()

            # 请求成功后，向用户展示结果大小，并由用户决定下一步操作
            content_length_kb = len(response.content) / 1024
            print(f"Requests成功获取页面！内容大小: {content_length_kb:.2f} KB。")

            while True:
                choice = input("是否接受此内容？(y/n, y=保存, n=尝试使用Selenium获取更完整内容): ").lower()
                if choice == 'y':
                    # 用户满意，将requests获取的内容赋给最终保存变量
                    final_content_to_save = response.content
                    break
                elif choice == 'n':
                    # 用户不满意，设置回退标志位，后续将启动Selenium
                    use_selenium_fallback = True
                    break
                else:
                    print("无效输入，请输入 'y' 或 'n'。")

        except requests.exceptions.RequestException as e:
            # 捕获所有requests可能抛出的异常（如连接超时、DNS错误、HTTP错误等）
            print(f"Requests请求失败 ({type(e).__name__})。")
            # 请求失败，自动设置回退标志位
            use_selenium_fallback = True

    # 如果“直接使用Selenium”被启用，或者“requests优先”策略失败/用户选择回退，则执行此代码块
    if USE_SELENIUM_DIRECTLY or use_selenium_fallback:
        if USE_SELENIUM_DIRECTLY:
            print("\n--- 模式: 直接使用 Selenium ---")
        else:
            print("\n--- 启动回退策略: 调用Selenium进行攻坚 ---")
        # 调用强大的Selenium抓取函数
        final_content_to_save = fetch_page_with_selenium(url, current_user_agent, PROXY_ADDRESS)

    # --- 5. 结果处理与保存 ---
    # 检查final_content_to_save是否有效（即不为None）
    if final_content_to_save:
        # 确保保存目录存在，如果不存在则创建它。exist_ok=True表示目录已存在时不会报错
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        # 以二进制写模式("wb")打开文件，因为我们的内容是bytes类型
        with open(file_path, "wb") as f:
            f.write(final_content_to_save)
        print(f"\n恭喜大侠! 文件已成功下载, 位置: {file_path}")
    else:
        # 如果所有策略都失败了，final_content_to_save将是None
        print("\n任务失败：所有策略均未能成功获取页面内容。")

    # 正常退出程序
    sys.exit(0)

# ----------------------------------- 主程序入口 ------------------------------------------ #
# 这是一个Python脚本的标准入口点。
# 当这个文件被直接运行时，__name__的值是"__main__"，于是main()函数会被调用。
# 如果这个文件被其他脚本作为模块导入，__name__的值将是模块名，if条件不成立，main()不会被执行。
if __name__ == "__main__":
    main()