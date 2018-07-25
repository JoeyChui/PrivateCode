#-*-coding:utf-8-*-
#2017-10-27 JoeyChui sa517045@mail.ustc.edu.cn

import urllib, requests, xlrd, xlwt
from requests.exceptions import RequestException

def getOnePage(url, encoding = 'utf-8', header = {}, cookie = {}, json = False):
    try:
        response = requests.get(url, headers = header, cookies = cookie)
        if response.status_code == 200:
            response.encoding = encoding
            if json:
                return response.json()
            else:
                return response.text
        return None
    except RequestException:
        print('ER:getOnePage', url)
        return None

def getDouBanTVData():
    url = 'https://movie.douban.com/j/search_subjects?type=tv&tag=综艺&sort=time&page_limit=500&page_start=0'
    doubanTVData = getOnePage(url, json = True)['subjects']
    return doubanTVData

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
    print("write success!")
    return

def tvNameHander(tvName):
    if tvName == '':
        return "mriasdgadfgadfgadfadfg"
    if tvName[0] == '第':
        return tvName
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


file, wtFilename = 'IQiYiZY0.xls', '综艺好评榜candidates-20171216-20171229'

foundFlag = False
tvNameRate = []
tvNameList = readFromXLS(file)
print(tvNameList)
doubanTVData = getDouBanTVData()
print(doubanTVData)
for tvName in tvNameList:
    tvName = tvNameHander(tvName)
    for item in doubanTVData:
        if tvName in item['title']:
            tvNameRate.append([item['title'], float(item['rate']), item['url']])
            foundFlag = True
            break
    if foundFlag:
        print('   ', tvName)
        foundFlag = False
    else:
        print('Not Found', tvName)
print(len(tvNameRate))
writeToXLS(tvNameRate, wtFilename)
