#-*-coding:utf-8-*- 
#2017-9-26 JoeyChui sa517045@mail.ustc.edu.cn

import re, requests
from requests.exceptions import RequestException

def getOnePage(url, header={}, cookie={}):    
    try:
        response = requests.get(url, headers=header, cookies=cookie)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('ER:getOnePage')
        return None

header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
          "Referer":"http://s.weibo.com/weibo/",
          "Host":"s.weibo.com"}
cookie = {"Cookie":'SINAGLOBAL=5603284969403.144.1506346301779; UM_distinctid=15ed84b0ae0706-0e9b74d7b9807e-6b1b1279-100200-15ed84b0ae15c4; ULV=1506941291450:4:1:1:662253573607.4519.1506941291440:1506691164833; UOR=,,www.cnblogs.com; SSOLoginState=1507548073; SCF=Aq4-tJQHVXbm3sfysY5zYIoWBIP_6Vd9d1TK_vQ2syjP1jJEqXX03_JSNmxU9959h8OZh-I_QO6MIKxAKZg4lo0.; SUB=_2A2502Mw6DeRhGeBO7VIT9CbIwzmIHXVXr7ryrDV8PUNbmtANLUjQkW-Z9G2QSsWFMEEHJ3s4-SRukYAwqg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFrb8b65iCT0ifykZ.qvATx5JpX5KMhUgL.Foq7So5EShnX1h-2dJLoI7yZdcH4BcyfIBtt; SUHB=0sqxrZka6Oz8zk; ALF=1539174377; SWB=usrmdinst_12'}

candidates = ['刘洲成', '吴亦凡', '毛不易', 'tfboys', '俞灏明', '迪丽热巴']
candidateWeibo = {}
for candidate in candidates:
    url = 'http://s.weibo.com/weibo/' + candidate
    print(url)
    html = getOnePage(url, header, cookie)
    item = re.findall(r'action-data=\\\"uid=(\d+)', html)[0]
    candidateWeibo[candidate] = 'http://weibo.com/u/' + item
    print('http://weibo.com/u/' + item)
print(candidateWeibo)
