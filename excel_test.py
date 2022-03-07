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
    list.append('B'+str(j))
print(worksheet.acell(list[0]).value=="0")