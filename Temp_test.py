# --------------------------用面向对象的方式实现一个简单的贴吧爬虫--------------------------
import requests                                                                                                               # 导入requests库
class Fetch_Tieba:
    def __init__(self):
        self.url = 'https://tieba.baidu.com/f?'                                                                    # 这是网址的基础格式
        self.search_kw = input("请输入你要获取的贴吧名字:")                                            # 这是贴吧的具体名字
        self.pages = 3                                                                                                           # 这想要爬取的页数,代表想要在这个吧中爬取几页
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
    def send(self,params):                                                                                                 # 定义一个方法来发送请求
        response = requests.get(self.url, params=params, headers=self.headers)       # 发送GET请求
        return response.text                                                                                                # 返回响应内容
    def save(self,page,con):                                                                                               # 定义一个方法来保存内容
        with open(f"{self.search_kw}_page_{page+1}.html", 'w', encoding='utf-8') as f:  # 打开文件以写入
            f.write(con)                                                                                                            # 写入内容
    def run(self):                                                                                                                  # 定义一个方法来运行爬虫
        for i in range(self.pages):                                                                                         # 循环遍历每一页
            pn = i * 50                                                                                                              # 计算偏移量
            params = {'kw': self.search_kw, 'ie': 'utf-8', 'pn': pn}                                          # 构建参数字典
            data = self.send(params)                                                                                     # 发送请求并获取响应内容
            self.save(i, data)                                                                                                    # 保存内容到文件

if __name__ == "__main__":                                                                                               # 如果这个脚本是主程序
    fetcher = Fetch_Tieba()                                                                                                 # 创建Fetch_Tieba类的实例
    fetcher.run()                                                                                                                   # 运行爬虫