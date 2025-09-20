# 测试gemini接口调用
import importlib
import os
import textwrap  # 用于格式化输出,让长文本在控制台显示更美观,这是pyton官方库
from google.api_core.exceptions import GoogleAPIError  # 导入Google API的通用异常基类


# 动态导入 google.generativeai，避免静态分析器抱怨某些符号未导出
try:
    _gemini_mod = importlib.import_module("google.generativeai")
except Exception as e:
    print("未能导入 google.generativeai 模块，请确认已安装官方 SDK（pip install --upgrade google-generative-ai)")
    print(f"导入错误: {e}")
    exit(10000)

# 尝试找到 configure 和 GenerativeModel 的可用方式
_configure_obj = getattr(_gemini_mod, "configure", None)
GenerativeModel = getattr(_gemini_mod, "GenerativeModel", None)

if _configure_obj is None:
    # 有些 SDK 版本可能通过 client 配置或直接使用环境变量，此处只是告知并继续
    def configure(*args, **kwargs):
        print("警告: 当前 google.generativeai 版本没有显式导出 'configure'。如果需要，请使用环境变量或升级 SDK。")
else:
    configure = _configure_obj

if GenerativeModel is None:
    # 兼容性回退：某些版本可能提供一个工厂函数或类名不同，尝试查找常见替代项
    GenerativeModel = getattr(_gemini_mod, "Model", None) or getattr(_gemini_mod, "Models", None)

    if GenerativeModel is None:
        print("警告: 当前 google.generativeai 版本没有导出 'GenerativeModel'。无法继续初始化模型。")
        print("请检查 SDK 文档或升级到支持 GenerativeModel 的版本。")
        exit(10002)


gemini_key = os.getenv("gemini_key")  # 从系统环境变量中读取gemini的API

if gemini_key:
    try:
        configure(api_key=gemini_key)
        print("API配置成功!")
    except Exception:
        # 如果 configure 是回退的占位函数，上面可能只是打印警告，但许多 SDK 也支持从环境变量读取 key
        print("调用 configure 时遇到问题：继续运行并尝试依赖环境变量或 SDK 的默认行为。")
else:
    print("API未配置,请检查!")
    exit(10001)

try:
    model_name = "gemini-2.5-flash"
    model = GenerativeModel(model_name)
    print(f"模型初始化成功!当前配置模型为:{model_name}")
except Exception as e:
    print(f"模型初始化失败:{e}!请检查配置!")
    exit(10003)

chat = model.start_chat(history=[])
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
        print(textwrap.fill(response.text, width=80))
    except GoogleAPIError as e:
        print(f"与 Gemini API 交互时发生错误:{e}")
        print("请检查你的网络连接或 API Key.")
    except Exception as e:
        print(f"发生未知错误:{e}")
        print("请重新启动聊天机器人程序!")
        break