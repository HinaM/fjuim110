from cgitb import text
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
                template=ImageCarouselTemplate(
                    columns=[
                        ImageCarouselColumn(
                            image_url="https://upload.cc/i1/2022/02/03/J9OPX7.jpg",
                            action=URITemplateAction(
                                label="課程任務",
                                text="課程任務"
                            )
                        ),
                        ImageCarouselColumn(
                            image_url="https://upload.cc/i1/2022/02/03/UKhvma.jpg",
                            action=URITemplateAction(
                                label="生活任務",
                                text="生活任務"
                            )
                        ),
                        ImageCarouselColumn(
                            image_url="https://upload.cc/i1/2022/02/03/IkOir7.jpg",
                            action=URITemplateAction(
                                label="建築任務",
                                text="建築任務"
                            )
                        )
                    ]
                )
            )
        )
    else:    
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)