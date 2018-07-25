
import re, time, json, requests, xlwt
from requests.exceptions import RequestException


def getOnePage(url, encoding = 'UTF-8', headers = {}, cookies = {}, json = False):
    try:
        response = requests.get(url, headers = headers, cookies = cookies)
        if response.status_code == 200:
            response.encoding = encoding
            if json:
                return response.json()
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

def getMovieDate(url):
    html = getOnePage(url)
    patternStr = "initialReleaseDate\" content=\"(\d+-\d+-\d+).*?\">"
    date = reHTML(patternStr, html, first = True)
    return date

def getMovieInfo(url):
    html = getOnePage(url)
    # director
    patternStr = "\"v:directedBy\">(.*?)<"
    director = reHTML(patternStr, html, loop = True)
    # actors
    patternStr = "\"v:starring\">(.*?)<"
    actors = reHTML(patternStr, html, loop = True)
    # votes
    patternStr = "property=\"v:votes\">(.*?)<"
    votes = reHTML(patternStr, html, first = True)
    # commentNum
    patternStr = "comments-section.*?href=\"https.*?P\">.*?(\d+).*?<"
    commentNum = reHTML(patternStr, html, first = True)
    # movieClass
    patternStr = "v:genre\">(.*?)<"
    movieClass = reHTML(patternStr, html, loop = True)
    return votes, commentNum, movieClass, director, actors

# 爬取正在上映电影
def crawlNowplaying(bigTable, headers, cookies):
    url = "https://movie.douban.com/cinema/nowplaying/shanghai/"
    html = getOnePage(url, headers = headers, cookies = cookies)
    # name score director actors id
    patternStr = "data-title=\"(.*?)\".*?data-score=\"([\.\d]+)\".*?data-director=\"(.*?)\".*?data-actors=\"(.*?)\".*?data-subject=\"(\d+)\""
    items = reHTML(patternStr, html)
    for item in items:
        url = "https://movie.douban.com/subject/{}/".format(item[4])
        votes, commentNum, movieClass, director, actors = getMovieInfo(url)

        # name score director actors id
        print(item[0], item[1], votes, commentNum,)
        ticketoOffice = 0
        oneMovieList = [item[0], item[1], item[2], item[3], item[4], url, votes, commentNum, movieClass, ticketoOffice]
        if item[0].find(" ") != -1:
            oneMovieList[0] = item[0][:item[0].find(" ")]
        bigTable.append(oneMovieList)
    return bigTable

# 爬取近期电影
def crawlFromTime(bigTable, headers, cookies):
    url = "https://movie.douban.com/j/search_subjects?type=movie&tag=热门&sort=time&page_limit=50&page_start=0"
    movies = getOnePage(url, headers = headers, cookies = cookies, json = True)["subjects"]
    for movie in movies:
        url = "https://movie.douban.com/subject/{}/".format(movie["id"])
        votes, commentNum, movieClass, director, actors = getMovieInfo(url)
        print(movie["title"], movie["rate"], votes, commentNum )
        # name score director actors id
        ticketoOffice = 0
        oneMovieList = [movie["title"], movie["rate"], director, actors, movie["id"], url, votes, commentNum, movieClass, ticketoOffice]
        if movie["title"].find(" ") != -1:
            oneMovieList[0] = movie["title"][:movie["title"].find(" ")]
        bigTable.append(oneMovieList)
    return bigTable

def wtToXLS(content, filename):
    workbook = xlwt.Workbook(encoding = 'utf-8')
    booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok = True)
    for i, rowVal in enumerate(content):
        for j, colVal in enumerate(rowVal):
            booksheet.write(i, j, colVal)
    workbook.save('%s.xls' % filename)
    return


headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Host": "movie.douban.com",
            "Referer": "https://movie.douban.com/cinema/nowplaying/beijing/",
            "Upgrade-Insecure-Requests": "1",
            "Referer": "https://movie.douban.com/explore",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
          }
cookies = {"Cookie": 'bid=BUg_m5oBSmQ; ll="108297"; __yadk_uid=y0Xm8xagpM4fvtwAmXBh2rt6qNXcxaFp; viewed="26874682"; dbcl2="171636217:34LP98haFT0"; ps=y; ct=y; ck=zFBM; ap=1; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1514412517%2C%22https%3A%2F%2Fwww.baidu.com%2Fs%3Fwd%3D%25E8%25B1%2586%25E7%2593%25A3%26ie%3DUTF-8%22%5D; _pk_id.100001.4cf6=b3a52e216ca50df9.1514114248.9.1514413849.1514375648.; _pk_ses.100001.4cf6=*; __utma=30149280.603007022.1512401229.1514375268.1514412517.10; __utmb=30149280.0.10.1514412517; __utmc=30149280; __utmz=30149280.1512401229.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.17163; __utma=223695111.745141187.1514114248.1514375268.1514412517.9; __utmb=223695111.0.10.1514412517; __utmc=223695111; __utmz=223695111.1514114248.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic|utmctr=%E8%B1%86%E7%93%A3; push_noty_num=0; push_doumail_num=0; _vwo_uuid_v2=9AF24EBE1CC467FA051070EA0BE13468|04a0aa21f6c80c9f7b343ee630c2a133'}

bigTable = [["name", "score", "director", "actors", "id", "url", "votes", "commentNum", "movieClass", "ticketoOffice"]]
bigTable = crawlNowplaying(bigTable, headers, cookies)
bigTable = crawlFromTime(bigTable, headers, cookies)
wtToXLS(bigTable, "DoubanDianYing")
