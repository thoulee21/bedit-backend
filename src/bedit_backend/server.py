import json

from chat import chat
from flask import Flask, Response, request, stream_with_context
from flask_cors import cross_origin
from markdown import markdown
from utils.loguru_logger import logger

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, erniebot! v0.1.2"


@app.route('/chat')
@cross_origin()
def chat_prompt():
    prompt = request.args.get("prompt")
    stream_raw = request.args.get("stream", 'false')
    # preferred to be false by default
    stream = stream_raw.lower() in ['true', '1', 'yes', 'y', 't']
    html_raw = request.args.get("html", 'false')
    html_enabled = html_raw.lower() in ['true', '1', 'yes', 'y', 't']

    logger.info(json.dumps(request.args.to_dict(), ensure_ascii=False))
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
        debug=True,
    )
