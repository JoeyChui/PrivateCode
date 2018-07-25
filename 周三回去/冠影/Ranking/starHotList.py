#-*-coding:utf-8-*- 
#2017-9-20 JoeyChui sa517045@mail.ustc.edu.cn

import re, requests, xlwt#, crawllWeiZS
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

def getStarCandidate(urls):
    starCandidate = []
    for url in urls:
        html = getOnePage(url, encoding = 'gbk')
        pattern = re.compile('"list-title" target="_blank".*?>(.*?)</a>', re.S)
        items = re.findall(pattern, html)
        for item in items:
            if item not in starCandidate:
               starCandidate.append(item)
    return starCandidate
'''
def getCandidateWeiboURL(candidate, header, cookie):
    url = 'http://s.weibo.com/weibo/' + candidate
    html = getOnePage(url, header, cookie)
    #print(html)
    weiboID = re.findall(r'action-data=\\\"uid=(\d+)', html)[0]
    weiboIDURL = 'http://weibo.com/u/' + weiboID + '?is_all=1&page=1'
    items = re.findall(r'star_detail.*?href=\\"http:\\/\\/weibo.com\\/([_\w]+)\?', html)
    if items != []:
        weiboIDCN = items[0]
    else:
        weiboIDCN = -1
    weiboIDCNURL = 'http://weibo.com/' + str(weiboIDCN) + '?is_all=1&page=1'
    if weiboIDCN == -1:
        return weiboIDURL
    else:
        return weiboIDCNURL
'''
def reHTML(patternStr, html):
    pattern = re.compile(patternStr, re.S)
    items = re.findall(pattern, html)
    if items == []:
        return None
    return items[0]

def getCandidateWeiboURL(name, header, cookie):
    url = 'http://s.weibo.com/user/' + name
    html = getOnePage(url, header, cookie)
    if 'noresult_tit' in html:
        raise SelfException

    patternStr = r'person_detail.*?href=\\"\\/\\/(weibo\.com[\\/u]*\\/[_\w\d]+)\?refer_flag'
    reResult = reHTML(patternStr, html) # 'weibo.com\\/u\\/5111239333', 'weibo.com\\/abtcxtw'
    if 'weibo.com\\/u\\/' in reResult:
        weiboID = reResult[len('weibo.com\\/u\\/'):]
        weiboURL = 'https://weibo.com/u/' + str(weiboID) + '?is_hot=1'
    else:
        weiboID = reResult[len('weibo.com\\/'):]
        weiboURL = 'https://weibo.com/' + weiboID + '?is_hot=1'
    return weiboURL

def strToInt(strList):
    intList = []
    for ele in strList:
        intList.append(int(ele))
    return intList

def getCandidateWeiboData(url, header, cookie):
    html = getOnePage(url, header, cookie)
    basicData = re.findall(r'strong class=\\"W_f\d+\\">(\d+).*?strong><span class=', html)
    forward = re.findall(r'"W_ficon ficon_forward S_ficon\\">&#xe\d+;<\\/em><em>(\d+)<\\/em>', html)
    repeat = re.findall(r'W_ficon ficon_repeat S_ficon\\">&#xe\d+;<\\/em><em>(\d+)<\\/em>', html)
    praised = re.findall(r'W_ficon ficon_praised S_txt2\\">.*?<\\/em><em>(\d+)<\\/em>', html)
    basicData, forwardAver, repeatAver, praisedAver = strToInt(basicData), sum(strToInt(forward)) / len(forward), sum(strToInt(repeat)) / len(repeat), sum(strToInt(praised)) / len(praised)
    hotData = int((forwardAver + repeatAver * 10 + praisedAver) / 5)
    print('Weibo\'s num is', len(basicData), len(forward), len(repeat), len(praised))
    return basicData, hotData

def wtToXLS(content, filename):
    workbook = xlwt.Workbook(encoding = 'utf-8')
    booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok = True)
    for i, rowVal in enumerate(content):
        for j, colVal in enumerate(rowVal):
            booksheet.write(i, j, colVal)
    workbook.save('%s.xls' % filename)
    return


baiduTopURL = ['http://top.baidu.com/buzz?b=258&fr=topboards',
               'http://top.baidu.com/buzz?b=618&fr=topindex', 
               'http://top.baidu.com/buzz?b=1395&c=9&fr=topbuzz_b17_c9', 
               'http://top.baidu.com/buzz?b=1396&c=9&fr=topbuzz_b1395_c9']

baiduTopURL = ['http://top.baidu.com/buzz?b=618&c=9']
header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
          "Referer": "http://s.weibo.com/weibo/",
          "Host": "s.weibo.com"}
cookie = {"Cookie": 'SINAGLOBAL=9593676043677.764.1512397399492; YF-Page-G0=00acf392ca0910c1098d285f7eb74a11; _s_tentry=-; Apache=8489084273703.082.1514774587448; ULV=1514774587458:6:1:1:8489084273703.082.1514774587448:1514610546684; YF-V5-G0=1da707b8186f677d9e4ad50934b777b3; YF-Ugrow-G0=1eba44dbebf62c27ae66e16d40e02964; login_sid_t=0a15d777a09e706106d5c4cdfdb92cd4; appkey=; ULOGIN_IMG=15147768177067; WBStorage=c1cc464166ad44dc|undefined; cross_origin_proto=SSL; crossidccode=CODE-yf-1EvQHA-FxhGN-lpyB3Ba4F9HuSIl29e9f3; SSOLoginState=1514777048; SCF=Aq7YX9XtP9dpcKHI5mhPhhh0lHvVJ-oZtNdj1soOvY2jeRdCY6uL2fIsDxVJnjDGD7va3mZSxCWStOHyzf7o_vw.; SUB=_2A253TdmIDeThGeBK71oZ9CrJwjWIHXVUO0xArDV8PUNbmtANLWHWkW9NR6LNHFaxu7tPcRJ-8tv7An7xe62nYZOn; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhaBsvDSWSEex17Pj.WMAZ45JpX5KzhUgL.FoqXShnRShBf1K.2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMcShBR1hBXSK.4; SUHB=0cS3pqCG7z9Je5; ALF=1546313047; UOR=www.baidu.com,bang.weibo.com,login.sina.com.cn; wvr=6; wb_cusLike_6448844599=N; WBtopGlobal_register_version=49306022eb5a5f0b'}

starCandidate = getStarCandidate(baiduTopURL)

#starCandidate = ['迪丽热巴', '吴彦祖']

print(starCandidate, len(starCandidate))

bigTable = [["name", "weiboURL", "weiboHotData"]]


while starCandidate != []:
    candidate = starCandidate[0]
    try:
        weiboURL = getCandidateWeiboURL(candidate, header, cookie)
        weiboBasicData, weiboHotData = getCandidateWeiboData(weiboURL, header, cookie)
        bigTable.append([candidate, weiboURL, weiboHotData])
        print("ok", candidate, weiboURL, weiboBasicData, weiboHotData)
        starCandidate.pop(0)
    except:
        print("er", candidate)
        starCandidate.pop(0)

        #if candidate = ""
        

wtToXLS(bigTable, "StarHotList")
