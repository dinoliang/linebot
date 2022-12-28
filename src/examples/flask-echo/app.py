# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

import os
import sys
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, MessageAction, TemplateSendMessage, CarouselTemplate, CarouselColumn, QuickReply, QuickReplyButton,
)

#from googletrans import Translator # Google 翻譯模組

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    # basic
    '''
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )
    '''

    # further
    message = text=event.message.text
    if '股票' in message:
        #line_bot_api.reply_message(event.reply_token, TextSendMessage('Come in 001' + message))

        buttons_template_message = TemplateSendMessage(
            alt_text = '股票資訊',
            template = CarouselTemplate(
                columns = [
                    CarouselColumn(
                        thumbnail_image_url = 'https://miro.medium.com/max/1838/1*xRW05xCHmq7r8OOmFzlosw.png',
                        title = message + '股票資訊',
                        text = '請點選請查詢的股票資訊',
                        actions = [
                            MessageAction(
                                label = 'xxx' + ' 個股資訊',
                                text = '個股資訊 ' + 'xxx'
                            ),
                            MessageAction(
                                label = 'xxx' + ' 個股新聞',
                                text = '個股新聞 ' + 'xxx'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url = 'https://miro.medium.com/max/1838/1*xRW05xCHmq7r8OOmFzlosw.png',
                        title = message + '股票資訊',
                        text = '請點選請查詢的股票資訊',
                        actions = [
                            MessageAction(
                                label = 'xxx' + ' 最新分鐘圖',
                                text = '最新分鐘圖 ' + 'xxx'
                            ),
                            MessageAction(
                                label = 'xxx' + ' 日線圖',
                                text = '日線圖 ' + 'xxx'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url = 'https://miro.medium.com/max/1838/1*xRW05xCHmq7r8OOmFzlosw.png',
                        title = message + '股票資訊',
                        text = '請點選請查詢的股票資訊',
                        actions = [
                            MessageAction(
                                label = 'xxx' + ' 平均股利',
                                text = '平均股利 ' + 'xxx'
                            ),
                            MessageAction(
                                label = 'xxx' + ' 歷年股利',
                                text = '歷年股利' + 'xxx'
                            )
                        ]
                    )
                ]
            )
        )

        #line_bot_api.reply_message(event.reply_token, TextSendMessage('Come in 002' + message))

        line_bot_api.reply_message(event.reply_token, buttons_template_message)
    elif '大戶' in message:
        # only show on mobile
        flex_message = TextSendMessage(
            text = '請選擇要顯示的資訊',
            quick_reply = QuickReply(
                items = [
                    QuickReplyButton(action=MessageAction(label='最近法人', text='最近法人買賣超')),
                    QuickReplyButton(action=MessageAction(label='歷年法人', text='歷年法人買賣超')),
                    QuickReplyButton(action=MessageAction(label='外資', text='外資買賣超')),
                    QuickReplyButton(action=MessageAction(label='投信', text='投信買賣超')),
                    QuickReplyButton(action=MessageAction(label='自營商', text='自營商買賣超')),
                    QuickReplyButton(action=MessageAction(label='三大法人', text='三大法人買賣超'))
                ]
            )
        )

        line_bot_api.reply_message(event.reply_token, flex_message)
    
    elif '@翻英' in message or '@翻日' in message or '@翻中' in message:
        '''
        if message[:3] == "@翻英":
            content = translate_text(message[3:], "en")
            message = TextSendMessage(text=content)
            line_bot_api.reply_message(event.reply_token, message)
        if message[:3] == "@翻日":
            content = translate_text(message[3:] , "ja")
            message = TextSendMessage(text=content)
            line_bot_api.reply_message(event.reply_token, message)
        if message[:3] == "@翻中":
            content = translate_text(message[3:] , "zh-tw")
            message = TextSendMessage(text=content)
            line_bot_api.reply_message(event.reply_token, message)
        '''
        pass
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message + '???'))
    
    return

'''
#新增自訂translate_text()函數
def translate_text(text, dest='en'):
    """以google翻譯將text翻譯為目標語言

    :param text: 要翻譯的字串，接受UTF-8編碼。
    :param dest: 要翻譯的目標語言，參閱googletrans.LANGCODES語言列表。
    """
    translator = Translator()
    result = translator.translate(text, dest).text
    return result
'''

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
