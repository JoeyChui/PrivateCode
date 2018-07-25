#-*-coding:utf-8-*-
#2017-11-08 JoeyChui sa517045@mail.ustc.edu.cn

import time, urllib, requests, re, xlrd, xlwt
from requests.exceptions import RequestException

def getOnePage(url, encoding = 'UTF-8', headers = {}, cookies = {}, json = False):
    try:
        response = requests.get(url, headers = headers, cookies = cookies)
        response.encoding = encoding
        if response.status_code != 200:
            print("ER:getOnePage", "status_code is " + str(response.status_code), url)
            return None
        if json:
            return response.json()
        return response.text
    except RequestException:
        print("ER:getOnePage", url)
        return None

def reHTML(patternStr, html, first = False, functionFlag = False, function = None):
    pattern = re.compile(patternStr, re.S)
    items = re.findall(pattern, html)
    if items == []:
        return []
    for ii in range(len(items)):
        if type(items[ii]) == tuple:
            itemStrip = []
            for ele in items[ii]:
                itemStrip.append(str(ele).strip())
            items[ii] = itemStrip
        else:
            items[ii] = str(items[ii]).strip()
    if first:
        return items[0]
    if functionFlag:
        return function(items)
    return items

def margeList(a, b):
    for ele in b:
        a.append(ele)
    return a

def getTwentyComments(commentURL, headers, cookies):
    html = getOnePage(commentURL, headers = headers, cookies = cookies)
    patternStr = "comment-item.*?class=\"votes\">(\d+)</span>.*?rating\" title=\"(.*?)\">.*?comment-time.*?>(.*?)</span>.*?p class=\"\">(.*?)</p>"
    items = reHTML(patternStr, html)
    comments = []
    for item in items:
        oneCommentDict = {}
        oneCommentDict["vote"] = item[0]
        oneCommentDict["rate"] = item[1]
        oneCommentDict["date"] = item[2]
        oneCommentDict["content"] = item[3]
        comments.append(oneCommentDict)
    return comments

def getShortComments(movieID, start, headers, cookies):
    comments = []
    while True:
        print("########", start)
        commentURL = "https://movie.douban.com/subject/{}/comments?start={}&limit=20&sort=new_score&status=P&percent_type=".format(movieID, start)
        twentyComments = getTwentyComments(commentURL, headers, cookies)
        print(twentyComments)
        margeList(comments, twentyComments)
        if twentyComments == []:
            break
        start += 20
    return comments


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
          "Host": "movie.douban.com"}
cookies = {"Cookie": 'bid=uIdvb7Zx93o; ll="118163"; __yadk_uid=dKCYLMfL0Sm6YNOVsFMOa760TfYUqQJc; ps=y; dbcl2="171636217:34LP98haFT0"; ck=zFBM; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1516505355%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _vwo_uuid_v2=078B00143C1A8A290A62671CAB841223|509c7ea76933e60f72bae011c9077902; _pk_id.100001.4cf6=9fc96e3e445dc5bf.1515943852.5.1516505760.1516456770.; _pk_ses.100001.4cf6=*; __utma=30149280.1367348568.1515943853.1516454393.1516505355.6; __utmb=30149280.0.10.1516505355; __utmc=30149280; __utmz=30149280.1516448214.3.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utma=223695111.1205779028.1515943853.1516454393.1516505355.5; __utmb=223695111.0.10.1516505355; __utmc=223695111; __utmz=223695111.1516451383.3.3.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; push_noty_num=0; push_doumail_num=0'}


movieName = "寻梦环游记"
movieID = 26372319
movieURL = "https://movie.douban.com/subject/" + str(movieID)
start = 400
shortComments = getShortComments(movieID, start, headers, cookies)
print("*******************")
print(shortComments)
