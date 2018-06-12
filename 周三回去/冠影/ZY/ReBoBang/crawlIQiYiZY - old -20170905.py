#-*-coding:utf-8-*- 
#2017-9-10 JoeyChui sa517045@mail.ustc.edu.cn

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

def getSourceURL(url):
    sourceURL = []
    html = getOnePage(url)
    items = re.findall('http://www.iqiyi.com/(v_\w+).html', html)
    for item in items:
        url = 'http://www.iqiyi.com/{}.html'.format(item)
        if url not in sourceURL:
            sourceURL.append(url)
    return sourceURL

def getIDDate(url):
    try:
        html = getOnePage(url)
        pattern = re.compile('tvId:(\d+).*?sourceId:(\d+).*?tvYear:(\d+)', re.S)
        tvID, sourceID, tvYear = re.findall(pattern, html)[0]
        wallID = re.findall('wallId:\'(\d+)', html)[0]
        return sourceID, tvID, wallID, tvYear
    except:
        return -1, -1, -1, -1

def getTVAllYear(sourceID):
    url = 'http://cache.video.iqiyi.com/jp/sdlst/6/{}/'.format(sourceID)
    html = getOnePage(url)
    #item = re.findall('=({.*?})', html)[0]
    item = html[html.find('{'):]
    data = eval(item)
    if 'data' in data:
        return(data['data'])
    return {}

def getStrTVYearMoth(tvAllYear):
    strTVYearMoth = ''
    for tvOneYear in tvAllYear:
        for tvOneMonth in tvAllYear[tvOneYear]:
            tvYearMonth = str(tvOneYear) + str(tvOneMonth)
            strTVYearMoth = strTVYearMoth + '&tvYear={}'.format(tvYearMonth)
    return strTVYearMoth

def getTVDisCnt(tvID):
    url = 'http://cache.video.iqiyi.com/jp/pc/{}/'.format(tvID)
    html = getOnePage(url)
    tvDisCnt = re.findall('{"\d+":(\d+)}', html)[0]
    return tvDisCnt

def getFeedCount(wallID):
    try:
        url = 'http://paopao.iqiyi.com/apis/e/starwall/basic_wall.action?authcookie=&device_id=pc_web&agenttype=118&wallId={}&atoken=8ffffbc44F3tKBShRo5tC9Bm1J5k01EeIqm1jnhIKXLdVMRB2m11Ctom4'.format(wallID)
        html = getOnePage(url)
        feedCount = re.findall('feedCount":(\d+)', html)[0]
        return feedCount
    except:
        return -1

def geTVDetail(sourceID, tvYear, wallID):
    #&tvYear=201611&tvYear=201612&tvYear=201701&tvYear=201702
    url = 'http://cache.video.iqiyi.com/jp/sdvlst/latest?key=sdvlist&categoryId=6&sourceId={}&tvYear={}'.format(sourceID, tvYear)
    print(url)
    html = getOnePage(url)
    pattern = re.compile('tvYear":"([\w-]+).*?tvId":(\d+).*?score":([\d\.]+).*?videoName":"(.*?)".*?sName":"(.*?)".*?vUrl":"(.*?)"', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
                'sourceID' : sourceID,
                'tvID' : item[1],
                'sName' : item[4],
                'vName' : item[3],
                'tvYear' : item[0],
                'score' : item[2],
                'displayCount' : getTVDisCnt(item[1]),
                'feedCount' : getFeedCount(wallID),
                'vURL' : item[5]
            }

def writeToTXT(content, fileName):
    with open('%s.txt' % fileName, 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()
    return
def writeToXLS(content, fileName):
    workbook = xlwt.Workbook(encoding='utf-8')
    booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)
    for i, rowVal in enumerate(content):
        for j, colVal in enumerate(rowVal):
            booksheet.write(i, j, colVal)
    workbook.save('%s.xls' % fileName)
    return

def judgeMonth(tvYear, startMonth):
    if int(tvYear) == startMonth:
        return True
    return False


startMonth = 201709 # 设定爬取月份
#seedURL = 'http://www.iqiyi.com/zongyi/' #爱奇艺 综艺主页
#seedURL = 'http://list.iqiyi.com/www/6/-------------4-1-1-iqiyi--.html' # 按更新时间排序 爱奇艺
seedURL = 'http://list.iqiyi.com/www/6/-------------4-1-1---.html' # 按更新时间排序 全网
print(seedURL)
toCrawlSourceURL = []
crawledSourceURL = []

toCrawlSourceURL = getSourceURL(seedURL)
print('OK:getSourceURL', len(toCrawlSourceURL))

counter = 0
while True:
    if toCrawlSourceURL == []:
        print('toCrawlSourceURL is [].', counter)
        break
    crawlingURL = toCrawlSourceURL.pop()
    sourceID, tvID, wallID, tvYear = getIDDate(crawlingURL)
    print(sourceID)
    #tvAllYear = getTVAllYear(sourceID)
    if judgeMonth(tvYear, startMonth):
        tvDetails = geTVDetail(sourceID, tvYear, wallID)
        for item in tvDetails:
            writeToTXT(item, 'iqiyitxt')
            counter += 1
            print( 'OK:', tvID, tvYear)
        writeToXLS(tvDetails, 'iqiyi')
    crawledSourceURL.append(crawlingURL)
