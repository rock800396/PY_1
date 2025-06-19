# 这是一个测试XPath表达式的练习

import requests
from lxml import etree

url = "https://www.qidian.com/wuxia/"
headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"}

response = requests.get(url, headers=headers)
e = etree.HTML(response.text)
name = e.xpath('//div[@class = "book-info"]/h2/a/text()')
author = e.xpath('//div[@class = "state-box cf"]/a[@class = "author"]/text()')
print(name)
print(author)