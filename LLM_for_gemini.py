# Gemini API新版SDK示例
import os
import textwrap
from google.genai import Client
from google.auth.exceptions import GoogleAuthError

gemini_key = os.getenv("gemini_key")
if not gemini_key:
    print("API未配置,请检查!")
    exit(10001)


try:
    client = Client(api_key=gemini_key)
    model_name = "gemini-3-flash"
    print(f"模型初始化成功!当前配置模型为:{model_name}")
except GoogleAuthError as e:
    print(f"认证失败:{e}!请检查API Key!")
    exit(10002)
except Exception as e:
    print(f"模型初始化失败:{e}!请检查配置!")
    exit(10003)

chat = client.chats.create(model=model_name)
print("\n--- Gemini 聊天机器人 ---")
print("你可以开始提问了。输入 '再见' 结束对话。")

while True:
    try:
        user_input = input("\n天上人间一号妹妹:")
        if user_input == "再见":
            print("先生慢走!欢迎再次光临!")
            break
        response = chat.send_message(user_input)
        print("\nGemini聊天机器人:")
        print(textwrap.fill(response.text or "", width=80))
    except GoogleAuthError as e:
        print(f"与 Gemini API 认证时发生错误:{e}")
        print("请检查你的API Key.")
    except Exception as e:
        print(f"发生未知错误:{e}")
        print("请重新启动聊天机器人程序!")
        break