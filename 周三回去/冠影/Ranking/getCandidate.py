#-*-coding:utf-8-*- 
#2017-9-20 JoeyChui sa517045@mail.ustc.edu.cn

import re, requests
from requests.exceptions import RequestException

def getOnePage(url, encoding='utf-8'):
    try:
        response = requests.get(url)
        response.encoding = encoding
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('ER:getOnePage')
        return None

def getCandidates(URLS):
    candidates = []
    for url in URLS:
        html = getOnePage(url, 'gbk')
        pattern = re.compile('"list-title" target="_blank".*?>(.*?)</a>', re.S)
        items = re.findall(pattern, html)#[:15]
        for item in items:
            if item not in candidates:
               candidates.append(item)
    return candidates


URLS = ['http://top.baidu.com/buzz?b=258&fr=topboards',
        'http://top.baidu.com/buzz?b=618&fr=topindex', 
        'http://top.baidu.com/buzz?b=1395&c=9&fr=topbuzz_b17_c9', 
        'http://top.baidu.com/buzz?b=1396&c=9&fr=topbuzz_b1395_c9']

candidates = getCandidates(URLS)
print(candidates, len(candidates))
