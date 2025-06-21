# main_gui.py

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os

# 从我们的模块中导入解析函数
import html_parser


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("HTML 内容提取器 (v1.0)")
        self.root.geometry("600x400")  # 设置窗口大小

        # --- 数据存储变量 ---
        # 使用Tkinter的StringVar来动态更新界面上的文本
        self.source_file_path = tk.StringVar()
        self.output_dir_path = tk.StringVar()
        self.tags_to_extract = tk.StringVar()

        # --- 创建界面组件 ---
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill="both", expand=True)

        # 1. 源文件选择
        source_frame = ttk.LabelFrame(main_frame, text="1. 选择源HTML文件", padding="10")
        source_frame.pack(fill="x", pady=5)

        source_entry = ttk.Entry(source_frame, textvariable=self.source_file_path, state="readonly")
        source_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

        source_button = ttk.Button(source_frame, text="浏览...", command=self.select_source_file)
        source_button.pack(side="left")

        # 2. 输出目录选择
        output_frame = ttk.LabelFrame(main_frame, text="2. 设置输出位置", padding="10")
        output_frame.pack(fill="x", pady=5)

        output_entry = ttk.Entry(output_frame, textvariable=self.output_dir_path, state="readonly")
        output_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

        output_button = ttk.Button(output_frame, text="浏览...", command=self.select_output_dir)
        output_button.pack(side="left")

        # 3. 提取标签设置
        tags_frame = ttk.LabelFrame(main_frame, text="3. 设置提取标签 (可选)", padding="10")
        tags_frame.pack(fill="x", pady=5)

        tags_label = ttk.Label(tags_frame, text="输入标签名,用逗号分隔 (如: p,h1,div)。留空则提取所有。")
        tags_label.pack(anchor="w")

        tags_entry = ttk.Entry(tags_frame, textvariable=self.tags_to_extract)
        tags_entry.pack(fill="x", pady=(5, 0))

        # 4. 操作按钮
        action_frame = ttk.Frame(main_frame, padding="10")
        action_frame.pack(fill="x", pady=20)

        text_button = ttk.Button(action_frame, text="提取文本", command=self.run_text_extraction)
        text_button.pack(side="left", fill="x", expand=True, padx=5)

        image_button = ttk.Button(action_frame, text="提取图片", command=self.run_image_extraction)
        image_button.pack(side="left", fill="x", expand=True, padx=5)

        # 5. 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("准备就绪...")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor="w", padding=5)
        status_bar.pack(side="bottom", fill="x")

    def select_source_file(self):
        # 打开文件选择对话框，只允许选择html和htm文件
        filepath = filedialog.askopenfilename(
            title="选择HTML文件",
            filetypes=[("HTML 文件", "*.html;*.htm"), ("所有文件", "*.*")]
        )
        if filepath:
            self.source_file_path.set(filepath)
            self.status_var.set(f"已选择源文件: {os.path.basename(filepath)}")

    def select_output_dir(self):
        # 打开目录选择对话框
        dirpath = filedialog.askdirectory(title="选择保存位置")
        if dirpath:
            self.output_dir_path.set(dirpath)
            self.status_var.set(f"已设置输出目录: {dirpath}")

    def run_text_extraction(self):
        source = self.source_file_path.get()
        output_dir = self.output_dir_path.get()

        # 输入验证
        if not source or not output_dir:
            messagebox.showerror("错误", "请先选择源文件和输出位置！")
            return

        self.status_var.set("正在提取文本...")
        self.root.update_idletasks()  # 强制刷新界面，显示新状态

        # 处理标签输入
        tags_str = self.tags_to_extract.get()
        # 列表推导式：高效处理字符串，分割并去除空白，过滤掉空标签
        target_tags = [tag.strip() for tag in tags_str.split(',') if tag.strip()]

        # 构造输出文件名
        output_filename = os.path.basename(source) + "_text.txt"
        output_txt_path = os.path.join(output_dir, output_filename)

        # 调用后端模块的函数
        result = html_parser.extract_text_from_file(source, output_txt_path, target_tags)

        messagebox.showinfo("操作完成", result)
        self.status_var.set("文本提取完成。")

    def run_image_extraction(self):
        source = self.source_file_path.get()
        output_dir = self.output_dir_path.get()

        if not source or not output_dir:
            messagebox.showerror("错误", "请先选择源文件和输出位置！")
            return

        # 为图片创建一个专门的子目录，避免混乱
        image_output_subdir = os.path.join(output_dir, os.path.basename(source) + "_images")

        self.status_var.set("正在提取图片...")
        self.root.update_idletasks()

        # 调用后端模块的函数
        result = html_parser.extract_images_from_file(source, image_output_subdir)

        messagebox.showinfo("操作完成", result)
        self.status_var.set("图片提取完成。")


if __name__ == "__main__":
    # --- 程序主入口 ---
    # 这段代码是Tkinter程序的标准启动方式
    # 就像C/C++程序的 main() 函数
    root = tk.Tk()
    app = App(root)
    # root.mainloop() 会启动事件循环，等待用户操作（点击按钮等）
    # 程序会一直在这里运行，直到用户关闭窗口
    root.mainloop()

