
# -----------------------------------爬虫实践和代码练习,我要把它做成一个强大的爬虫!------------------------------------------ #
from fake_useragent import UserAgent                                                           # User-Agent池模块,备用
# from urllib.parse import quote,unquote                                                         # 地址编码和解码,备用
import requests
import re
import sys
import os
if __name__ == "__main__":                                                                               # 主程序入口
    pattern = r'^(https?://)?([a-zA-Z0-9.-]+)(:[0-9]+)?(/.*)?$'                                 # 检查网址合法性的正则表达式
    """
    根据计算机中的目录结构来构建以下存储变量,把获取/爬取的内容自动按照文件类型保存在对应目录中
    例如,当获取的是一首歌曲时,只需要修改file_name的值和file_type[0]中的脚标即可
    """
    file_dir = r"E:\Fetch resource"
    file_type = ["Music","Video","Picture","Text","HTML","Other"]
    file_name = "测试.mp4"
    file_path = os.path.join(file_dir,file_type[1],file_name)

    while True:                                                                                                     # 使用while循环,直到用户输入合法的URL
        try:
            url = input("请输入需要爬取的URL:")                                                         # 接收用户输入的URL
            if re.match(pattern,url) is None:                                                              # 如果网址不合法,则抛出异常
                raise ValueError("输入的网址不合法,请检查后重新输入!")                         # 抛出异常,提示用户输入的网址不合法,会跳转到except语句块,try块后面的语句不会执行
            # name = input("请输入搜索参数:")                                                              # 百度搜索带参数调用
            # url = f"https://www.baidu.com/s?wd={name}"
            # headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36" , "Referer" : "https://www.baidu.com/"}
            headers = {"User-Agent" : UserAgent().random , "Referer" : "https://www.baidu.com/"}            # User-Agent池随机生成,防止访问次数过多被拒绝服务;Referer参数声明跳转来自可信站点,也是防止反爬虫必备
            """
            构建请求头,User-Agent参数用于伪装成用户浏览器(部分网站会反爬虫),Referer参数用于伪装重定向前来自于可信地址百度
            UserAgent().random构建了一个随机的User-Agent池,如果向一个服务器发送大量请求,这样做可以避免被系统判定为爬虫
            """
            response = requests.get(url,headers = headers)                                      # 使用requests库发送GET请求,获取网页内容,注意:这里没有检查url的协议头,符合正则规则但没有带协议头的网址,例如www.baidu.com,还需要加上协议头
            # for response_history in response.history:                                              # 用于检测重定向的历史路径,可能需要先禁用request的自动重定向,后续使用
            #     print(f"重定向路径为: {response_history.url}\n")
            # print(f"获取的请求内容为:\n{response.text}")                                          # 打印获取的网页内容,换行只是为了美观,如果网站不是utf-8格式,中文将显示为乱码
            # print(f"获取的请求内容为:\n{response.content.decode()}")                      # 这种方式更优秀,会将content获取的二进制内容转为utf_8格式,中文不会成为乱码
            # print("返回长度为:",len(response.content.decode()))                              # 检查返回的响应长度,用于调试
            # print(f"请求头信息为:{response.request.headers}")                                 # 检查请求头信息,用于调试
            # print(f"本次请求虚拟的User-Agent为:{headers['User-Agent']}")               # 跟踪随机User-Agent池,用于调试
            with open(file_path,"wb") as f:                                                                # 保存爬取的文件
                f.write(response.content)
            print(f"恭喜大侠!文件已成功下载,位置: {file_path}")                                     # 便于观察执行结果,不影响程序逻辑
            break                                                                                                     # 如果获取成功,则跳出while循环,否则会陷入死循环
        except ValueError as e:                                                                               # 捕获异常
            print(f"发生错误: {e}")                                                                              # 打印异常信息,这个except块处理结束后,try...except执行结束,重新进入下一轮while循环
        except Exception as e:                                                                                # 捕获其他异常
            print(f"发生未知错误: {e}")                                                                        # 打印异常信息
            sys.exit(2)                                                                                               # 退出程序,错误码2用来跟踪未知错误
    # os.startfile(full_path_music)                                                                         # 调用os方法运行,调用系统默认播放器,只在播放测试时使用