
# ----------------这是一个基于Google Custom Search引擎的关键词搜索/翻译实现-------------------

from googleapiclient.discovery import build
from google.cloud import translate_v2 as translate
import sys
import os
import httplib2

# --- 配置你的 API Key 和 CX ID ---
API_KEY = "AIzaSyAYTvCOra6t1btoVRLFe9oPmtN0rUySyGI"
CX_ID = "d2f7c3453d86144f2"

# --- 配置你的代理信息 ---
PROXY_HOST = "127.0.0.1"
PROXY_PORT = 10090
PROXY_TYPE = httplib2.socks.PROXY_TYPE_HTTP # 假设是 HTTP 代理

# --- 初始化翻译客户端 ---
try:
    translate_client = translate.Client()
    print("Google Cloud Translation 客户端初始化成功。")
except Exception as e:
    print(f"警告：Google Cloud Translation 客户端初始化失败: {e}")
    print("请确保已设置 GOOGLE_APPLICATION_CREDENTIALS 环境变量，或检查服务账号密钥文件。")
    translate_client = None

def google_custom_search(query_input, api_key, cx_id, num_results=15):
    """
    使用 Google Custom Search API 进行搜索，并支持自动翻译中文关键词。
    """
    query_to_use = query_input.strip()

    # --- 尝试翻译关键词 ---
    if translate_client and any('\u4e00' <= char <= '\u9fff' for char in query_to_use):
        print(f"检测到中文关键词: '{query_to_use}'，尝试翻译为英文...")
        try:
            translation_result = translate_client.translate(query_to_use, target_language='en')
            translated_query = translation_result['translatedText']
            print(f"翻译后的英文关键词: '{translated_query}'")
            query_to_use = translated_query
        except Exception as e:
            print(f"关键词翻译失败: {e}")
            print("将使用原始关键词进行搜索。请检查 Cloud Translation API 配置和认证。")

    elif not translate_client:
        print("翻译客户端未初始化，无法进行关键词翻译。将使用原始关键词进行搜索。")

    # --- 配置代理 ---
    try:
        proxy_info = httplib2.ProxyInfo(
            PROXY_TYPE,
            PROXY_HOST,
            PROXY_PORT
        )
        http = httplib2.Http(proxy_info=proxy_info)
        proxy_type_str = "HTTP" if PROXY_TYPE == httplib2.socks.PROXY_TYPE_HTTP else \
                         ("SOCKS5" if PROXY_TYPE == httplib2.socks.SOCKS5 else "SOCKS")
        print(f"代理已配置: {PROXY_HOST}:{PROXY_PORT} (类型: {proxy_type_str})")
    except Exception as e:
        print(f"代理配置失败: {e}")
        print("将尝试不使用代理进行连接。")
        http = None

    # --- 执行 Google Custom Search API 查询 ---
    try:
        service = build("customsearch", "v1", developerKey=api_key, http=http)

        res = service.cse().list(
            q=query_to_use,
            cx=cx_id,
            lr="lang_en",  # 限制信息来源为英文网页
            hl="zh-CN",   # 尝试影响界面语言和部分摘要翻译（效果不保证）
            num=num_results
        ).execute()

        return res.get('items', [])

    except Exception as e:
        print(f"调用 Google Custom Search API 失败: {e}")
        return None

if __name__ == "__main__":
    while True:
        search_term_input = input("请输入搜索参数 (中文或英文): ")
        if not search_term_input.strip():
            print("搜索关键词不能为空，请重新输入。")
            continue

        print(f"\n正在使用 Google Custom Search API 搜索: '{search_term_input}'...")
        results = google_custom_search(search_term_input, API_KEY, CX_ID)

        if results:
            print("\n--- 搜索结果 ---")
            for i, item in enumerate(results):
                original_title = item.get('title', '无标题')
                original_snippet = item.get('snippet', '无摘要').replace('&#39;', "'").replace('&quot;', '"')
                link = item.get('link', '无链接')

                translated_title = original_title
                translated_snippet = original_snippet

                # *** 关键修改在这里：显式调用翻译服务 ***
                if translate_client: # 确保翻译客户端已成功初始化
                    try:
                        # 翻译标题
                        title_translation_result = translate_client.translate(original_title, target_language='zh-CN')
                        translated_title = title_translation_result['translatedText']

                        # 翻译摘要
                        snippet_translation_result = translate_client.translate(original_snippet, target_language='zh-CN')
                        translated_snippet = snippet_translation_result['translatedText']
                    except Exception as e:
                        print(f"警告：翻译搜索结果失败: {e}。将显示原始英文内容。")
                        # 翻译失败时，保持原始英文内容

                print(f"{i+1}. 标题: {translated_title}")
                print(f"   链接: {link}")
                print(f"   摘要: {translated_snippet}\n")
            break
        else:
            print("未找到结果或 API 调用失败。请检查关键词或 API 配置。")