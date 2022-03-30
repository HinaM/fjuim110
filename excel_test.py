from fileinput import filename
import gspread
gc=gspread.service_account(filename='fjuim-340916-7e527f907c19.json')
sh=gc.open_by_key('1LozvTUSglnM_TtYO1tyDROkFkpX4lrlaVD1tC0911XM')
worksheet=sh.sheet1

res=worksheet.get_all_records()


userid_list=worksheet.col_values(1)

user=worksheet.row_values(3)
print(user)
#worksheet.delete_row(3)
if 'Ud184a816c79cdc37caaf18bc97051cec' in userid_list:
    for i in range(len(userid_list)):
        if userid_list[i]=='Ud184a816c79cdc37caaf18bc97051cec':
            j=i+1
list=[]
list.append("E"+str(j))
list.append("F"+str(j))
list.append("AY"+str(j))           
if 'Ud184a816c79cdc37caaf18bc97051cec' in userid_list and worksheet.acell(list[0]).value=='1':
    worksheet.update_acell(list[0],int(2))
    worksheet.update_acell(list[1],int(1))
    worksheet.update_acell(list[2],int(0))
    print('True')
else:
    print('False')
