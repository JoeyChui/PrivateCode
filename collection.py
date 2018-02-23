#-*-coding:utf-8-*-
#2017-11-08 JoeyChui sa517045@mail.ustc.edu.cn

import csv, os, xlrd, xlwt

def getOnePage(url, encoding = 'UTF-8', headers = {}, cookies = {}, json = False):
    try:
        response = requests.get(url, headers = headers, cookies = cookies)
        response.encoding = encoding
        if response.status_code != 200:
            print("ER:getOnePage", "status_code is " + str(response.status_code), url)
            return None
        if json:
            return response.json()
        return response.text
    except RequestException:
        print("ER:getOnePage", url)
        return None

def reHTML(patternStr, html, first = False, function = None, functionArguments = ()):
    pattern = re.compile(patternStr, re.S)
    items = re.findall(pattern, html)
    if items == []:
        return '' if first else []
    for ii in range(len(items)):
        if type(items[ii]) == tuple:
            itemStrip = []
            for ele in items[ii]:
                itemStrip.append(str(ele).strip())
            items[ii] = itemStrip
        else:
            items[ii] = str(items[ii]).strip()
    if first:
        return items[0]
    if function != None:
        return function(items, functionArguments)
    return items

def mergeList(a, b):
    for ele in b:
        a.append(ele)
    return a

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

# html = str(html["data"]).encode('utf-8').decode('unicode_escape')

#files = os.listdir("C:\\Users\\Joey\\Desktop\\zhengwuwb\\AccountAllData")
#for file in files:
#    print(file)


def wtToCSV(biglist, file, printFlag = True, info = ''):
    with open(file, 'w', newline = '') as csvFile:
        csvFile.write(codecs.BOM_UTF8)
        writer = csv.writer(csvFile, dialect = 'excel')
        for row in biglist:
            writer.writerow(row)
        file = str(file)
        if file[-4:] != ".csv":
            file += ".csv"
        if printFlag:
            if info != '':
                info = ' ' + info
            print("write successfully:" + file + info)
        return

#    except Exception as e:
#        print("Write an CSV file to path: %s, Case: %s" % (file, e))

def rdCSVTableByRow(file, firstRowFlag = True, printFlag = True, info = ''):
    file = str(file)
    if file[-4:] != ".csv":
        file += ".csv"
    with open(file,'r') as csvFile:
        lines = csv.reader(csvFile)
        biglist = []
        for row in lines:
            if row != []:
                biglist.append(row)
    if not firstRowFlag:
        biglist = biglist[1:]
    if printFlag:
        if info != '':
            info = ' ' + info
        print("read successfully:" + file + info)
    return biglist


