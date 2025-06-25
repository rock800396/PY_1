# 测试gemini接口调用
import google.generativeai as gemini                                                         # 导入gemini库,这是谷歌官方发布的SDK
import os
import textwrap                                                                                                         # 用于格式化输出,让长文本在控制台显示更美观,这是pyton官方库
from google.api_core.exceptions import GoogleAPIError               # 导入Google API的通用异常基类

gemini_key = os.getenv("gemini_key")                                                        # 从系统环境变量中读取gemini的API

if gemini_key:
    gemini.configure(api_key=gemini_key)
    print("API配置成功!")
else:
    print("API未配置,请检查!")
    exit(10001)

try:
    model_name = "gemini-2.5-flash"
    model = gemini.GenerativeModel(model_name)
    print(f"模型初始化成功!当前配置模型为:{model_name}")
except Exception as e:
    print(f"模型初始化失败:{e}!请检查配置!")
    exit(10002)

chat = model.start_chat(history=[])
print("\n--- Gemini 聊天机器人 ---")
print("你可以开始提问了。输入 '再见' 结束对话。")

while True:
    try:
        user_input = input("\n天上人间一号妹妹:")
        if user_input == "再见" :
            print("先生慢走!欢迎再次光临!")
            break
        response = chat.send_message(user_input)
        print("\nGemini聊天机器人:")
        print(textwrap.fill(response.text, width=80))
    except GoogleAPIError as e:
        print(f"与 Gemini API 交互时发生错误:{e}")
        print("请检查你的网络连接或 API Key.")
    except Exception as e:
        print(f"发生未知错误:{e}")
        print("请重新启动聊天机器人程序!")
        break