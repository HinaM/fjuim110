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
    line_bot_api.reply_message(event.reply_token,event.message.text)


if __name__ == "__main__":
    app.run()