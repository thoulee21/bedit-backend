import json
import os
from pathlib import Path

import pytoml
from chat import chat
from django.conf import settings
from django.core.management import execute_from_command_line
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from markdown import markdown
from ocr import get_img_text
from utils.loguru_logger import logger

# Django settings
BASE_DIR = Path(__file__).resolve().parent.parent.parent
with open(BASE_DIR / "pyproject.toml", "r") as f:
    toml_config = pytoml.load(f)
    django_settings = {key.upper(): value for key, value in toml_config.items()}
    settings.configure(
        DEBUG=True,
        ROOT_URLCONF=__name__,
        ALLOWED_HOSTS=['*'],
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.staticfiles',
        ],
        MIDDLEWARE=[
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ],
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [],
                'APP_DIRS': True,
                'OPTIONS': {
                    'context_processors': [
                        'django.template.context_processors.debug',
                        'django.template.context_processors.request',
                        'django.contrib.auth.context_processors.auth',
                        'django.contrib.messages.context_processors.messages',
                    ],
                },
            },
        ],
        STATIC_URL='/static/',
        SECRET_KEY=os.environ.get('DJANGO_SECRET_KEY', 'your-secret-key'),
        **django_settings
    )

from django.urls import path


def index(request):
    return HttpResponse(f"Hello, I'm erniebot API v{settings.PROJECT['version']}!")

@csrf_exempt
@require_http_methods(["POST", "GET"])
def chat_prompt(request):
    if request.method == 'GET':
        return redirect('/')

    data = json.loads(request.body)
    prompt = data.get("prompt")
    former_messages = data.get("messages", [])

    stream = data.get("stream", False)
    html_enabled = data.get("html", False)

    logger.info(json.dumps(data, ensure_ascii=False))

    if not prompt:
        return HttpResponse("Please provide a prompt in request.", status=400)

    if stream:
        generate = chat(prompt, stream, former_messages)
        return StreamingHttpResponse(generate)
    else:
        response = chat(prompt, stream, former_messages)

        if html_enabled:
            return HttpResponse(markdown(response))
        else:
            return HttpResponse(response)

@csrf_exempt
@require_http_methods(["POST"])
def ocr(request):
    img_data = request.body
    if not img_data:
        return HttpResponse("Please provide an image in request.", status=400)

    response = get_img_text(img_data)
    return JsonResponse(list(response), safe=False)

urlpatterns = [
    path('', index),
    path('chat', chat_prompt),
    path('ocr', ocr),
]

if __name__ == '__main__':
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8080'])
