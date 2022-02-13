from flask import Flask, request, abort
 
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from fileinput import filename
import gspread

gc=gspread.service_account(filename='fjuim-340916-7e527f907c19.json')
sh=gc.open_by_key('1LozvTUSglnM_TtYO1tyDROkFkpX4lrlaVD1tC0911XM')
worksheet=sh.sheet1
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
    if event.message.text=="開始遊戲":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            #重置設定施工中
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已經開始遊戲，要重置嗎"))
        else:
            userid_list=worksheet.col_values(1)
            x=len(userid_list)
            list=[]
            for i in range(65,76):
                list.append(chr(i)+str(x+1))
            #ID
            worksheet.update(list[0],event.source.user_id)
            #題目數量施工中
            #初始值設定
            for i in range(1,len(list)):
                worksheet.update(list[i],int(0))
            worksheet.update(list[3],int(1))
            confirm_template_message = TemplateSendMessage(
                alt_text='請選擇視角',
                template=ConfirmTemplate(
                    text='選擇以日向（男主角）或是小光（女主角）的視角遊玩。',
                    actions=[
                        MessageAction(
                            label='日向',
                            text='以日向的視角進行遊戲'
                        ),
                        MessageAction(
                            label='小光',
                            text='以小光的視角進行遊戲'
                        )
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token,confirm_template_message)

    elif event.message.text=="選擇視角":
        confirm_template_message = TemplateSendMessage(
                alt_text='請選擇視角',
                template=ConfirmTemplate(
                    text='選擇以日向（男主角）或是小光（女主角）的視角遊玩。',
                    actions=[
                        MessageAction(
                            label='日向',
                            text='以日向的視角進行遊戲'
                        ),
                        MessageAction(
                            label='小光',
                            text='以小光的視角進行遊戲'
                        )
                    ]
                )
            )
        line_bot_api.reply_message(event.reply_token,confirm_template_message)    

    elif event.message.text=="以日向的視角進行遊戲":
        userid_list=worksheet.col_values(1)
        #ID已寫入
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('C'+str(j))
            #ID已寫入且已選擇視角
            if worksheet.acell(list[0]).value=="0":
                worksheet.update(list[0],int(1))
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="選擇了日向視角，選擇遊戲任務開始遊戲吧！"))
            #ID已寫入建立且視角!=0
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已經選日向視角，要重置請輸入「重置遊戲」。"))
        #ID未寫入
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="還沒建立個人檔案喔，輸入「開始遊戲」建立。"))
            
    elif event.message.text=="以小光的視角進行遊戲":
        userid_list=worksheet.col_values(1)
        #ID已寫入
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('C'+str(j))
            #ID已寫入且已選擇視角
            if worksheet.acell(list[0]).value=="0":
                worksheet.update(list[0],int(2))
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="選擇了小光視角，選擇遊戲任務開始遊戲吧！"))
            #個人檔案已建立且視角!=0
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已經選小光視角，要重置請輸入「重置遊戲」。"))
        #ID未寫入
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="還沒建立個人檔案喔，輸入「開始遊戲」建立。"))

    #文字施工中
    elif event.message.text=="遊戲規則":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="發生在輔大資管系某一屆普通卻又不普通的故事，透過回答問題一步步解鎖劇情。"+"\n"+"問題分成三類：生活、建築、課程，回答課程類問題可以增加學分升級喔。"))
    
    elif event.message.text=="人物介紹":
        carousel_template_message = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://dic.nicovideo.jp/oekaki/725601.png',
                        title='日向',
                        text='男主角',
                        actions=[
                            MessageAction(
                                label='角色資料',
                                text='日向角色資料'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://img.komicolle.org/2019-04/15566418114917.jpg',
                        title='小光',
                        text='女主角',
                        actions=[
                            MessageAction(
                                label='角色資料',
                                text='小光角色資料'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://5.share.photo.xuite.net/davidyea2006/15c7ae8/19334735/1060636313_x.jpg',
                        title='司',
                        text='男主朋友',
                        actions=[
                            MessageAction(
                                label='角色資料',
                                text='司角色資料'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://ygodl.com/wp-content/uploads/2021/09/5_Moment.jpg',
                        title='羽山',
                        text='學霸',
                        actions=[
                            MessageAction(
                                label='角色資料',
                                text='羽山角色資料'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,carousel_template_message)
    elif event.message.text=="日向角色資料":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="萬年吊車尾的日向，竟誤打誤撞的考上了輔大資管系，還遇到自己的真命天女—小光。為了要讓小光喜歡上他，日向開始努力讀書，希望有一天能被小光看見。"))
    elif event.message.text=="小光角色資料":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="以全校第一的成績進入輔大資管系，無論何時何地都在讀書。平時都擺著一張撲克臉，讓人難以親近的樣子。不過一看到小動物時，臉上總是洋溢著幸福的笑容。"))
    elif event.message.text=="司角色資料":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="大二才轉學過來的轉學生，是日向的死黨。和日向一起去打籃球、吃飯、上課，雖然偶爾冒冒失失的，但是總是把朋友擺在第一位，常常把「兄弟就是要有福同享、有難同當阿」掛在嘴邊。"))
    elif event.message.text=="羽山角色資料":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="「萬般皆下品，唯有讀書高」是他的人生名言，與小光角逐班上的一二名。羽山也喜歡小光，為了不讓日向一直靠近小光，因此常常提出問題刁難日向。"))
    
    elif event.message.text=="個人檔案":
        userid_list=worksheet.col_values(1)
        if event.source.user_id in userid_list:
            #玩家名稱
            user_id = event.source.user_id         
            profile = line_bot_api.get_profile(user_id)
            #從exccel取學分
            x=len(userid_list)
            list=[]
            for i in range(x):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list.append('B'+str(j))
            list.append('C'+str(j))
            #升級所需學分施工中
            #還沒選擇視角
            if worksheet.acell(list[1]).value=="0":
                confirm_template_message = TemplateSendMessage(
                alt_text='請選擇視角',
                template=ConfirmTemplate(
                text='選擇以日向（男主角）或是小光（女主角）的視角遊玩。',
                actions=[
                    MessageAction(
                        label='日向',
                        text='以日向的視角進行遊戲'
                    ),
                    MessageAction(
                        label='小光',
                        text='以小光的視角進行遊戲'
                    )
                ]
                )
                )
                line_bot_api.reply_message(event.reply_token,confirm_template_message)
            #日向視角
            elif worksheet.acell(list[1]).value=="1":
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="【輔仁大學學生證】"+"\n"+"姓名：日向"+"\n"+"目前學分數："+worksheet.acell(list[0]).value+"\n"+"還需很多學分升上二年級"))
            #小光視角
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="【輔仁大學學生證】"+"\n"+"姓名：小光"+"\n"+"目前學分數："+worksheet.acell(list[0]).value+"\n"+"還需很多學分升上二年級"))   
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="還沒開始遊戲喔，請輸入「開始遊戲」建立個人檔案。"))

    else:    
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="答錯了，想想看喔"))


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)