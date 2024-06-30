import json
import os

import erniebot
import user_agents
from flask import Flask, Response, request, stream_with_context
from markdown import markdown
from utils.loguru_logger import logger

erniebot.api_type = "aistudio"
erniebot.access_token = os.environ.get("ERNIEBOT_ACCESS_TOKEN")

app = Flask(__name__)


@app.route('/')
def index():
    args = request.args.to_dict()
    if args:
        return json.dumps(args)
    else:
        return "Hello, erniebot!"


@app.route('/chat')
def prompt():
    prompt = request.args.get("prompt")
    stream_raw = request.args.get("stream", 'false')
    # preferred to be false by default
    stream = stream_raw.lower() in ['true', '1', 'yes', 'y', 't']
    logger.info(
        f"prompt: {prompt}, stream: {stream}, stream_raw: {stream_raw}"
    )

    if not prompt:
        return "Please provide a prompt in the query string.", 400

    response = erniebot.ChatCompletion.create(
        model="ernie-3.5",
        stream=stream,
        messages=[
            {
                "role": "user",
                "content": "请问你是谁？"
            }, {
                "role": "assistant",
                "content":
                "我是百度公司开发的人工智能语言模型，我的中文名是文心一言，英文名是ERNIE-Bot，可以协助您完成范围广泛的任务并提供有关各种主题的信息，比如回答问题，提供定义和解释及建议。如果您有任何问题，请随时向我提问。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    def generate():
        for message in response:
            yield message.get_result()

    if stream:
        return Response(stream_with_context(generate()))
    else:
        # 如果访问来自于浏览器，返回markdown格式的文本
        ua = user_agents.parse(request.user_agent.string)

        if ua.is_bot:
            return response.get_result()
        else:
            return markdown(response.get_result())


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=True,
    )
