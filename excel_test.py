from fileinput import filename
import gspread
gc=gspread.service_account(filename='fjuim-340916-7e527f907c19.json')
sh=gc.open_by_key('1LozvTUSglnM_TtYO1tyDROkFkpX4lrlaVD1tC0911XM')
worksheet=sh.sheet1

res=worksheet.get_all_records()
print(res)

userid_list=worksheet.col_values(1)
print(userid_list)

if "Ud184a816c79cdc37caaf18bc97051cec" in userid_list:
    for i in range(len(userid_list)):
        if userid_list[i]=="Ud184a816c79cdc37caaf18bc97051cec":
            j=i+1
            list=[]
            list.append('C'+str(j))
            #ID已寫入且已選擇視角
            if worksheet.acell(list[0]).value=="0":
                worksheet.update(list[0],int(1))
                print("j06t/6")
            #個人檔案已建立且視角!=0
            else:
                print("j06t")