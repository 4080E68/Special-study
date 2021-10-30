from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from func3api.models import Location

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *
from module import func
from urllib.parse import parse_qsl
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import requests

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        #先設定一個要回傳的message空集合
        message = []
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

        for event in events:
            if isinstance(event, MessageEvent):
                print(event.message.type)
                if event.message.text == "新竹":
                    # 篩選location資料表中，地區欄位為使用者發送地區的景點資料
                    locations = Location.objects.filter(area=event.message.text)

                    content = ''  # 回覆使用者的內容
                    for location in locations:
                        content += location.name + '\n' + location.address

                    line_bot_api.reply_message(  # 回覆訊息
                        event.reply_token,
                        TextSendMessage(text=content)
                    )
                if event.message.text == "台中":
                    # 篩選location資料表中，地區欄位為使用者發送地區的景點資料
                    locations = Location.objects.filter(
                        area=event.message.text)

                    content = ''  # 回覆使用者的內容
                    for location in locations:
                        content += location.name + '\n' + location.address

                    line_bot_api.reply_message(  # 回覆訊息
                        event.reply_token,
                        TextSendMessage(text=content)
                    )
                if event.message.text =="@傳送文字":
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="我是 Linebot，\n您好！")
                        )
                if event.message.text == "@傳送圖片":
                    line_bot_api.reply_message(
                        event.reply_token,
                        ImageSendMessage(
                            original_content_url="https://i.imgur.com/q67isps.png",
                            preview_image_url="https://i.imgur.com/q67isps.png"
                        )
                    )
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


                if event.message.text == "11":
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                title='查詢地區',
                                text='請選擇地區',
                                actions=[
                                    MessageTemplateAction(
                                        label='新竹',
                                        text='新竹'
                                    ),
                                    MessageTemplateAction(
                                        label='台中市',
                                        text='台中'
                                    ),
                                    MessageTemplateAction(
                                        label='高雄市',
                                        text='高雄市'
                                    )
                                ]
                            )
                        )
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
