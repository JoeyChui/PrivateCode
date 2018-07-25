#-*-coding:utf-8-*- 
#2017-9-10 JoeyChui sa517045@mail.ustc.edu.cn

import json, xlrd, xlwt, crawlWeiZS

def figureHotZTAvg(hotZT):
    sum = 0
    for item in hotZT:
        sum += item[1]
    return int(sum / len(hotZT))

def crawlWeiZSHotZT(header, keywords, sDate, eDate):
    weiZSHotZT = []
    for keyword in keywords:
        print('crawlWeiZSHotZT', keyword)
        hotZT = crawlWeiZS.getWeiZSHotZT(header, keyword, sDate, eDate)
        hotZTAvg = figureHotZTAvg(hotZT)
        weiZSHotZT.append([keyword, hotZTAvg])
    return weiZSHotZT

def figurePhaseReYiGrade(weiZSVaule, date1, date2):
    vauleSum = 0
    for item in weiZSVaule:
        if date1 <= item[0] <= date2:
            vauleSum =  vauleSum + int(item[1])
    return int(vauleSum / (date2 - date1 + 1) * 20)

def readFromXLS(file):
    xlsFile = xlrd.open_workbook(file)
    table = xlsFile.sheets()[0]
    tvNameList = table.col_values(0)
    return tvNameList

def writeToXLS(content, filename):
    workbook = xlwt.Workbook(encoding = 'utf-8')
    booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok = True)
    for i, rowVal in enumerate(content):
        for j, colVal in enumerate(rowVal):
            booksheet.write(i, j, colVal)
    workbook.save('%s.xls' % filename)
    return


header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36",
          "Referer": "http://data.weibo.com/index?sudaref=www.google.com"}
          #"Referer": "http://data.weibo.com/index/hotword?wid={}&wname={}".format(wid, keyword)
cookie = {"Cookie": 'SINAGLOBAL=375435575531.87726.1508677024809; WEB3=36fd7f9d6da16c76bfabd6ca14115b18; WBStorage=d0b15edc6ddab7a4|undefined; _s_tentry=www.baidu.com; UOR=www.baidu.com,data.weibo.com,www.baidu.com; Apache=6573048472319.707.1509071622692; ULV=1509071622703:3:3:3:6573048472319.707.1509071622692:1508764497348; PHPSESSID=qni7ev7g7gis7qots4abi0v9t6; open_div=close'}

file, wtFilename = 'DSJNameTemp.xls', 'DSJData'
sDate, eDate = "2017-10-01", "2017-10-27"

keywords = readFromXLS(file)
weiZSHotZTList = crawlWeiZSHotZT(header, keywords, sDate, eDate)
writeToXLS(weiZSHotZTList, wtFilename)
