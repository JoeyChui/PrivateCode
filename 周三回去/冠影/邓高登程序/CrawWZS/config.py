import xlrd
import openpyxl


keywords = []
wb =openpyxl.load_workbook('rank.xlsx')
ws = wb.active

for row in ws.rows:
        data = str(row[0].value)
        if (data == None):
            data = "0"
        keywords.append(data)

print(keywords)

