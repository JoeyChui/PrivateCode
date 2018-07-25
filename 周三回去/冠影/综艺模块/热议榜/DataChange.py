
import urllib, requests, xlwt
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

def keywordJudge(header, keyword):
    url = "http://data.weibo.com/index/ajax/hotword?word={}&flag=nolike&_t=0".format(keyword)
    request = getOnePage(url, header = header, json = True)
    if request['code'] != '100000':
        print('ER:{}'.format(keyword))
    return #'OK:{}'.format(keyword)

def getWID(header, keyword):
    url = "http://data.weibo.com/index/ajax/hotword?word={}&flag=nolike&_t=0".format(keyword)
    request = getOnePage(url, header = header, json = True)
    if request['code'] != '100000':
        print('ER:{}'.format(keyword))
        return
    return request['data']['id']

def getWeiZSHotZT(header, keyword, sDate, eDate):
    keyword = urllib.parse.quote(keyword)
    wid = getWID(header, keyword)
    url = "http://data.weibo.com/index/ajax/getchartdata?wid={}&sdate={}&edate={}".format(wid, "2017-10-01", "2017-10-27")
    hotOriginal = getOnePage(url, header = header, json = True)
    hotZT, hotZTOriginal = [], hotOriginal['zt']
    if hotZTOriginal == False:
        return []
    for ii in range(len(hotZTOriginal)-1):
        day_key = int(hotZTOriginal[ii]['day_key'].replace('-',''))
        value = int(hotZTOriginal[ii]['value'])
        hotZT.append([day_key, value])
    return hotZT

def getWeiZSRegionInfo(header, cookie, keyword):
    keyword = urllib.parse.quote(keyword)
    url_regionInfo = 'http://data.weibo.com/index/ajax/keywordzone?type=default'
    regionInfo = getOnePage(url_regionInfo, header = header, cookie = cookie, json = True)
    url_provinceCompare = 'http://data.weibo.com/index/ajax/getprovincecompare'
    provinceCompare = getOnePage(url_provinceCompare, header = header, cookie = cookie)
    return regionInfo, provinceCompare

def getWeiZSAttribute(header, cookie, keyword):
    keyword = urllib.parse.quote(keyword)
    url = 'http://data.weibo.com/index/ajax/getdefaultattributealldata'
    attributeAllDate = getOnePage(url, header = header, cookie = cookie, json = True)
    return attributeAllDate

def writeToXLS(content, filename):
    workbook = xlwt.Workbook(encoding = 'utf-8')
    booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok = True)
    for i, rowVal in enumerate(content):
        for j, colVal in enumerate(rowVal):
            booksheet.write(i, j, colVal)
    workbook.save('%s.xls' % filename)
    return

def writeToTXT(content, filename):
    with open('%s.txt' % filename, 'w', encoding = 'utf-8') as f:
        f.write(content)
        f.close()
    return


header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36",
          "Referer": "http://data.weibo.com/index?sudaref=www.google.com"}
          #"Referer": "http://data.weibo.com/index/hotword?wid={}&wname={}".format(wid, keyword)
cookie = {"Cookie": 'SINAGLOBAL=375435575531.87726.1508677024809; WEB3=36fd7f9d6da16c76bfabd6ca14115b18; WBStorage=d0b15edc6ddab7a4|undefined; _s_tentry=www.baidu.com; UOR=www.baidu.com,data.weibo.com,www.baidu.com; Apache=6573048472319.707.1509071622692; ULV=1509071622703:3:3:3:6573048472319.707.1509071622692:1508764497348; PHPSESSID=qni7ev7g7gis7qots4abi0v9t6; open_div=close'}

sDate, eDate = "2017-10-01", "2017-10-27"

