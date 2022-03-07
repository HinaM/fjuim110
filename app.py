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
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已經開始遊戲，要重新開始請輸入「重置遊戲」"))
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
                alt_text='選擇視角',
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
            #ID已寫入且未選擇視角
            if worksheet.acell(list[0]).value=="0":
                worksheet.update(list[0],int(1))
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="選擇了日向視角！"))
            #ID已寫入建立且視角!=0
            elif worksheet.acell(list[0]).value=="1":
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已經選擇日向視角。"))
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已經選小光視角，要重置請輸入「重置遊戲」。"))
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
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="選擇了小光視角！"))
            #個人檔案已建立且視角!=0
            elif worksheet.acell(list[0]).value=="2":
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已經選小光視角。"))
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="已經選日向視角，要重置請輸入「重置遊戲」。"))
        #ID未寫入
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="還沒建立個人檔案喔，輸入「開始遊戲」建立。"))

    #文字施工中
    elif event.message.text=="遊戲規則":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="本遊戲是採用回答問題的遊玩方式進行闖關！！"+"\n"+"玩家回答出遊戲內關卡的問題，透過回答問題一步步解鎖劇情✨"+"\n"+"若是問題回答不出來時可以參考下面網站裡的解題技巧喔٩( 'ω' )و "+"\n\n"+"最後祝各位玩家遊玩愉快🥳"))
    
    elif event.message.text=="人物介紹":
        carousel_template_message = TemplateSendMessage(
            alt_text='人物介紹',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://upload.cc/i1/2022/03/06/TCXEeK.png',
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
                        thumbnail_image_url='https://upload.cc/i1/2022/03/06/LEFq8S.png',
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
                        thumbnail_image_url='https://upload.cc/i1/2022/03/03/8rgJCv.png',
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
                        thumbnail_image_url='https://upload.cc/i1/2022/03/03/UvGMpX.png',
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

    elif event.message.text=="重置遊戲":
        userid_list=worksheet.col_values(1)
        #已寫入ID
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            for i in range(66,76):
                list.append(chr(i)+str(j))
            #題目數量施工中
            #初始值設定
            for i in range(0,len(list)):
                worksheet.update(list[i],int(0))
            worksheet.update(list[2],int(1))
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
        #未寫入ID
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="還沒建立開始遊戲喔，請輸入「開始遊戲」建立個人檔案。"))
    elif event.message.text=="遊戲地圖":
        #圖片施工中
        LM=CarouselColumn(
                        thumbnail_image_url='http://www.management.fju.edu.tw/smarteditupfiles/lm1.jpg',
                        title='利瑪竇大樓',
                        text='成功解鎖利瑪竇大樓！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='利瑪竇大樓介紹'
                            )
                        ]
                    )
        ZM=CarouselColumn(
                        thumbnail_image_url='https://upload.cc/i1/2022/03/06/TCXEeK.png',
                        title='中美堂',
                        text='成功解鎖中美堂！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='中美堂介紹'
                            )
                        ]
                    )
        SF=CarouselColumn(
                        thumbnail_image_url='https://upload.cc/i1/2022/03/06/TCXEeK.png',
                        title='聖言樓',
                        text='成功解鎖聖言樓！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='聖言樓介紹'
                            )
                        ]
                    )
        JZ=CarouselColumn(
                        thumbnail_image_url='https://upload.cc/i1/2022/03/06/TCXEeK.png',
                        title='靜心堂',
                        text='成功解鎖靜心堂！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='靜心堂介紹'
                            )
                        ]
                    )
        YS=CarouselColumn(
                        thumbnail_image_url='https://upload.cc/i1/2022/03/06/TCXEeK.png',
                        title='野聲樓',
                        text='成功解鎖野聲樓！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='野聲樓介紹'
                            )
                        ]
                    )
        JS=CarouselColumn(
                        thumbnail_image_url='https://upload.cc/i1/2022/03/06/TCXEeK.png',
                        title='濟時樓',
                        text='成功解鎖濟時樓！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='濟時樓介紹'
                            )
                        ]
                    )
        BS=CarouselColumn(
                        thumbnail_image_url='https://upload.cc/i1/2022/03/06/TCXEeK.png',
                        title='伯達樓',
                        text='成功解鎖伯達樓！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='伯達樓介紹'
                            )
                        ]
                    )
        ES=CarouselColumn(
                        thumbnail_image_url='https://upload.cc/i1/2022/03/06/TCXEeK.png',
                        title='進修部大樓',
                        text='成功解鎖進修部大樓！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='進修部大樓介紹'
                            )
                        ]
                    )
        carousel_template_message1 = TemplateSendMessage(
            alt_text='遊戲地圖',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='http://www.management.fju.edu.tw/smarteditupfiles/lm1.jpg',
                        title='利瑪竇大樓',
                        text='成功解鎖利瑪竇大樓！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='利瑪竇大樓介紹'
                            )
                        ]
                    )
                ]
            )
        )
        carousel_template_message2 = TemplateSendMessage(
            alt_text='遊戲地圖',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='http://www.management.fju.edu.tw/smarteditupfiles/lm1.jpg',
                        title='利瑪竇大樓',
                        text='成功解鎖利瑪竇大樓！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='利瑪竇大樓介紹'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://www.fju.edu.tw/showImg/focus/focus1435.jpg',
                        title='中美堂',
                        text='成功解鎖中美堂！',
                        actions=[
                            MessageAction(
                                label='建築介紹',
                                text='中美堂介紹'
                            )
                        ]
                    )
                ]
            )
        )
        #施工中
        if event.source.user_id in userid_list:
            for i in range(len(userid_list)):
                if userid_list[i]==event.source.user_id:
                    j=i+1
            list=[]
            list.append('B'+str(j))
            if worksheet.acell(list[0]).value=="0":
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="還沒解鎖任何建築！趕快去回答問題解鎖吧！"))
            elif worksheet.acell(list[0]).value=="1":
                line_bot_api.reply_message(event.reply_token,carousel_template_message1)
            else:
                line_bot_api.reply_message(event.reply_token,carousel_template_message2)
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="還沒建立個人檔案喔，輸入「開始遊戲」建立。"))
    elif event.message.text=="利瑪竇大樓介紹":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="利瑪竇大樓為法管學院綜合大樓，呈現「T」字形，於1986年落成，為紀念來華傳教的耶穌會會是利瑪竇神父，特意以其姓名命名，在利瑪竇大樓的前庭、後廳大理石地板，還鑲嵌著輔仁校訓「真善美聖」的拉丁文。利瑪竇為天主教在中國傳教的開拓者之一，除了傳播天主教福音之外，他還結交許多中國官員，教導天文、數學、地理等西方科學知識，因而獲得「泰西儒士」的尊稱。《坤輿萬國全圖》則是利瑪竇為中國所製作的世界地圖，問世後不久即被傳入日本，對於亞洲地理學的發展產生重要影響。"))
    elif event.message.text=="中美堂介紹":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="中美堂是學校體育館，屬於大型活動的集會場所，由聖言會會士、德國人林慎白總建築師，及我國專家陳濯、李實鐸、沈大魁、趙楓等四位合作規劃而成，象徵古羅馬競技精神的圓形建築，遠看狀似北平天壇，取前總統蔣中正以及前董事長蔣宋美齡名字各一字，簡稱中美堂。"))
    elif event.message.text=="聖言樓介紹":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="代號SF，主要科系為電子系與資工系，而資管系的資料結構、網路設計課程安排在此棟建築物授課。地下室具有敦煌書局，內部除了各大科系的教科書、文具以外，還具備蘋果專區和餐廳，相當便利。"))
    elif event.message.text=="靜心堂介紹":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="淨心堂位於外語學院跟法管學院之間，圓環的旁邊喔。於民國66年落成，整體外觀為白色，乃前任校長羅光總主教選定的顏色，代表純潔肅穆莊嚴。在建築風格上非常特別，結合了科學、藝術、宗教等等，可以在外觀上找到字母Α和字母Ω。"))
    elif event.message.text=="野聲樓介紹":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="野聲樓為輔大的行政中心，所有行政辦公室都設置在此處，包含校長室秘書室、人事室、會計室、會議室、註冊組、教務處、課務組、軍訓室、公共事務室、生活輔導組、出納組，谷欣廳⋯⋯等等；此外，在野聲樓四樓設有中國天主教文物館、校史館、于斌樞機紀念館，可供民眾預約參觀，以便更了解輔仁大學的歷史背景。「野聲」取自輔大第一任校長于斌樞機主教的字號，源於聖經中聖洗者若翰曠「野」的呼「聲」，有趣的是，在野聲樓外頭也豎立著于斌樞機主教的雕像，和野聲樓相映對照，透過此空間規劃間接說明輔大創建的校史。"))
    elif event.message.text=="濟時樓介紹":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="濟時樓圖書總館館舍總面積約3500坪，閱覽席位1062席、全館無線網路(SSID FJU)、學習共享空間與檢索查詢之電腦設備92組、研究小間28間、團體討論室7間。二樓為圖書館入口、借閱櫃台、參考服務區、資訊檢索區、指定參考書區、新書展示區、學習共享空間、寫作中心及閱報區；三樓為現期期刊區、學位論文區及參考書區；四樓為期刊室（含合訂本報紙）；五至七樓為中西文書庫；八樓為辦公室。"))
    elif event.message.text=="伯達樓介紹":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="代號BS，所屬科系為社會科學系、法律學系，資管系的資料庫管理和作業系統課程也在此授課。建築意義：愛護真理、保護青年的張伯達神父（1905-1951致命殉道），他常說：現代青年該具有團結、合作、謙虛、仁恕、急公、好義等社會道德，還要有創造力。這樣，一旦跨出校門，不但能夠適應社會，在社會中生存，更能領導社會，改造社會，做社會中堅份子。"))
    elif event.message.text=="進修部大樓介紹":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輔大進修部的前身是輔大夜間部，自民國五十八年成立迄今已五十餘年。秉持天主教的辦學理念與宗旨，以全人教育為目標；秉持真、善、美、聖的校訓，提供一個終生學習的環境，為社會國家造就許多人才。"+"\n"+"本部下轄8個學系及10個學士學位學程，致力培養學生具備廣博的知識及精進的專業能力，並培育學生具有人文素養、人本情懷、人際溝通與思惟判斷能力之完備的社會人。"))
    else:    
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)