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

'''
def get_seoul_weather():
    try:
        r = requests.get('http://api.openweathermap.org/data/2.5/forecast/daily?lat=37.56826&lon=126.977829&APPID=cd95f9904b38f03ac8b68901cff2c720')
        data = json.loads(r.text)

        temp = float(data["main"]["temp"]) - 273.15
        min_temp = float(data["main"]["temp_min"]) - 273.15
        max_temp = float(data["main"]["temp_max"]) - 273.15
        humid = data["main"]["humidity"]

        msg = "오늘 서울의 온도는 {}도, 최저 온도는 {}도, 최고 온도는 {}도, 습도는 {}%입니다. ".format(temp, min_temp, max_temp, humid)

        return msg

    except:
        return "날씨 api에 문제가 생겼습니다. 나중에 다시 시도해주세요!"
'''
'''
def get_exchange():
    try:
        r = requests.get('http://earthquake.kr:23490/')
        data = json.loads(r.text)

        jtok = data['JPYKRW'][0]
        #date_now = datetime.today().strftime("%Y/%m/%d %H:%M:%S")

        ratio = 100
        msg = "현재 환율은 {}엔에 {}원입니다".format(ratio, round(float(jtok) * ratio, 2))

        return(msg)
    except:
        return "환율 api에 문제가 생겼습니다. 나중에 다시 시도해주세요!"
'''

def get_pretty_print(json_object):
    dumps = json.dumps(json_object, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
    return dumps


def keyboard_default():
    return {
        "type": "buttons",
        "buttons": ["환율", "오늘서울날씨"]
    }


def keyboard(request):
    return HttpResponse(get_pretty_print(keyboard_default()), content_type="application/json; charset=utf-8")


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
        else:
            msg = "잘못된 요청입니다."

        message_default = {"message": {
            "text": msg
        }}
        message_default["keyboard"] = keyboard_default()

        return HttpResponse(get_pretty_print(message_default), content_type="application/json; charset=utf-8")
    else:
        raise Http404("잘못된 접근입니다.")


@csrf_exempt
def friend(request, user_key=''):
    return HttpResponse('')


@csrf_exempt
def chat_room(request, user_key=''):
    return HttpResponse('')
