import os

import erniebot
from utils.init_msgs import init_msgs
from utils.db_handler import DBHandler

mongodb = DBHandler('ChatResponse')

erniebot.api_type = "aistudio"
erniebot.access_token = os.environ.get("ERNIEBOT_ACCESS_TOKEN")


def chat(prompt: str, stream: bool = False, former_messages: list = [dict]):
    response = erniebot.ChatCompletion.create(
        # ernie-4.0, ernie-3.5, ernie-turbo
        model="ernie-3.5",
        stream=stream,
        messages=[
            *init_msgs,
            *former_messages,
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
        return generate()
    else:
        mongodb.insert(response.to_dict())
        return response.get_result()
