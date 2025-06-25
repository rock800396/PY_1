import requests
from lxml import etree
from flask import Flask, render_template, request

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

app = Flask(__name__)

# 这是主页入口,访问"http://127.0.0.1:5000"时会渲染index.html模板
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/query")
def query():
    # 注意,这里的request不是requests库的request,而是Flask框架提供的请求对象
    phone_num = request.args.get('phone_num')
    # query_mobile(phone_num)返回的是一个列表,需要将其转换为字符串
    return "<br/>".join(query_mobile(phone_num))

app.run(debug=True)