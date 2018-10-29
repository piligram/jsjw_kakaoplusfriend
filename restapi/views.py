from django.shortcuts import render
from django.http.response import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
import requests
import json
from datetime import datetime

from restapi.api_src.jypkrw_rate import get_exchange
from restapi.api_src.weather import get_seoul_weather
from restapi.api_src.movie_info import get_movie_info

def pretty_print(json_object):
    dumps = json.dumps(json_object, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
    return dumps


def keyboard_default():
    return {
        "type": "buttons",
        "buttons": ["환율", "오늘서울날씨", "영화정보"]
    }


def keyboard(request):
    return HttpResponse(pretty_print(keyboard_default()), content_type="application/json; charset=utf-8")


@csrf_exempt
def message(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        _user_key = data["user_key"]
        _type = data["type"]
        _content = data["content"]

        msg = ""
        print(_user_key, _type, _content)

        if _content == "환율":
            msg = get_exchange()
        elif _content == "오늘서울날씨":
            msg = get_seoul_weather()
        elif _content == "영화정보":
            msg = get_movie_info()
        else:
            msg = "잘못된 요청입니다."

        message_default = {"message": {
            "text": msg
        }}
        message_default["keyboard"] = keyboard_default()

        return HttpResponse(pretty_print(message_default), content_type="application/json; charset=utf-8")
    else:
        raise Http404("잘못된 접근입니다.")


@csrf_exempt
def friend(request, user_key=''):
    return HttpResponse('')


@csrf_exempt
def chat_room(request, user_key=''):
    return HttpResponse('')
