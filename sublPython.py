import requests
import json
import xlrd, xlwt, csv

def rdXLSTableByRow(file, sheetNum = 0, firstRowFlag = True, printFlag = True, info = '', returnDictListFlag = False):
    file = str(file)
    if file[-4:] != ".xlsx":
        file += ".xlsx"
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

def getDpShopId(url):
    result = getOnePage(url)
    if result is None:
        return "getDpShopId None"
    print("*******" + result)
    result = json.loads(result)
    if len(result) == 0:
        return ""
    return result['dpShopId']

url = "http://10.76.190.163:8080/match/matchOneShop?shopName={}&branch={}&city={}"
shopName = ""
branch = ""
city = ""

resultList = [["原店名", "原分店名", "dpShopId", "点评链接"]]
bigtable = rdXLSTableByRow("/Users/joeychui/GitHub/PrivateCode/temp")[3:]
for item in bigtable:
    shopName, branch = item[1], item[2]
    try:
        dpShopId = getDpShopId(url.format(shopName, branch, city))
    except:
        dpShopId = ""
    
    resultList.append([shopName, branch, dpShopId, "http://www.dianping.com/shop/" + dpShopId])
    print([shopName, branch, dpShopId])
    wtToXLS(resultList, "匹配结果")
    # wtToCSV(resultList, "匹配结果")
