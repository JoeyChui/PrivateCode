
import xlrd, xlwt

def rdXLSTableByRow(file, sheetNum = 0, firstRowFlag = True, printFlag = True, info = '', returnDictListFlag = False):
    file = str(file)
    if file[-4:] != ".xls":
        file += ".xls"
    xlsFile = xlrd.open_workbook(file)
    sheet = xlsFile.sheets()[sheetNum]
    biglist = []
    if returnDictListFlag:
        title = sheet.row_values(0)
        titleLen = len(title)
        info = "title:" + str(title)
    else:
        if firstRowFlag:
            biglist.append(sheet.row_values(0))
    for ii in range(1, sheet.nrows):
        row = sheet.row_values(ii)
        if row != []:
            if returnDictListFlag:
                rowDcit = {}
                for j in range(titleLen):
                    rowDcit[title[j]] = row[j]
                row = rowDcit
            biglist.append(row)
    if printFlag:
        if info != '':
            info = ' ' + info
        print("read successfully:" + file + info)
    return biglist

def wtToXLS(biglist, file, sheetName = 'Sheet1', printFlag = True, info = ''):
    workbook = xlwt.Workbook(encoding = 'utf-8')
    booksheet = workbook.add_sheet(sheetName, cell_overwrite_ok = True)
    for i, rowVal in enumerate(biglist):
        for j, colVal in enumerate(rowVal):
            booksheet.write(i, j, colVal)
    file = str(file)
    if file[-4:] != ".xls":
        file += ".xls"
    workbook.save(file)
    if printFlag:
        if info != '':
            info = ' ' + info
        print("write successfully:" + file + info)
    return

def mergeList(a, b):
    for ele in b:
        a.append(ele)
    return a


'''
tables = []
for count in range(1):
    file = "IQIQiYiZY{}.xls".format(count)
    table = rdXLSTableByRow(file)
    mergeList(tables, table)
print("tables")
'''
file = "综艺好评榜candidates-20171216-20171229.xls"
table = rdXLSTableByRow(file)
print(table)
