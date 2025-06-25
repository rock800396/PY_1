import requests
from lxml import etree
from flask import Flask, render_template

def query_mobile(phone_num):
    url = f"https://www.ip138.com/mobile.asp?mobile={phone_num}&action=mobile"
    headers = {
        "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'

    e = etree.HTML(response.text)
    list_msg_1 = e.xpath("//tbody/tr/td/span/text()")
    list_msg_2 = e.xpath("//tbody/tr/td/a/text()")[-3:]
    list_msg = list_msg_2[0:1]+list_msg_1+ list_msg_2[1:3]
    return list_msg

if __name__ == "__main__":
    phone_num = input("请输入手机号码:")
    list_msg = query_mobile(phone_num)
    print(f"查询结果: {list_msg}")