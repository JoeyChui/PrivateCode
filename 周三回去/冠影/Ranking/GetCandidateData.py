#-*-coding:utf-8-*- 
#2017-9-26 JoeyChui sa517045@mail.ustc.edu.cn

import re, requests, lxml.html
from requests.exceptions import RequestException

def getOnePage(url, encoding='utf-8', header={}, cookie={}):
    try:
        response = requests.get(url, headers=header, cookies=cookie)
        if response.status_code == 200:
            response.encoding = encoding
            return response.text
        return None
    except RequestException:
        print('ER:getOnePage', url)
        return None

def strToInt(strList):
    intList = []
    for ele in strList:
        intList.append(int(ele))
    return intList

def getCandidateData(url, header, cookie):
    html = getOnePage(url, header, cookie)
    basicData = re.findall(r'strong class=\\"W_f\d+\\">(\d+).*?strong><span class=', html)
    forward = re.findall(r'"W_ficon ficon_forward S_ficon\\">&#xe\d+;<\\/em><em>(\d+)<\\/em>', html)
    repeat = re.findall(r'W_ficon ficon_repeat S_ficon\\">&#xe\d+;<\\/em><em>(\d+)<\\/em>', html)
    praised = re.findall(r'W_ficon ficon_praised S_txt2\\">.*?<\\/em><em>(\d+)<\\/em>', html)
    print('Weibo\'s num is', len(basicData), len(forward), len(repeat), len(praised))
    basicData, forwardSum, repeatSum, praisedSum = strToInt(basicData), sum(strToInt(forward)), sum(strToInt(repeat)), sum(strToInt(praised))
    hotData = int((forwardSum + repeatSum * 10 + praisedSum) / 3)
    return basicData, hotData, forwardSum, repeatSum, praisedSum
'''
def getCandidateDataWithLXML(url):
    html = getOnePage(url)
    tree = lxml.html.fromstring(html)
    result = tree.cssselect('#Pl_Official_MyProfileFeed__23 > div > div:nth-child(2) > div.WB_feed_handle > div > ul > li:nth-child(2) > a > span > span > span > em:nth-child(2)')
    print(result)
'''
header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
          "Referer":"http://s.weibo.com/weibo/",
          "Host":"s.weibo.com"}
cookie = {"Cookie":'SINAGLOBAL=5603284969403.144.1506346301779; UM_distinctid=15ed84b0ae0706-0e9b74d7b9807e-6b1b1279-100200-15ed84b0ae15c4; ULV=1506941291450:4:1:1:662253573607.4519.1506941291440:1506691164833; UOR=,,www.cnblogs.com; SSOLoginState=1507548073; SCF=Aq4-tJQHVXbm3sfysY5zYIoWBIP_6Vd9d1TK_vQ2syjP1jJEqXX03_JSNmxU9959h8OZh-I_QO6MIKxAKZg4lo0.; SUB=_2A2502Mw6DeRhGeBO7VIT9CbIwzmIHXVXr7ryrDV8PUNbmtANLUjQkW-Z9G2QSsWFMEEHJ3s4-SRukYAwqg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFrb8b65iCT0ifykZ.qvATx5JpX5KMhUgL.Foq7So5EShnX1h-2dJLoI7yZdcH4BcyfIBtt; SUHB=0sqxrZka6Oz8zk; ALF=1539174377; SWB=usrmdinst_12'}


urls = ['http://weibo.com/u/3591355593?is_all=1&page=1']#, 'http://weibo.com/u/3591355593', 'http://weibo.com/u/1825457341', 'http://weibo.com/u/1804549454', 'http://weibo.com/u/1669879400']
for url in urls:
    basicData, hotData, forwardSum, repeatSum, praisedSum = getCandidateData(url, header, cookie)
    print(basicData, hotData, forwardSum, repeatSum, praisedSum)
