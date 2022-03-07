from fileinput import filename
import gspread
gc=gspread.service_account(filename='fjuim-340916-7e527f907c19.json')
sh=gc.open_by_key('1LozvTUSglnM_TtYO1tyDROkFkpX4lrlaVD1tC0911XM')
worksheet=sh.sheet1

res=worksheet.get_all_records()
print(res)

userid_list=worksheet.col_values(1)
print(userid_list)
'''
list_c=[]
for i in range(69,76):
    list_c.append(chr(i)+str(2))

for i in range(len(list_c)):
    if worksheet.acell(list_c[i]).value=="1":
        print(ord(list_c[i][0])-68)
'''
if 'Ud184a816c79cdc37caaf18bc97051cec' in userid_list:
    list_c=[]
    for i in range(69,76):
        list_c.append(chr(i)+str(2))
    for i in range(len(list_c)):
        if worksheet.acell(list_c[i]).value=="1":
            ques=ord(list_c[i][0])-68
print(type(ques))
print(worksheet.acell("C2").value)