import tkinter
import webbrowser

class VipForFree:
    def __init__(self, root):
        """
        初始化VipForFree应用程序。
        设置主窗口的标题、大小，并创建UI组件。
        """
        self.root = root
        self.root.title("追剧神器")
        self.root.geometry("480x200")
        # 调用方法创建所有UI组件
        self.create_widgets()
        # 修正：控制窗口是否可调整大小。
        # False, False 表示宽度和高度都不可调整，使窗口大小固定。
        # 如果希望可以调整，可以设置为 True, True 或根据需要设置。
        self.root.resizable(False, False)

    def create_widgets(self):
        """
        创建并布局应用程序的所有UI组件。
        """
        # 电影链接输入框的标签
        label_movie_link = tkinter.Label(self.root, text="输入电影链接:")
        label_movie_link.place(x=20, y=30, width=100, height=30)

        # 电影链接输入框
        self.entry_movie_link = tkinter.Entry(self.root)
        self.entry_movie_link.place(x=125, y=30, width=260, height=30)

        # 清空按钮，绑定到self.empty方法
        button_movie_link = tkinter.Button(self.root, text="清空", command=self.empty)
        button_movie_link.place(x=400, y=30, width=50, height=30)

        # 爱奇艺按钮，绑定到self.open_iqy方法
        button_movie1 = tkinter.Button(self.root, text="爱奇艺", command=self.open_iqy)
        button_movie1.place(x=25, y=80, width=80, height=40)

        # 腾讯视频按钮，绑定到self.open_tx方法
        button_movie2 = tkinter.Button(self.root, text="腾讯视频", command=self.open_tx)
        button_movie2.place(x=125, y=80, width=80, height=40)

        # 优酷按钮，绑定到self.open_yq方法
        button_movie3 = tkinter.Button(self.root, text="优酷", command=self.open_yq)
        button_movie3.place(x=225, y=80, width=80, height=40)

        # 播放VIP视频按钮，绑定到self.play_video方法
        button_movie = tkinter.Button(self.root, text="播放VIP视频", command=self.play_video)
        button_movie.place(x=325, y=80, width=125, height=40)

        # 友情提示文本
        text = "友情提示:该软件仅供学习交流使用,请遵守相关法律法规,尊重版权."
        lab_remind = tkinter.Label(self.root, text=text, fg="red", justify="left", font=("Arial", 10))
        lab_remind.place(x=50, y=150, width=400, height=30)

    # 以下是修正后的方法定义，它们现在是VipForFree类的成员方法，
    # 与__init__和create_widgets处于同一缩进级别。

    def open_iqy(self):
        """
        打开爱奇艺官网。
        """
        url = "https://www.iqiyi.com/"
        webbrowser.open(url)

    def open_tx(self):
        """
        打开腾讯视频官网。
        """
        url = "https://v.qq.com/"
        webbrowser.open(url)

    def open_yq(self):
        """
        打开优酷官网。
        """
        url = "https://www.youku.com/"
        webbrowser.open(url)

    def play_video(self):
        """
        获取输入框中的视频链接，并通过第三方解析网站播放。
        """
        video_url = self.entry_movie_link.get()
        if video_url: # 检查输入框是否为空
            # 这是一个示例解析接口，当前用的解析接口为虾米解析
            webbrowser.open('https://jx.xmflv.cc/?url=' + video_url)
        else:
            # 如果输入框为空，可以给用户一个提示
            print("请输入电影链接！") # 在控制台打印，实际应用中可使用tkinter.messagebox

    def empty(self):
        """
        清空电影链接输入框的内容。
        """
        self.entry_movie_link.delete(0, tkinter.END)

if __name__ == "__main__":
    # 创建Tkinter主窗口
    root = tkinter.Tk()
    # 实例化VipForFree应用程序
    app = VipForFree(root)
    # 启动Tkinter事件循环
    root.mainloop()