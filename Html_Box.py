# main_gui.py (最终版 v3.0)

import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import os
import shutil
import html_parser  # 确保导入我们刚刚创建的配套模块


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("HTML 内容提取器 (v3.0 - 终极版)")
        self.root.geometry("1024x768")

        # ... (这部分代码与之前相同，直接复制即可) ...
        self.source_file_path = tk.StringVar()
        self.output_dir_path = tk.StringVar()
        self.tags_to_extract = tk.StringVar()
        self.status_var = tk.StringVar()
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill="both", expand=True)
        source_frame = ttk.LabelFrame(main_frame, text="1. 选择源HTML文件", padding="10")
        source_frame.pack(fill="x", pady=5)
        source_entry = ttk.Entry(source_frame, textvariable=self.source_file_path, state="readonly")
        source_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        source_button = ttk.Button(source_frame, text="浏览...", command=self.select_source_file)
        source_button.pack(side="left")
        output_frame = ttk.LabelFrame(main_frame, text="2. 设置输出位置", padding="10")
        output_frame.pack(fill="x", pady=5)
        output_entry = ttk.Entry(output_frame, textvariable=self.output_dir_path, state="readonly")
        output_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        output_button = ttk.Button(output_frame, text="浏览...", command=self.select_output_dir)
        output_button.pack(side="left")
        tags_frame = ttk.LabelFrame(main_frame, text="3. 设置提取标签 (可选)", padding="10")
        tags_frame.pack(fill="x", pady=5)
        tags_label = ttk.Label(tags_frame, text="输入标签名,用逗号分隔 (如: p,h1,div)。留空则提取所有。")
        tags_label.pack(anchor="w")
        tags_entry = ttk.Entry(tags_frame, textvariable=self.tags_to_extract)
        tags_entry.pack(fill="x", pady=(5, 0))
        action_frame = ttk.Frame(main_frame, padding="10")
        action_frame.pack(fill="x", pady=10)
        self.text_button = ttk.Button(action_frame, text="提取文本", command=self.run_text_extraction)
        self.text_button.pack(side="left", fill="x", expand=True, padx=5)
        self.image_button = ttk.Button(action_frame, text="提取图片", command=self.run_image_extraction)
        self.image_button.pack(side="left", fill="x", expand=True, padx=5)
        progress_frame = ttk.LabelFrame(main_frame, text="实时进度", padding="10")
        progress_frame.pack(fill="both", expand=True, pady=5)
        self.progress_text = scrolledtext.ScrolledText(progress_frame, height=10, wrap=tk.WORD, state="disabled",
                                                       bg="#f0f0f0")
        self.progress_text.pack(fill="both", expand=True)
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief="sunken", anchor="w", padding=5)
        status_bar.pack(side="bottom", fill="x")

        # 设置默认值
        default_source = r"E:\Fetch resource\Html\测试.html"
        default_output = r"E:/Fetch resource/Other"
        self.source_file_path.set(default_source)
        self.output_dir_path.set(default_output)

        if os.path.exists(default_source):
            self.status_var.set(f"已加载默认配置。源文件: {os.path.basename(default_source)}")
        else:
            self.status_var.set(f"警告: 默认源文件不存在: {default_source}")

    def _log_progress(self, message):
        self.progress_text.config(state="normal")
        self.progress_text.insert(tk.END, message + "\n")
        self.progress_text.see(tk.END)
        self.progress_text.config(state="disabled")
        self.root.update_idletasks()

    def _toggle_buttons(self, enabled):
        state = "normal" if enabled else "disabled"
        self.text_button.config(state=state)
        self.image_button.config(state=state)

    def run_image_extraction(self):
        source = self.source_file_path.get()
        output_dir = self.output_dir_path.get()
        if not source or not output_dir:
            messagebox.showerror("错误", "请先选择源文件和输出位置！")
            return
        if not self.clear_directory(output_dir):
            return
        self._toggle_buttons(enabled=False)
        self.progress_text.config(state="normal")
        self.progress_text.delete('1.0', tk.END)
        self.progress_text.config(state="disabled")

        # 这一句现在一定能找到正确的函数了！
        image_generator = html_parser.extract_images_generator(source, output_dir)

        self.root.after(100, self._process_generator, image_generator)

    def _process_generator(self, generator):
        try:
            message = next(generator)
            self._log_progress(message)
            self.root.after(10, self._process_generator, generator)
        except StopIteration:
            self._log_progress("...所有任务已处理完毕...")
            self._toggle_buttons(enabled=True)
            messagebox.showinfo("操作完成", "图片提取流程已结束！")
        except Exception as e:
            self._log_progress(f"发生严重错误: {e}")
            self._toggle_buttons(enabled=True)
            messagebox.showerror("严重错误", f"处理过程中发生意外错误: {e}")

    # ... (其他辅助函数保持不变) ...
    def select_source_file(self):
        filepath = filedialog.askopenfilename(title="选择HTML文件",
                                              filetypes=[("HTML 文件", "*.html;*.htm"), ("所有文件", "*.*")])
        if filepath: self.source_file_path.set(filepath); self.status_var.set(
            f"已选择源文件: {os.path.basename(filepath)}")

    def select_output_dir(self):
        dirpath = filedialog.askdirectory(title="选择保存位置")
        if dirpath: self.output_dir_path.set(dirpath); self.status_var.set(f"已设置输出目录: {dirpath}")

    def clear_directory(self, dir_path):
        if not os.path.isdir(dir_path): return True
        if not messagebox.askyesno("确认操作", f"您确定要清空目录 '{dir_path}' 下的所有内容吗？\n此操作不可恢复！",
                                   icon='warning'):
            self.status_var.set("操作已取消.")
            return False
        self.status_var.set(f"正在清空目录: {dir_path}...")
        self.root.update_idletasks()
        try:
            for item_name in os.listdir(dir_path):
                item_path = os.path.join(dir_path, item_name)
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
            return True
        except Exception as e:
            messagebox.showerror("错误", f"清空目录时发生错误: {e}")
            self.status_var.set("清空目录失败.")
            return False

    def run_text_extraction(self):
        source, output_dir = self.source_file_path.get(), self.output_dir_path.get()
        if not source or not output_dir: messagebox.showerror("错误", "请先选择源文件和输出位置！"); return
        if not self.clear_directory(output_dir): return
        self.status_var.set("正在提取文本...")
        self.root.update_idletasks()
        tags_str = self.tags_to_extract.get()
        target_tags = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
        output_filename = os.path.basename(source) + "_text.txt"
        output_txt_path = os.path.join(output_dir, output_filename)
        result = html_parser.extract_text_from_file(source, output_txt_path, target_tags)
        messagebox.showinfo("操作完成", result)
        self.status_var.set("文本提取完成。")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
