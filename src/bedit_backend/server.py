import os

import erniebot
from flask import Flask

erniebot.api_type = "aistudio"
erniebot.access_token = os.environ.get("ERNIEBOT_ACCESS_TOKEN")

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/chat/<prompt>/')
def prompt(prompt: str):
    response = erniebot.ChatCompletion.create(
        model="ernie-3.5",
        messages=[{
            "role": "user",
            "content": "请问你是谁？"
        }, {
            "role": "assistant",
            "content":
            "我是百度公司开发的人工智能语言模型，我的中文名是文心一言，英文名是ERNIE-Bot，可以协助您完成范围广泛的任务并提供有关各种主题的信息，比如回答问题，提供定义和解释及建议。如果您有任何问题，请随时向我提问。"
        }, {
            "role": "user",
            "content": prompt
        }]
    )
    return response.get_result()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
