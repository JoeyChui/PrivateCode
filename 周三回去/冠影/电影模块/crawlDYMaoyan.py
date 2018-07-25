
import re, time, json, requests, xlwt
from requests.exceptions import RequestException


def getOnePage(url, encoding = 'UTF-8', headers = {}, cookies = {}):
    try:
        response = requests.get(url, headers = headers, cookies = cookies)
        if response.status_code == 200:
            response.encoding = encoding
            return response.text
        return None
    except RequestException:
        print("ER:getOnePage", url)
        return None

def reHTML(patternStr, html, first = False, loop = False):
    pattern = re.compile(patternStr, re.S)
    items = re.findall(pattern, html)
    if items == []:
        return None
    if first:
        return items[0]
    if loop:
        result = ""
        for item in items:
            if result != "":
                result += ','
            result += item.strip()
        return result
    return items

def getSecretKey(url):
    eotText = getOnePage(url)
    eotText = eotText[eotText.find("uni"):]
    secretList = eotText[:-3].split("\x07")
    secretKey = {}
    for ii in range(len(secretList)):
        secretKey[secretList[ii].lower()[3:]] = str(ii)
    return secretKey

def getActualNum(integer, decimal, secretKey):
    integer, decimal = str(integer), str(decimal)
    actualInteger = ''
    while integer != '':
        actualInteger += secretKey[integer[:4]]
        integer = integer[4:]
    actualDecimal = ''
    while decimal != '':
        actualDecimal += secretKey[decimal[:4]]
        decimal = decimal[4:]
    if actualDecimal == '':
        return actualInteger
    return actualInteger + '.' + actualDecimal

def mergeList(lista, listb):
    for ele in listb:
        lista.append(ele)
    return lista

def ticketoOfficeHander(string):
    if string == '':
        return ''
    result = ''
    string = string.split(";")
    for item in string:
        result += item[3:]
    return result

def getOneMovieInfo(url, headers = {}, cookies = {}):
    html = getOnePage(url, headers, cookies)

    # eot
    patternStr = "(//vfile.meituan.net/colorstone/[\d\w]+.eot)"
    eotURL = "http:" + reHTML(patternStr, html, first = True)
    secretKey = getSecretKey(eotURL)
    #print(secretKey)

    # score
    patternStr = "index-left info-num.*?<span class=\"stonefont\">&#x([\d\w]{4});.&#x([\d\w]{4});"
    score = reHTML(patternStr, html, first = True)
    score = getActualNum(score[0], score[1], secretKey)
    #print(score)

    # ticketoOffice
    #patternStr = "movie-index-content box\">.*?span class=\"stonefont\">([;&#x\d\w]+);\.([;&#x\d\w]+);.*?unit\">(.*?)<"
    patternStr = "movie-index-content box\">.*?span class=\"stonefont\">([\.;&#x\d\w]+);.*?unit\">(.*?)<"
    numberStr, unit = reHTML(patternStr, html, first = True)
    if ";." in numberStr:
        pos = numberStr.find(";.")
        integer = numberStr[:pos]
        decimal = numberStr[pos+2:]
    else:
        integer = numberStr
        decimal = ''
    integer = ticketoOfficeHander(integer)
    decimal = ticketoOfficeHander(decimal)
    ticketoOffice = getActualNum(integer, decimal, secretKey)
    ticketoOffice = ticketoOffice + unit # float(ticketoOffice) * units[items[-1]]
    #print(ticketoOffice)

    # votes
    patternStr = "class='score-num'><span class=\"stonefont\">([;&#x\d\w]+);"
    votes = reHTML(patternStr, html, first = True)
    votes = ticketoOfficeHander(votes)
    votes = getActualNum(votes, '', secretKey)
    #print(votes)

    # commentNum
    patternStr = "\"comment-approve-click.*?num\">(\d+)<"
    items = reHTML(patternStr, html)
    commentNum = 0
    for item in items:
        commentNum += int(item)
    #print(commentNum)

    # '动画,冒险,家庭', '2017-11-24'
    patternStr = "class=\"ellipsis\">(.*?)</li.*?li class=\"ellipsis\".*?class=\"ellipsis\">(\d+-\d+-\d+).*?<"
    movieClass, date = reHTML(patternStr, html, first = True)
    #print(movieClass, date)

    # director
    patternStr = "\"celebrity \".*?div class=\"info\".*?class=\"name\">(.*?)<"
    director = reHTML(patternStr, html, first = True).strip()
    #print(director)

    # actors
    patternStr = "class=\"celebrity actor\".*?class=\"info\".*?s=\"name\">(.*?)<"
    actors = reHTML(patternStr, html, loop = True)
    #print(actors)
    return score, ticketoOffice, commentNum, movieClass, date, director, actors, votes

def crawlDYMaoyanOnePage(offset, maoyanBigtable, headers, cookies):
    url = "http://maoyan.com/films?sortId=1&yearId=12&offset=" + str(offset)
    html = getOnePage(url, headers, cookies)
    patternStr = "title=\"(.*?)\".*?\"\{movieId:(\d+)\}\""
    items = reHTML(patternStr, html)
    print(1111, items)
    for item in items:
        try:
            name, id = item[0], item[1]
            if name.find(' ') != -1:
                name = name[:name.find(' ')]
            url = "http://maoyan.com/films/" + str(id)
            score, ticketoOffice, commentNum, movieClass, date, director, actors, votes = getOneMovieInfo(url, headers, cookies)
            print(name, score, director, actors, id, url, votes, commentNum, movieClass, ticketoOffice)
            # ["name", "score", "director", "actors", "id", "url", "votes", "commentNum", "movieClass", "ticketoOffice"]
            maoyanBigtable.append([name, score, director, actors, id, url, votes, commentNum, movieClass, ticketoOffice])
        except:
            print(-1)
            continue
    return maoyanBigtable

def wtToXLS(content, filename):
    workbook = xlwt.Workbook(encoding = 'utf-8')
    booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok = True)
    for i, rowVal in enumerate(content):
        for j, colVal in enumerate(rowVal):
            booksheet.write(i, j, colVal)
    workbook.save('%s.xls' % filename)
    print("write success!")
    return

def crawlDYMaoyan(offsetMax):
    headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, sdch, br",
                "Accept-Language": "zh-CN,zh;q=0.8",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive",
                "Host": "maoyan.com",
                "Referer": "https://movie.douban.com/cinema/nowplaying/beijing/",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
              }
    cookies = {"Cookie": 'uuid=4637468b0a124addb64a.1522986939.1.0.0; mtcdn=K; u=1051553653; n=qWg466131557; lt=EidBZoH75XB_lo7zWyfgNQp_5kwAAAAApAUAABmWeIMiiSql77WjSmoch3NBU55L2Icxx1rn5jxFCABS_zwu5sUAoxQHUErzIjmTiA; lsu='}

    maoyanBigtable = [["name", "score", "director", "actors", "id", "url", "votes", "commentNum", "movieClass", "ticketoOffice"]]
    for offset in range(0, offsetMax, 30):
        print("*********** now " + str(offset))
        maoyanBigtable = crawlDYMaoyanOnePage(offset, maoyanBigtable, headers, cookies)
    wtToXLS(maoyanBigtable, "MaoyanDianYing")

    print(2222, len(maoyanBigtable))
    return


if __name__=="__main__":
    print("main")
    crawlDYMaoyan(90)
