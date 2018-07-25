import requests, re
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

# ['里食真', '联合路店', '27206953', 'http://www.dianping.com/shop/27206953']
bigTable = rdXLSTableByRow("匹配结果 copy", firstRowFlag = False)
bigList = [["原店名", "原分店名", "点评店名", "dpShopId", "点评链接"]]
for item in bigTable:
    url = item[3]
    if len(url) > 29:
        html = getOnePage(url)
        dpShopName = reHTML("class=\"shop-name\">(.*?)<a", html, first = True)
    else:
        dpShopName = ""
    bigList.append([item[0], item[1], dpShopName, item[2], item[3]])
    wtToXLS(bigList, "最终匹配结果")
    print([item[0], item[1], dpShopName, item[2], item[3]])


