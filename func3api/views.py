from typing import Text
#from django.db.models.fields import _ErrorMessagesToOverride, TextField
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from func3api.models import *
import subprocess
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *
from module import func
from urllib.parse import parse_qsl
import requests
import web_crawler

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
HEROKU_APP_URL = ' https://topiclinebot.herokuapp.com/'


def listone(request):
    try:
        unit = display.objects.get(price=21900)
    except:
        errorMessage = "(讀取錯誤!)"
    return render(request,'listone.html',locals())


def listall(request):
    try:
        unit = display.objects.get(id=3)
        displays = display.objects.all().order_by('id')
    except:
        errorMessage = "(讀取錯誤!)"
    return render(request, 'listall.html', locals())

def index(request):
    try:
        unit = display.objects.get(id=3)
        displays = display.objects.all().order_by('id')
    except:
        errorMessage = "(讀取錯誤!)"
    return render(request, 'index.html', locals())


def ssd(request):
    
    return render(request, 'ssd.html', locals())


def cpu(request):

    return render(request, 'cpu.html', locals())

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        #先設定一個要回傳的message空集合
        message = []
        keyword = []
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        #在這裡將body寫入機器人回傳的訊息中，可以更容易看出你收到的webhook長怎樣#
        message.append(TextSendMessage(text=str(body)))

        try:
            events = parser.parse(body, signature)
            print(events)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        try:

            for event in events:
                if isinstance(event, MessageEvent):
                    msg = event.message.text

                if msg[:3] == '###' and len(msg) > 3:
                        func.manageForm(event, msg)
                

                if 'pc+' in msg:
                        keyword = msg.split('+')[1]
                        message = web_crawler.youtube_vedio_parser(keyword)
                        line_bot_api.reply_message(event.reply_token, message)

                if event.message.text == "@傳送位置":
                        line_bot_api.reply_message(
                            event.reply_token,
                            LocationSendMessage(
                                title='崑山科技大學 Kun Shan University',
                                address='710台南市永康區崑大路195號',
                                latitude=22.99792647872198,  # 緯度
                                longitude=120.25310442615711  # 經度
                            )
                        )
        except:
            if isinstance(event, MessageEvent):
                    display_name = display.objects.filter(name=event.message.text)
                    for displays in display_name:
                        flex_message = FlexSendMessage(
                            alt_text='搜尋結果',
                            contents={
                                "type": "bubble",
                                "hero": {
                                    "type": "image",
                                    "url": displays.pc_images,
                                    "size": "full",
                                    "aspectRatio": "3:2",
                                    "aspectMode": "cover",
                                    "action": {
                                        "type": "uri",
                                        "uri": displays.pc_images
                                    }
                                },
                                "body": {
                                    "type": "box",
                                    "layout": "vertical",
                                    "spacing": "md",
                                    
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "價格:"+displays.price,
                                            "size": "xl",
                                            "weight": "bold"
                                        },
                                        {
                                            "type": "separator",
                                            "color": "#000000"
                                        },
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "spacing": "sm",
                                            "contents": [
                                                {
                                                    "type": "box",
                                                    "layout": "baseline",
                                                    "contents": [
                                                        {
                                                            "type": "icon",
                                                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/restaurant_regular_32.png"
                                                        },
                                                        {
                                                            "type": "text",
                                                            "text": "詳細資訊",
                                                            "weight": "bold",
                                                            "margin": "sm",
                                                            "flex": 0
                                                        }
                                                    ]
                                                },
                                                {
                                                    "type": "box",
                                                    "layout": "vertical",
                                                    "contents": [
                                                        {
                                                            "type": "text",
                                                            "wrap": True,
                                                            "align": "start",
                                                            "offsetStart": "xxl",
                                                            "size": "xs",
                                                            "text": displays.commodity
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                },
                                "footer": {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "button",
                                            "style": "primary",
                                            "color": "#905c44",
                                            "action": {
                                                "type": "uri",
                                                "label": "購買連結",
                                                "uri": displays.url_list
                                            }
                                        }
                                    ]
                                }
                            }
                            

                        )

                        content = ''  # 回覆使用者的內容
                        content += "價格:"+displays.price + '\n' + \
                        displays.commodity + '\n' + displays.url_list + '\n'+displays.pc_images
                            

                        line_bot_api.reply_message(  # 回覆訊息
                            event.reply_token, flex_message
                        )

            



               

    
        if isinstance(event, PostbackEvent):  #PostbackTemplateAction觸發此事件
                backdata = dict(parse_qsl(event.postback.data))  #取得Postback資料
                if backdata.get('action') == 'buy':
                    func.sendBack_buy(event, backdata)
                #elif backdata.get('action') == 'sell':
                #    func.sendBack_sell(event, backdata)
                elif backdata.get('action') == 'sell':
                    func.sendData_sell(event, backdata)

        return HttpResponse()

    else:
        return HttpResponseBadRequest()

