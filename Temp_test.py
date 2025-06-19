# ================================================================================== #
#                                                                                                                                                                                                                                 #
#                      一个强大的、智能的、通用的动态网页爬虫框架          由天上人间一号妹妹倾情打造!版权所有!                                                       #
#                                                                                                                                                                                                                                 #
#                                                                                                                                                                                                                                 #
# ================================================================================== #

# ----------------------------------- 基础与核心库导入 ------------------------------------------ #
import os
import random
import re
import sys
import time
from urllib.parse import urlparse
import requests

# ----------------------------------- 强大的Selenium与相关模块导入 ------------------------------------------ #
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from fake_useragent import UserAgent
from webdriver_manager.chrome import ChromeDriverManager


# ================================================================================== #
#                                                                                                                                                                                                                                 #
#                                                                      --- 全局配置中心 (可在此处修改所有手动设置) ---                                                                            #
#                                                                                                                                                                                                                                 #
# ================================================================================== #

# --- 1. 文件与路径配置 ---
# 爬取文件保存的基础目录
SAVE_DIR_BASE = r"D:\Fetch resource"
# 文件分类子目录 (程序将使用 'HTML' 这一项)
SAVE_SUB_DIRS = ["Music", "Video", "Picture", "Text", "HTML", "Other"]
# 默认保存的文件名
DEFAULT_FILENAME = "京东.html"

# --- 2. 代理配置 ---
# 如果不需要代理，请将下面的值设为 None
# 示例: PROXY_ADDRESS = None
PROXY_ADDRESS = "http://127.0.0.1:10090"  # 请替换为你的有效代理地址

# --- 3. 核心策略与行为配置 ---
# 是否直接使用Selenium模式 (True/False)
#   - True:  跳过requests，直接使用强大的Selenium模式，适合已知需要动态渲染的复杂网站。
#   - False: 优先使用轻量级的requests，失败后自动回退到Selenium模式，效率更高。
USE_SELENIUM_DIRECTLY = False

# Selenium是否以无头模式运行 (True/False)
#   - True:  在后台运行，不显示浏览器界面，适合自动化执行。
#   - False: 显示浏览器界面，便于观察爬虫的每一步操作，强烈建议在调试新网站时使用。
RUN_HEADLESS = False

# Selenium等待关键元素的超时时间（秒）
#   - 如果网络较慢或目标网站加载时间长，可以适当增加此值。
SELENIUM_WAIT_TIMEOUT = 20

# 模拟滚动页面时，每次滚动后等待加载的时间（秒）
#   - 这是一个随机范围，程序会在此范围内取一个随机值，让行为更不可预测。
SCROLL_WAIT_TIME_RANGE = (1.5, 2.5)


# ================================================================================== #
#                                                                                                                                                                                                                                 #
#                                                                                   --- 核心功能函数 (请勿轻易修改) ---                                                                                    #
#                                                                                                                                                                                                                                 #
# ================================================================================== #

def setup_undetected_driver(user_agent_str, proxy_address=None):
    """
    初始化并返回一个配置了强大反检测能力的 undetected-chromedriver 实例。
    它会使用全局配置中的 RUN_HEADLESS 设置。
    """
    chrome_options = uc.ChromeOptions()
    if RUN_HEADLESS:
        chrome_options.add_argument("--headless=new")
    chrome_options.add_argument(f"user-agent={user_agent_str}")
    chrome_options.add_argument("--window-size=1920,1080")
    if proxy_address:
        chrome_options.add_argument(f'--proxy-server={proxy_address}')
    try:
        driver_path = ChromeDriverManager().install()
        return uc.Chrome(driver_executable_path=driver_path, options=chrome_options)
    except Exception as e:
        print(f"初始化undetected-chromedriver失败: {e}")
        return None


def generate_site_config(driver, url):
    """
    核心智能模块：通过启发式策略智能分析页面，动态生成用于等待的配置。
    """
    print("\n--- 进入智能分析模式 ---")
    try:
        driver.get(url)
        time.sleep(5)
        print("正在智能分析页面结构，寻找关键内容区域...")

        KEYWORDS = ['main', 'content', 'container', 'list', 'article', 'search', 'app', 'footer']
        SEMANTIC_TAGS = ['main', 'footer', 'article', 'aside']
        found_locators = []

        for tag in SEMANTIC_TAGS:
            if driver.find_elements(By.TAG_NAME, tag):
                print(f"  [启发式命中] 发现语义化标签: <{tag}>")
                found_locators.append((By.TAG_NAME, tag))

        for keyword in KEYWORDS:
            selectors = [f'[id*="{keyword}"]', f'[class*="{keyword}"]']
            for selector in selectors:
                if driver.find_elements(By.CSS_SELECTOR, selector):
                    print(f"  [启发式命中] 发现含关键词 '{keyword}' 的元素 (选择器: {selector})")
                    found_locators.append((By.CSS_SELECTOR, selector))

        if not found_locators:
            print("智能分析失败：未能根据启发式规则找到任何可用于等待的关键元素。")
            return None

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
    Selenium攻坚总指挥：整合了智能分析、智能等待和惰性加载处理。
    """
    # 使用 with 语句优雅地管理 driver 的生命周期，自动确保浏览器被关闭
    try:
        with setup_undetected_driver(user_agent_str, proxy_address) as driver:
            if driver is None:
                return None

            # --- 步骤1: 智能分析与配置生成 ---
            site_config = generate_site_config(driver, url)
            if not site_config:
                return None

            # --- 步骤2: 正式访问与智能等待 ---
            print(f"\n--- 开始正式爬取 ---")
            print(f"正在访问: {url}, 请稍候......")
            driver.get(url)

            print(f"页面初步加载，现在开始等待关键动态内容（最长{SELENIUM_WAIT_TIMEOUT}秒）...")
            wait_conditions = [EC.presence_of_element_located(loc) for loc in site_config["wait_locators"]]
            WebDriverWait(driver, SELENIUM_WAIT_TIMEOUT).until(EC.any_of(*wait_conditions))
            print("关键动态内容已加载！")

            # --- 步骤3: 处理惰性加载 (Lazy Loading) ---
            print("正在模拟滚动页面，以触发所有惰性加载内容...")
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.uniform(SCROLL_WAIT_TIME_RANGE[0], SCROLL_WAIT_TIME_RANGE[1]))
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            print("已滚动至页面底部。")

            # --- 步骤4: 获取最终页面源码 ---
            final_html_content = driver.page_source
            print("Selenium成功获取渲染后的完整页面！")
            return final_html_content.encode('utf-8')

    except Exception as e:
        print(f"在Selenium主流程中发生错误: {e}")
        return None


# ----------------------------------- 主函数逻辑 ------------------------------------------ #
def main():
    """
    程序的主执行函数，负责调度requests和Selenium。
    """
    # --- 1. 初始化路径和代理 ---
    # 根据全局配置构建完整的文件保存路径
    file_path = os.path.join(SAVE_DIR_BASE, SAVE_SUB_DIRS[4], DEFAULT_FILENAME)
    # 为requests构建代理字典
    requests_proxies = {"http": PROXY_ADDRESS, "https": PROXY_ADDRESS} if PROXY_ADDRESS else None

    # --- 2. 用户交互 ---
    url = input("请输入需要爬取的URL: ")
    if not re.match(r'^(https?://)', url):
        url = 'https://' + url

    # --- 3. 构建通用请求头 ---
    current_user_agent = UserAgent().random
    print(f"本次使用的User-Agent: {current_user_agent}")
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "User-Agent": current_user_agent,
    }

    final_content_to_save = None

    # --- 4. 智能调度核心逻辑 ---
    if not USE_SELENIUM_DIRECTLY:
        # 策略1: 优先尝试轻量级的 requests
        try:
            print("\n--- 模式: 优先使用 Requests ---")
            print(f"正在尝试使用requests访问: {url}")
            session = requests.Session()
            session.headers.update(headers)
            response = session.get(url, timeout=10, proxies=requests_proxies)
            response.raise_for_status()
            final_content_to_save = response.content
            print("Requests成功获取页面！任务高效完成。")
        except requests.exceptions.RequestException as e:
            print(f"Requests请求失败 ({type(e).__name__})。")
            print("--- 启动回退策略: 调用Selenium进行攻坚 ---")
            final_content_to_save = fetch_page_with_selenium(url, current_user_agent, PROXY_ADDRESS)
    else:
        # 策略2: 根据配置，直接使用Selenium
        print("\n--- 模式: 直接使用 Selenium ---")
        final_content_to_save = fetch_page_with_selenium(url, current_user_agent, PROXY_ADDRESS)

    # --- 5. 结果处理与保存 ---
    if final_content_to_save:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(final_content_to_save)
        print(f"\n恭喜大侠! 文件已成功下载, 位置: {file_path}")
    else:
        print("\n任务失败：所有策略均未能成功获取页面内容。")

    sys.exit(0)

# ----------------------------------- 主程序入口 ------------------------------------------ #
if __name__ == "__main__":
    main()