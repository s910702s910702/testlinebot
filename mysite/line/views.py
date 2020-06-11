from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from .models import *

import json

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


def is_secret(str):
    print(str)
    if str == '123456789':
        return True

    return False

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                res = json.loads(str(event.source))
                print(res['userId'])

                if is_secret(event.message.text) == True:
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text='666' + res['userId']))
                    print(Ppl.objects.get(secret = event.message.text).name)
                    Ppl.objects.filter(secret = event.message.text).update(lineuid = res['userId'])
                    print(event)

        #     print(event)
        #     if isinstance(event, MessageEvent):
        #         if isinstance(event.message, TextMessage):
        #             # line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))
        #             # line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.source.userId))
        #             line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))\

        return HttpResponse()
    else:
        return HttpResponseBadRequest()

def pushss(request):
    line_bot_api.push_message('U71fdc4be604bd742d2c24a729ae2c688', TextSendMessage(text="奏外"))
    return HttpResponse("已送出奏外") 

def ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    iplist.append(ip)

    return redirect("https://police.gov.taipei/")

def getip(request):
    ipstr = ''
    for ip in iplist:
        ipstr += ("\n" + ip)
    return HttpResponse(ipstr) 