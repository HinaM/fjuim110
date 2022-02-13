from fileinput import filename
import gspread
gc=gspread.service_account(filename='fjuim-340916-7e527f907c19.json')
sh=gc.open_by_key('1LozvTUSglnM_TtYO1tyDROkFkpX4lrlaVD1tC0911XM')
worksheet=sh.sheet1

res=worksheet.get_all_records()
print(res)

userid_list=worksheet.col_values(1)
print(userid_list)

x=len(userid_list)
list=[]
for i in range(65,76):
    list.append(chr(i)+str(x+1))
#ID
worksheet.update(list[0],"Ud184a816c79cdc37caaf18bc97051cec")
#初始值設定
for i in range(1,len(list)):
    worksheet.update(list[i],int(0))
print("成功")