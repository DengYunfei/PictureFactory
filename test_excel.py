import openpyxl

wb = openpyxl.load_workbook('产品详单_202004.xlsx')
# print(wb.get_sheet_names())
sheet = wb['总表']
# for sheet_name in wb.get_sheet_names():
#     sheet = wb[sheet_name]
#     sheets.append(sheet)
my_dict = []
my_user = {}
count = 0
for row in sheet.iter_rows():
    if count == 0:
        continue
    print(len(row))
    for cell in row:

        # my_user[row[0]] = cell.value

        count += 1
print(my_dict)
