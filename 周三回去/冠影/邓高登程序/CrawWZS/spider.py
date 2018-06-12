# coding=utf-8
# 2017年9月23日 下午6:59
# author:Gordon Deng

import urllib, requests
from config import *

weiZSData = {}
def getWID(keyword):
    header = {
                 "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36",
                 "Referer":"http://data.weibo.com/index?sudaref=www.google.com"
             }
    url = "http://data.weibo.com/index/ajax/hotword?word=%s&flag=nolike&_t=0" % keyword
    result = requests.get(url, headers = header).json()
    if result['code'] != '100000':
        print('ER:%s' % str(keyword))
        return
    wid = result['data']['id']
    return wid

def getWeiZSOrigin(keyword, sDate, eDate):
    keyword = urllib.parse.quote(keyword)
    wid = getWID(keyword)
    header = {
			  "Connection":"keep-alive",
			  "Accept-Encoding": "gzip, deflate, sdch",
			  "Accept": "*/*",
			  "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36",
			  "Accept-Language": "zh-CN,zh;q=0.8",
			  "Referer": "http://data.weibo.com/index/hotword?wid={}&wname={}".format(wid, keyword),
			  "Content-Type": "application/x-www-form-urlencoded",
			  "Host":"data.weibo.com"
    		 }
    url = "http://data.weibo.com/index/ajax/getchartdata?wid={}&sdate={}&edate={}".format(wid, sDate, eDate)
    result = requests.get(url, headers = header).json()
    return result

def getWeiZSVaule(weiZSOrigin):
    weiZSVaule = {}
    weiZSZT = weiZSOrigin['zt']
    if weiZSZT == False:
        return 0
    for ii in range(len(weiZSZT)-1):
        weiZSVaule[weiZSZT[ii]['day_key'].replace('-','')] = weiZSZT[ii]['value']
    return weiZSVaule

def writeToTXT(content, fileName):
    with open('%s.txt' % fileName, 'w', encoding='utf-8') as f:
        f.write(content)
        f.close()
    return

def crawlWeiZS(keywords, sDate, eDate):
    for keyword in keywords:
        print(keyword)
        weiZSOrigin = getWeiZSOrigin(keyword, sDate, eDate)
        weiZSVaule = getWeiZSVaule(weiZSOrigin)
        weiZSData[keyword] = weiZSVaule
    # writeToTXT(str(weiZSData).replace("'",'"'), 'WeiZS-{}-{}'.format(sDate.replace('-', ''), eDate.replace('-', '')))


sDate, eDate = "2017-08-01", "2017-09-10"

crawlWeiZS(keywords, sDate, eDate)
