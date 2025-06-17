import os

credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

if credentials_path:
    print(f"环境变量 GOOGLE_APPLICATION_CREDENTIALS 已设置，路径为: {credentials_path}")
    if os.path.exists(credentials_path):
        print("密钥文件存在于指定路径。")
        # 尝试读取文件内容，确认是否是有效的JSON
        try:
            with open(credentials_path, 'r') as f:
                import json
                json.load(f)
            print("密钥文件是有效的 JSON。")
        except json.JSONDecodeError:
            print("警告：密钥文件不是有效的 JSON 格式！")
        except Exception as e:
            print(f"读取密钥文件时发生未知错误: {e}")
    else:
        print("错误：密钥文件不存在于指定路径！请检查路径是否正确。")
else:
    print("错误：环境变量 GOOGLE_APPLICATION_CREDENTIALS 未设置或未生效。")

print("\n请确保你运行此脚本的终端是设置环境变量后新打开的，或者你已重启 VS Code/电脑。")
