
# -----------------------------------爬虫实践和代码练习,我要把它做成一个强大的爬虫!------------------------------------------ #
# from fake_useragent import UserAgent                                                         # User-Agent池模块,备用
# from urllib.parse import quote,unquote                                                         # 地址编码和解码,备用
import requests
# import re
import sys
import os
if __name__ == "__main__":                                                                               # 主程序入口
    pattern = r'^(https?://)?([a-zA-Z0-9.-]+)(:[0-9]+)?(/.*)?$'                                 # 检查网址合法性的正则表达式
    file_path_music = r"E:\Fetch resource\Music"
    music_name = "我的微笑.mp3"
    file_path_video = r"E:\Fetch resource\Video"
    video_name = ""
    file_path_picture = r"E:\Fetch resource\Picture"
    picture_name = "测试图片.jpg"
    file_path_text = r"E:\Fetch resource\Text"
    text_name = ""
    file_path_html = r"E:\Fetch resource\HTML"
    html_name = ""
    file_path_other = r"E:\Fetch resource\Other"
    other_name = ""
    full_path_music = os.path.join(file_path_music,music_name)
    full_path_video = os.path.join(file_path_video,video_name)
    full_path_picture = os.path.join(file_path_picture,picture_name)
    full_path_text = os.path.join(file_path_text,text_name)
    full_path_html = os.path.join(file_path_html,html_name)
    full_path_other = os.path.join(file_path_other,other_name)
    while True:                                                                                                     # 使用while循环,直到用户输入合法的URL
        try:
            # url = input("请输入需要爬取的URL:")                                                         # 接收用户输入的URL
            # if re.match(pattern,url) is None:                                                              # 如果网址不合法,则抛出异常
            #     raise ValueError("输入的网址不合法,请检查后重新输入!")                         # 抛出异常,提示用户输入的网址不合法,会跳转到except语句块,try块后面的语句不会执行
            name = input("请输入搜索参数:")
            url = f"https://www.google.com/search?q={name}"
            headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36" , "Referer" : "https://www.google.com/"}
            # headers = {"User-Agent" : UserAgent().random , "Referer" : "https://www.google.com/"}
            """
            构建请求头,User-Agent参数用于伪装成用户浏览器(部分网站会反爬虫),Referer参数用于伪装重定向前来自于可信地址百度
            UserAgent().random构建了一个随机的User-Agent池,如果向一个服务器发送大量请求,这样做可以避免被系统判定为爬虫
            """
            response = requests.get(url,headers = headers)                                      # 使用requests库发送GET请求,获取网页内容,注意:这里没有检查url的协议头,符合正则规则但没有带协议头的网址,例如www.baidu.com,还需要加上协议头
            # for response_history in response.history:                                              # 用于检测重定向的历史路径,可能需要先禁用request的自动重定向,暂时不用
            #     print(f"重定向路径为: {response_history.url}\n")
            # print(f"获取的请求内容为:\n{response.text}")                                          # 打印获取的网页内容,换行只是为了美观,如果网站不是utf-8格式,中文将显示为乱码
            print(f"获取的请求内容为:\n{response.content.decode()}")                      # 这种方式更优秀,会将content获取的二进制内容转为utf_8格式,中文不会成为乱码
            # print("返回长度为:",len(response.content.decode()))                              # 检查返回的响应长度,用于调试
            # print(f"请求头信息为:{response.request.headers}")                                 # 检查请求头信息,用于调试
            # print(f"本次请求虚拟的User-Agent为:{UserAgent().random}")                  # 跟踪随机User-Agent池,用于调试
            # with open(full_path_picture,"wb") as f:                                                    # 保存爬取的媒体文件,根据文件类型,使用不同的参数
            #     f.write(response.content)
            # print(f"恭喜大侠!文件已成功下载,位置: {full_path_picture}")
            break                                                                                                     # 如果获取成功,则跳出while循环,否则会陷入死循环
        except ValueError as e:                                                                               # 捕获异常
            print(f"发生错误: {e}")                                                                              # 打印异常信息,这个except块处理结束后,try...except执行结束,重新
        except Exception as e:                                                                                # 捕获其他异常
            print(f"发生未知错误: {e}")                                                                        # 打印异常信息
            sys.exit(2)                                                                                               # 退出程序,错误码为2用来跟踪未知错误
    # os.startfile(full_path_music)                                                                         # 调用os方法运行,调用系统默认播放器,只在播放测试时使用