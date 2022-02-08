from flask import Flask, request, abort
 
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

line_bot_api = LineBotApi('0YOmR5t/enr60Sxnp03ggMuNwmCPTbploASY6HVcpahhtNyXEQwAhKF+YhytXUcLRVuxYNaOJqjKzszVm72L9kCM2+C2KfyZA5Rx+fuXKdW8aChvdDOI5KNsy49+/JIJh8xDXWs8233iE8LXJqYsNwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('71caa7dfabd5410deb357a2e80194d11')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message=event.message.text
    message=message.encode('utf-8')
    if event.message.text=="遊戲任務":
        line_bot_api.reply_message(  
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='選擇遊戲任務。',
                            template=ButtonsTemplate(
                                title='遊戲任務',
                                text='選擇想遊玩的任務類型',
                                actions=[
                                    MessageTemplateAction(
                                        label='課程任務',
                                        text='課程任務'
                                    ),
                                    MessageTemplateAction(
                                        label='建築任務',
                                        text='建築任務'
                                    ),
                                    MessageTemplateAction(
                                        label='生活任務',
                                        text='生活任務'
                                    )
                                ]
                            )
                        )
                    )
    elif event.message.text=="遊戲規則":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="規則是巴拉巴拉之類的"))
    elif event.message.text=="個人檔案":
        user_id = event.source.user_id         
        profile = line_bot_api.get_profile(user_id)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="學生證"+"\n"+"姓名："+profile.display_name+"\n"+"目前學分數："+"\n"+"還需很多學分升上二年級"))
    else:    
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)