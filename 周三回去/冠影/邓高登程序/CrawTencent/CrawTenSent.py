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
    tvDisCnt = re.findall(',"view_all_count":(\d+),"movie_c', html)[0]
    return int(tvDisCnt)

def getTVDetail(html):
    tvDetail = []
    pattern = re.compile('a href="(https://v.qq.com/x/cover/\w+\.html).*?videos-vert:title">(.*?)</a>', re.S)
    items = re.findall(pattern, html)
    print('match number is', len(items))
    for item in items:
        print([item[1]])
        tvDetail.append([item[1], getTVDisCnt(item[0]), item[0], 'TencentVideo'])
    return tvDetail

def writeToXLS(content, fileName):
    workbook = xlwt.Workbook(encoding='utf-8')
    booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)
    for i, rowVal in enumerate(content):
        for j, colVal in enumerate(rowVal):
            booksheet.write(i, j, colVal)
    workbook.save('%s.xls' % fileName)
    return

def crawlTencentVideoDSJ(minOffset, maxOffset):
    allTVDetail = []
    for ii in range(minOffset, maxOffset, 30):
        seedURL = 'http://v.qq.com/x/list/tv?sort=19&iarea=814&offset=%s' % ii
        html = getOnePage(seedURL)
        tvDetail = getTVDetail(html)
        for item in tvDetail:
            allTVDetail.append(item)
    writeToXLS(allTVDetail, 'TencentVideoDSJ')
    print('all match number is', len(allTVDetail))

minOffset, maxOffset = 0, 300
crawlTencentVideoDSJ(minOffset, maxOffset)
