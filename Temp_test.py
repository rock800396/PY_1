import requests

index = "https://tieba.baidu.com/p/9805631065"

response = requests.get(index).text

print(response)