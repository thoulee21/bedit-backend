import json
import os
from pathlib import Path

import pytoml
from chat import chat
from flask import Flask, Response, redirect, request, stream_with_context
from flask_cors import cross_origin
from markdown import markdown
from ocr import get_img_text
from utils.loguru_logger import logger

app = Flask(__name__)

with open(Path(os.getcwd()) / "pyproject.toml", "r") as f:
    app.config.update(pytoml.load(f))


@app.route('/')
def index():
    return f"Hello, I'm erniebot API v{app.config.get('project').get('version')}!"


@app.route('/chat', methods=['POST', 'GET'])
@cross_origin(methods=['POST', 'GET'])
def chat_prompt():
    if request.method == 'GET':
        return redirect('/')

    prompt = request.json.get("prompt")
    former_messages = request.json.get("messages", [])

    stream = request.json.get("stream", False)
    html_enabled = request.json.get("html", False)

    logger.info(json.dumps(request.json, ensure_ascii=False))

    if not prompt:
        return "Please provide a prompt in request.", 400

    if stream:
        generate = chat(prompt, stream, former_messages)
        return Response(stream_with_context(generate))
    else:
        response = chat(prompt, stream, former_messages)

        if html_enabled:
            return markdown(response)
        else:
            return response


@app.route('/ocr', methods=['POST'])
@cross_origin(methods=['POST'])
def ocr():
    img_data = request.get_data()
    if not img_data:
        return "Please provide an image in request.", 400

    response = get_img_text(img_data)
    return list(response)


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=True,
    )
