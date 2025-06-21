import os
import shutil
import time
import random
import sys
import threading
import tkinter as tk
from tkinter import filedialog, scrolledtext

from lxml import html
from fake_useragent import UserAgent
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# --- 1. 爬虫核心逻辑 (已支持动态XPath) ---

def setup_undetected_driver(user_agent_str):
    """
    初始化并配置一个undetected_chromedriver实例。
    """
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument(f"user-agent={user_agent_str}")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    
    try:
        return uc.Chrome(options=chrome_options)
    except Exception as e:
        print(f"初始化 undetected_chromedriver 失败: {e}")
        print("请检查：1. Chrome浏览器是否已安装。 2. 网络连接是否正常。")
        return None

def scrape_logic(base_html_path, output_dir, chapter_xpath, content_xpath, status_callback):
    """
    爬虫核心逻辑函数。
    :param base_html_path: 本地HTML文件路径。
    :param output_dir: 内容输出目录。
    :param chapter_xpath: 提取章节链接的XPath。
    :param content_xpath: 提取章节内容的XPath。
    :param status_callback: 用于更新GUI状态的函数。
    """
    output_file_name = "scraped_chapters.txt" 
    output_file_path = os.path.join(output_dir, output_file_name)
    
    # --- 1. 清空输出文件夹 ---
    print(f"正在清空目录: {output_dir}...")
    shutil.rmtree(output_dir, ignore_errors=True)
    os.makedirs(output_dir)
    print("目录清空并重建完成。")

    # --- 2. 读取本地HTML文件并解析 ---
    print(f"正在读取本地HTML文件: {base_html_path}...")
    try:
        with open(base_html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        tree = html.fromstring(html_content)
        print("本地HTML文件读取并解析成功。")
    except FileNotFoundError:
        print(f"错误：文件未找到，请检查路径是否正确: {base_html_path}")
        status_callback()
        return
    except Exception as e:
        print(f"读取或解析本地HTML文件时发生错误: {e}")
        status_callback()
        return

    # --- 3. 提取章节链接 (使用传入的XPath) ---
    print(f"使用章节链接XPath: {chapter_xpath}")
    chapter_relative_urls = tree.xpath(chapter_xpath)
    total_chapters = len(chapter_relative_urls)

    if not chapter_relative_urls:
        print("未找到任何章节链接，请检查XPath表达式或HTML结构。")
        status_callback()
        return

    print(f"共找到 {total_chapters} 个章节链接。")

    # --- 4. 初始化 undetected_chromedriver ---
    driver = None
    try:
        current_user_agent = UserAgent().random
        print(f"本次使用的User-Agent: {current_user_agent}")
        
        driver = setup_undetected_driver(current_user_agent)
        if not driver:
            status_callback()
            return
        
        print("undetected_chromedriver 初始化成功，浏览器将以无头模式运行。")

        # --- 5. 遍历所有章节链接，获取内容并保存 ---
        print(f"使用章节内容XPath: {content_xpath}")
        for chapter_num, relative_url in enumerate(chapter_relative_urls, 1):
            full_chapter_url = ""
            try:
                full_chapter_url = "https:" + relative_url
                print(f"\n--- [{chapter_num}/{total_chapters}] ---")
                print(f"正在获取内容: {full_chapter_url}")

                driver.get(full_chapter_url)

                # 等待条件也使用传入的XPath
                WebDriverWait(driver, 30).until(
                    EC.visibility_of_element_located((By.XPATH, content_xpath))
                )
                
                chapter_html_content = driver.page_source
                chapter_tree = html.fromstring(chapter_html_content)
                # 提取内容也使用传入的XPath
                content_elements = chapter_tree.xpath(content_xpath)
                
                chapter_content = ""
                if content_elements:
                    chapter_content = "\n".join([elem.text_content().strip() for elem in content_elements])
                    print(f"成功获取第 {chapter_num} 章内容！")
                else:
                    print(f"警告：第 {chapter_num} 章 ({full_chapter_url}) 未找到内容。")

                with open(output_file_path, 'a', encoding='utf-8') as outfile:
                    if chapter_num > 1:
                        outfile.write("\n\n")
                    outfile.write(f"第{chapter_num}章\n")
                    outfile.write(chapter_content)
                
                sleep_time = random.uniform(1, 3)
                print(f"爬取成功，随机等待 {sleep_time:.2f} 秒...")
                time.sleep(sleep_time)

            except TimeoutException:
                print(f"错误：获取第 {chapter_num} 章 ({full_chapter_url}) 时超时，请检查内容XPath是否正确或网络状况。")
            except Exception as e:
                print(f"处理第 {chapter_num} 章 ({full_chapter_url}) 时发生未知错误: {e}，跳过此章。")

    except Exception as e:
        print(f"发生严重错误，程序终止: {e}")
    finally:
        if driver:
            try:
                driver.quit()
                print("\n浏览器已关闭。")
            except OSError as e:
                print(f"\n关闭浏览器时发生预期内的错误，已忽略: {e}")

    print(f"\n全部任务完成，内容已保存到: {output_file_path}")
    status_callback()

# --- 2. GUI界面实现 (已增加XPath配置) ---

class TextRedirector:
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str_):
        self.widget.after(0, self._write, str_)

    def _write(self, str_):
        self.widget.configure(state='normal')
        self.widget.insert('end', str_, (self.tag,))
        self.widget.see('end')
        self.widget.configure(state='disabled')

    def flush(self):
        pass

class ScraperGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("章节内容下载器")
        self.geometry("800x650") # 稍微调高一点窗口

        # --- 默认配置 ---
        self.base_html_path = tk.StringVar(value=r"D:\Fetch resource\HTML\测试.html")
        self.output_dir = tk.StringVar(value=r"D:\Fetch resource\Other")
        # 新增：XPath的默认值
        self.chapter_xpath = tk.StringVar(value='//li[@class = "chapter-item"]/a/@href')
        self.content_xpath = tk.StringVar(value='//span[@class = "content-text"]')

        self.create_widgets()

        self.log_widget = self.log_text
        sys.stdout = TextRedirector(self.log_widget, "stdout")
        sys.stderr = TextRedirector(self.log_widget, "stderr")

    def create_widgets(self):
        main_frame = tk.Frame(self, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- 路径设置部分 ---
        path_frame = tk.LabelFrame(main_frame, text="路径设置", padx=10, pady=10)
        path_frame.pack(fill=tk.X, pady=(0, 10))
        path_frame.grid_columnconfigure(1, weight=1)

        tk.Label(path_frame, text="HTML文件:").grid(row=0, column=0, sticky=tk.W, pady=5)
        tk.Entry(path_frame, textvariable=self.base_html_path).grid(row=0, column=1, sticky=tk.EW, padx=5)
        tk.Button(path_frame, text="浏览...", command=self.select_html_file).grid(row=0, column=2)

        tk.Label(path_frame, text="输出目录:").grid(row=1, column=0, sticky=tk.W, pady=5)
        tk.Entry(path_frame, textvariable=self.output_dir).grid(row=1, column=1, sticky=tk.EW, padx=5)
        tk.Button(path_frame, text="浏览...", command=self.select_output_dir).grid(row=1, column=2)

        # --- 新增：XPath设置部分 ---
        xpath_frame = tk.LabelFrame(main_frame, text="解析规则 (XPath)", padx=10, pady=10)
        xpath_frame.pack(fill=tk.X, pady=(0, 10))
        xpath_frame.grid_columnconfigure(1, weight=1)

        tk.Label(xpath_frame, text="章节链接XPath:").grid(row=0, column=0, sticky=tk.W, pady=5)
        tk.Entry(xpath_frame, textvariable=self.chapter_xpath).grid(row=0, column=1, sticky=tk.EW, padx=5)

        tk.Label(xpath_frame, text="章节内容XPath:").grid(row=1, column=0, sticky=tk.W, pady=5)
        tk.Entry(xpath_frame, textvariable=self.content_xpath).grid(row=1, column=1, sticky=tk.EW, padx=5)

        # --- 日志输出部分 ---
        log_frame = tk.LabelFrame(main_frame, text="进度日志", padx=10, pady=10)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, state='disabled')
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.tag_config("stderr", foreground="red")

        # --- 控制按钮 ---
        self.start_button = tk.Button(main_frame, text="开始爬取", command=self.start_scraping_thread, font=("", 12, "bold"), bg="lightblue")
        self.start_button.pack(fill=tk.X, pady=(10, 0))

    def select_html_file(self):
        path = filedialog.askopenfilename(title="选择HTML文件", filetypes=[("HTML files", "*.html"), ("All files", "*.*")])
        if path: self.base_html_path.set(path)

    def select_output_dir(self):
        path = filedialog.askdirectory(title="选择输出文件夹")
        if path: self.output_dir.set(path)

    def start_scraping_thread(self):
        self.start_button.config(state=tk.DISABLED, text="正在爬取...")
        
        self.log_text.configure(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state='disabled')

        # 将GUI中的XPath值传递给爬虫线程
        scraper_thread = threading.Thread(
            target=scrape_logic,
            args=(
                self.base_html_path.get(), 
                self.output_dir.get(),
                self.chapter_xpath.get(),
                self.content_xpath.get(),
                self.on_scraping_complete
            )
        )
        scraper_thread.daemon = True
        scraper_thread.start()

    def on_scraping_complete(self):
        self.start_button.config(state=tk.NORMAL, text="开始爬取")

# --- 3. 运行程序 ---
if __name__ == "__main__":
    app = ScraperGUI()
    app.mainloop()