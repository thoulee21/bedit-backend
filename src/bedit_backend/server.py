import json
import os
from pathlib import Path

import pytoml
from chat import chat
from flask import Flask, Response, request, stream_with_context
from flask_cors import cross_origin
from markdown import markdown
from utils.loguru_logger import logger

app = Flask(__name__)

with open(Path(os.getcwd()) / "pyproject.toml", "r") as f:
    app.config.update(pytoml.load(f))


@app.route('/')
def index():
    return f"Hello, I'm erniebot API v{app.config.get('project').get('version')}!"


@app.route('/chat', methods=['POST'])
@cross_origin()
def chat_prompt():
    prompt = request.json.get("prompt")
    stream = request.json.get("stream", False)
    html_enabled = request.json.get("html", False)

    logger.info(json.dumps(request.json, ensure_ascii=False))

    if not prompt:
        return "Please provide a prompt in the query string.", 400

    if stream:
        generate = chat(prompt, stream)
        return Response(stream_with_context(generate))
    else:
        response = chat(prompt, stream)

        if html_enabled:
            return markdown(response)
        else:
            return response


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=8080,
    )
