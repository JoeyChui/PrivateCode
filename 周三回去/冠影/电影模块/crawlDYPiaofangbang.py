
import requests, re, xlwt
from requests.exceptions import RequestException
import crawlDYMaoyan


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

def getMovieInfoDict(url, uid):
    headers = {
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, sdch",
                "Accept-Language": "zh-CN,zh;q=0.8",
                "Connection": "keep-alive",
                "Host": "piaofang.maoyan.com",
                #"Referer": "http://piaofang.maoyan.com/?date=2017-12-25",
                "Uid": "{}".format(uid),
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest"
              }
    html = getOnePage(url, headers = headers)
    '''
    id: patternStr = "href:./movie/(\d+)\?_v_=yes\'..>"
    name: patternStr = "li class='c1'.*?<b>(.*?)<"
    ticketoOffice: patternStr = "<li class=.\"c2 .\">.*?<b>(.*?)<"
    '''
    patternStr = "href:./movie/(\d+)\?_v_=yes\'..>.*?li class='c1'.*?<b>(.*?)<.*?<li class=.\"c2 .\">.*?<b>(.*?)<"
    pattern = re.compile(patternStr, re.S)
    items = re.findall(pattern, html)
    movieInfoList = []
    if items != []:
        for item in items:
            oneMovieInfo = {}
            oneMovieInfo["id"] = item[0]
            oneMovieInfo["name"] = item[1]
            oneMovieInfo["ticketoOfficeMonth"] = str(int(float(item[2]) * 10000))
            movieInfoList.append(oneMovieInfo)
    return movieInfoList

def wtToXLS(content, filename):
    workbook = xlwt.Workbook(encoding = 'utf-8')
    booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok = True)
    for i, rowVal in enumerate(content):
        for j, colVal in enumerate(rowVal):
            booksheet.write(i, j, colVal)
    workbook.save('%s.xls' % filename)
    print("write success!")
    return

def crawlDYPiaofangbang():
    bigTable = [["name", "id", "ticketoOfficeMonth", "url", "score", "ticketoOffice", "commentNum", "movieClass", "date", "director", "actors", "votes"]]
    month = "201712"
    uid = "c6d02c7c3717cf196e6c486dcc3981f9505d9225"
    url = "http://piaofang.maoyan.com/boxoffice/2?date={}&cnt=10".format(month)
    movieInfoList = getMovieInfoDict(url, uid)
    print(movieInfoList, len(movieInfoList))

    for item in movieInfoList:
        print(item["name"], item["id"])
        url = "http://maoyan.com/films/" + str(item["id"])
        score, ticketoOffice, commentNum, movieClass, date, director, actors, votes = crawlDYMaoyan.getOneMovieInfo(url)
        print(score, ticketoOffice, commentNum, movieClass, date, director, actors, votes)
        bigTable.append([item["name"], item["id"], item["ticketoOfficeMonth"], url, score, ticketoOffice, commentNum, movieClass, date, director, actors, votes])
    wtToXLS(bigTable, "PiaoFangBang123")
    return


crawlDYPiaofangbang()
