#-*-coding:utf-8-*- 
#2017-9-15 JoeyChui sa517045@mail.ustc.edu.cn

import re, requests, json, xlwt
from requests.exceptions import RequestException
#from time import sleep

def getOnePage(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('ER:getOnePage')
        return None

def getTVDisCnt(url):
    html = getOnePage(url)
    item = re.findall(',"view_all_count":(\d+),"copyright', html)
    if item == []:
        return -1
    return int(item[0])

def getTVDetail(url):
    html = getOnePage(url)
    pattern = re.compile('figure_info">(.*?)</span>.*?strong class="figure_title"><a href="(https://v.qq.com/x/cover/\w+\.html).*?videos:title">(.*?)</a><.*?figure_desc" title="(.*?)">', re.S)
    items = re.findall(pattern, html)
    for item in items:
        tvDate = re.findall('(\d+)-(\d+)-(\d+)', item[0])
        tvDate = str(tvDate[0][0]) + str(tvDate[0][1]) + str(tvDate[0][2])
        print(item[2], item[3], tvDate)
        yield [item[2], item[3], int(tvDate), getTVDisCnt(item[1]), item[1], 'TencentVideo']

def writeToXLS(content, fileName):
    workbook = xlwt.Workbook(encoding='utf-8')
    booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)
    for i, rowVal in enumerate(content):
        for j, colVal in enumerate(rowVal):
            booksheet.write(i, j, colVal)
    workbook.save('%s.xls' % fileName)
    return

def crawlTencentVideoZY(offset):
    url = 'https://v.qq.com/x/list/variety?sort=5&offset=%s' % offset
    tvDetail = getTVDetail(url)
    writeToXLS(tvDetail, 'TencentVideoZY%s' % offset)

crawlTencentVideoZY(180) # 0 30 60
