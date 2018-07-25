#-*-coding:utf-8-*- 
#2017-9-10 JoeyChui sa517045@mail.ustc.edu.cn


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
        #print('ER:{}'.format(keyword))
        return False
    return True #'OK:{}'.format(keyword)

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
    url = "http://data.weibo.com/index/ajax/getchartdata?wid={}&sdate={}&edate={}".format(wid, sDate, eDate)
    hotOriginal = getOnePage(url, header = header, json = True)
    hotZT, hotZTOriginal = [], hotOriginal['zt']
    #print('2345678',keyword, hotZTOriginal)
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

'''
header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36",
          "Referer": "http://data.weibo.com/index?sudaref=www.google.com"}
          #"Referer": "http://data.weibo.com/index/hotword?wid={}&wname={}".format(wid, keyword)
cookie = {"Cookie": 'SINAGLOBAL=9593676043677.764.1512397399492; SCF=Aq7YX9XtP9dpcKHI5mhPhhh0lHvVJ-oZtNdj1soOvY2j6keICzB0pwgv0jS2yZaePItCRqfMPiT2ecRsOOL4t8k.; SUHB=0h150JzumyJkzk; ALF=1544001250; SUB=_2AkMtGD09f8NxqwJRmPEWyWrqa4l0zw3EieKbRMzmJRMxHRl-yT9kqkgLtRB6BpgQPAqirEDVY709sspAfDkeK1bbeitk; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WhKMK7JPLUUvlvAyubBex1v; WEB3=16eecaac1b039ffa98ceae90acb175f9; WBStorage=c1cc464166ad44dc|undefined; _s_tentry=www.baidu.com; UOR=www.baidu.com,bang.weibo.com,www.baidu.com; Apache=2150166840655.1433.1514610546674; ULV=1514610546684:5:5:2:2150166840655.1433.1514610546674:1514451428930; PHPSESSID=5negdul8714ndu2o8209qk39i3'}


keywords = ['中国新歌声', '我是演说家', '青春旅社', '湖南卫视中秋晚会', '亲爱的客栈', '天籁之战', '小手牵小狗', '爸爸去哪儿', '穿越吧厨房', '我们来了', '男子甜点俱乐部', '漂亮的房子', '天使之路', '极速前进', '梦想改造家', '天籁之战', '哎哟辣么美', '我为喜剧狂', '我们的征途', '大片起来嗨', '跨界喜剧王', '脱口秀大会', '非诚勿扰', '爱情保卫战', '非常完美', '非正式会谈', '武林风', '变形计', '鲁豫有约', '坑王驾到']

sDate, eDate = "2017-12-21", "2017-12-27"

keyword = '青春旅社'

hotZT = getWeiZSHotZT(header, keyword, sDate, eDate)
# regionInfo, provinceCompare = getWeiZSRegionInfo(header, cookie, keyword)
# attributeAllDate = getWeiZSAttribute(header, cookie, keyword)
print(hotZT)
'''
