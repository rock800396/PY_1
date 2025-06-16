
# -----------------------------------爬虫实践和代码练习,我要把它做成一个强大的爬虫!------------------------------------------ #

import requests
import re
import sys
import os
if __name__ == "__main__":                                                                               # 主程序入口
    pattern = r'^(https?://)?([a-zA-Z0-9.-]+)(:[0-9]+)?(/.*)?$'                                 # 检查网址合法性的正则表达式,全局变量
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
            url = input("请输入需要爬取的URL:")                                                         # 接收用户输入的URL
            if re.match(pattern,url) is None:                                                              # 如果网址不合法,则抛出异常
                raise ValueError("输入的网址不合法,请检查后重新输入!")                         # 抛出异常,提示用户输入的网址不合法,会跳转到except语句块,try块后面的语句不会执行
            response = requests.get(url)                                                                   # 使用requests库发送GET请求,获取网页内容,注意:这里没有检查协议头,符合正则规则但没有带协议头的网址,例如www.baidu.com,还需要加上协议头
            # print(f"获取的请求内容为:\n{response.text}")                                          # 打印获取的网页内容,换行只是为了美观,如果网站不是utf-8格式,中文将显示为乱码
            # print(f"获取的请求内容为:\n{response.content.decode()}")                      # 这种方式更优秀,会将content获取的二进制内容转为utf_8格式,中文不会成为乱码
            with open(full_path_music,"wb") as f:
                f.write(response.content)
            print(f"恭喜大侠!文件已成功下载,位置: {full_path_music}")
            break                                                                                                     # 如果获取成功,则跳出while循环,否则会陷入死循环
        except ValueError as e:                                                                               # 捕获异常
            print(f"发生错误: {e}")                                                                              # 打印异常信息,这个except块处理结束后,try...except执行结束,重新
        except Exception as e:                                                                                # 捕获其他异常
            print(f"发生未知错误: {e}")                                                                        # 打印异常信息
            sys.exit(2)                                                                                               # 退出程序,错误码为2用来跟踪未知错误
    # os.startfile(full_path_music)                                                                         # 调用os方法运行,调用系统默认播放器,只在播放测试时使用