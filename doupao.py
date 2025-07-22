# doubao.py
import os
import requests

def get_doubao_reply(user_input):
    url = "https://open.doubao.com/llm/chat/completions"

    headers = {
        "Authorization": f"Bearer {os.getenv('DOUBAO_API_KEY')}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "glm-4",  # 可换成 glm-3-turbo
        "messages": [
            {"role": "system", "content": "你是一名中文简历撰写顾问，请根据用户输入生成适合的职业建议或简历内容。"},
            {"role": "user", "content": user_input}
        ]
    }

    try:
        res = requests.post(url, headers=headers, json=body, timeout=10)
        res.raise_for_status()
        return res.json()['choices'][0]['message']['content']
    except Exception as e:
        print("豆包AI错误：", e)
        return "对不起，我暂时无法生成内容，请稍后再试。"
