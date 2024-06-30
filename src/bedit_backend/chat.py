import os

import erniebot
from init_msgs import init_msgs

erniebot.api_type = "aistudio"
erniebot.access_token = os.environ.get("ERNIEBOT_ACCESS_TOKEN")


def chat(prompt: str, stream: bool = False):
    response = erniebot.ChatCompletion.create(
        # ernie-4.0, ernie-3.5, ernie-turbo
        model="ernie-3.5",
        stream=stream,
        messages=[*init_msgs, {
            "role": "user",
            "content": prompt
        }]
    )

    def generate():
        for message in response:
            yield message.get_result()

    if stream:
        return generate()
    else:
        return response.get_result()
