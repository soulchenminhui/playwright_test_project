import os
import requests

API_KEY = os.getenv("DEEPSEEK_API_KEY","sk-7df2cf2b0764447eb3e7f86c139f31b4")
API_URL = "https://api.deepseek.com/chat/completions"

prompt = """你是一名资深自动化测试工程师。

请使用 Python + Playwright + Pytest
为以下网站生成 UI 自动化测试代码，要求：

1. 按POM模式生成Page类(带元素与方法)
2. 自动生成pytest测试用例文件(import对应Page类)
输出格式要求：
{
  "pages": {"xxx_page.py": "...代码..."},
  "tests": {"test_xxx.py": "...代码..."}
}
3. 定位器稳定，优先使用 data-test / id / name
4. 包含基础断言
5. 代码可以直接运行

网站:https://vks_thunder.ktvsky.com/#/

测试场景1:测试搜索功能(这是一个page)
具体步骤如下(这是一个tests中的详细步骤):
1. 打开网址
2. 点击搜索输入框
3. 输入“周杰伦”
4. 点击搜索按钮
5. 点击歌手
6. 点击歌曲
7. 点击任意一首歌曲

测试场景2:测试已点模块(这是一个page)
具体步骤如下(这是一个tests中的详细步骤):
1. 打开网址
2. 点击定制歌单
3. 点击任意一首歌曲
4. 点击已点
5. 点击已唱
6. 点击已点
7. 点击删除按钮
8. 点击关闭

请直接输出完整 Python 代码文件内容。"""

def generate_code(prompt: str):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    resp = requests.post(API_URL, headers=headers, json=payload)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


if __name__ == "__main__":
    code = generate_code(prompt)
    print(code)
