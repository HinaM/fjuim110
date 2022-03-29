from fileinput import filename
import gspread
gc=gspread.service_account(filename='fjuim-340916-7e527f907c19.json')
sh=gc.open_by_key('1LozvTUSglnM_TtYO1tyDROkFkpX4lrlaVD1tC0911XM')
worksheet=sh.sheet1

res=worksheet.get_all_records()


userid_list=worksheet.col_values(1)

x=len(userid_list)
for i in range(0,x):
    if userid_list[i]=='Ud184a816c79cdc37caaf18bc97051cec':
        i+=1

print(i)
list=[]
for x in range(65,91):
    list.append(chr(x)+str(i))
for y in range(65,67):    
    for x in range(65,91):
        list.append(chr(y)+chr(x)+str(i))
for x in range(65,71):
    list.append("C"+chr(x)+str(i))
print(list)
print(len(list))
