
import json, xlrd, xlwt, crawlWeiZS


def tvNameHander(tvName):
    if tvName == '':
        return "mriasdgadfgadfgadfadfg"
    if tvName[0] == '第':
        return tvName
    if '（' in tvName:
        tvName = tvName[:tvName.find('（')]
    if '(' in tvName:
        tvName = tvName[:tvName.find('(')]
    if ' ' in tvName:
        tvName = tvName[:tvName.find(' ')]
    if '第' in tvName:
        tvName = tvName[:tvName.find('第')]
    if '：' in tvName:
        tvName = tvName[:tvName.find('：')]
    while tvName[-1].isdigit():
        tvName = tvName[:-1]
    return tvName

def readFromXLS(file):
    xlsFile = xlrd.open_workbook(file)
    table = xlsFile.sheets()[0]
    tvNameList = table.col_values(0)
    return tvNameList

def dataHander(dataList):
    sum = 0
    for ele in dataList:
        sum += ele[1]
    return sum

def writeToXLS(content, filename):
    workbook = xlwt.Workbook(encoding = 'utf-8')
    booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok = True)
    for i, rowVal in enumerate(content):
        for j, colVal in enumerate(rowVal):
            booksheet.write(i, j, colVal)
    workbook.save('%s.xls' % filename)
    print("write S!")
    return


header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36",
          "Referer": "http://data.weibo.com/index?sudaref=www.google.com"}
          #"Referer": "http://data.weibo.com/index/hotword?wid={}&wname={}".format(wid, keyword)
#cookie = {"Cookie": 'SINAGLOBAL=9593676043677.764.1512397399492; SCF=Aq7YX9XtP9dpcKHI5mhPhhh0lHvVJ-oZtNdj1soOvY2j6keICzB0pwgv0jS2yZaePItCRqfMPiT2ecRsOOL4t8k.; SUHB=0h150JzumyJkzk; ALF=1544001250; SUB=_2AkMtGD09f8NxqwJRmPEWyWrqa4l0zw3EieKbRMzmJRMxHRl-yT9kqkgLtRB6BpgQPAqirEDVY709sspAfDkeK1bbeitk; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WhKMK7JPLUUvlvAyubBex1v; WEB3=16eecaac1b039ffa98ceae90acb175f9; WBStorage=c1cc464166ad44dc|undefined; _s_tentry=www.baidu.com; UOR=www.baidu.com,bang.weibo.com,www.baidu.com; Apache=2150166840655.1433.1514610546674; ULV=1514610546684:5:5:2:2150166840655.1433.1514610546674:1514451428930; PHPSESSID=5negdul8714ndu2o8209qk39i3'}

file, wtFilename = '活頁簿1.xlsx', '综艺热议榜-20171216-20171229'
sDate, eDate = "2017-12-24", "2017-12-30"

keywords = []
tvNameList = readFromXLS(file)
for ii in range(len(tvNameList[1:400])):
    tvNameList[ii] = tvNameHander(tvNameList[ii])
    if not tvNameList[ii] in keywords:
        keywords.append(tvNameList[ii])
print(keywords, len(keywords))

bigList = [["name", "zhishu"]]
trueKeywords = []
falseKeywords = []
for ii in range(len(keywords)):

    if crawlWeiZS.keywordJudge(header, keywords[ii]):
        trueKeywords.append(keywords[ii])
        print(keywords[ii])

#        hotZT = crawlWeiZS.getWeiZSHotZT(header, keywords[ii], sDate, eDate)
#        zhishu = dataHander(hotZT)
#        print(hotZT, zhishu)

    else:
        falseKeywords.append(keywords[ii])

#print(falseKeywords, len(falseKeywords))
#print(trueKeywords, len(trueKeywords))

for keyword in trueKeywords:
    hotZT = crawlWeiZS.getWeiZSHotZT(header, keyword, sDate, eDate)
    zhishu = dataHander(hotZT)
    bigList.append([keyword, zhishu])
    print(hotZT, zhishu)

writeToXLS(bigList, "sdsrfsdf")


