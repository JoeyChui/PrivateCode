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

def getTVID(url):
    html = getOnePage(url)
    pattern = re.compile('ata-qidanadd-sourceid="(\d+).*?ass="icon-vInfo">(.*?)</span>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        sourceID, tvDate = item
        tvDate = re.findall('(\d+)-(\d+)-(\d+)', tvDate)
        tvMonth = tvDate[0][0] + tvDate[0][1]
        yield [int(sourceID), int(tvMonth)]

def getTVDisCnt(tvID):
    url = 'http://cache.video.iqiyi.com/jp/pc/%s/' % tvID
    html = getOnePage(url)
    tvDisCnt = re.findall('{"\d+":(\d+)}', html)[0]
    return int(tvDisCnt)

def geTVDetail(sourceID, tvMonth):
    url = 'http://cache.video.iqiyi.com/jp/sdvlst/latest?key=sdvlist&categoryId=6&sourceId={}&tvYear={}'.format(sourceID, tvMonth)
    print(url)
    html = getOnePage(url)
    pattern = re.compile('tvYear":"([-\d]+)".*?tvId":(\d+).*?score":([\.\d]+).*?videoName":"(.*?)".*?sName":"(.*?)".*?vUrl":"(http://www.iqiyi.com/v_\w+\.html)"', re.S)
    items = re.findall(pattern, html)
    for item in items:
        tvDate = re.findall('(\d+)-(\d+)-(\d+)', item[0])
        tvDate = tvDate[0][0] + tvDate[0][1] + tvDate[0][2]
        yield [item[4], item[3], int(tvDate), getTVDisCnt(item[1]), int(item[1]), item[5], 'IQiYi']

def writeToXLS(content, fileName):
    workbook = xlwt.Workbook(encoding='utf-8')
    booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)
    for i, rowVal in enumerate(content):
        for j, colVal in enumerate(rowVal):
            booksheet.write(i, j, colVal)
    workbook.save('%s.xls' % fileName)
    return

def crawlIQiYiZY(page):
    SEEDURL = 'http://list.iqiyi.com/www/6/-------------4-%s-1---.html' % page # 按更新时间排序 全网
    tvIDMonth = getTVID(SEEDURL)
    print('OK@getTVID')
    tvList = []
    for item in tvIDMonth:
        tvDetail = geTVDetail(item[0], item[1])
        for ele in tvDetail:
            tvList.append(ele)
    writeToXLS(tvList, 'IQiYiZY%s' % page)


crawlIQiYiZY(16) # start from 0
