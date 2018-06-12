
import re, time, json, requests
from requests.exceptions import RequestException
from multiprocessing import Pool

'''
from urllib.request import urlopen

html = urlopen('http://www.mgtv.com/b/317645/4078913.html')
print(html.read().decode('utf-8'))
'''
'''
for link in soup.find_all('a'):
    print(link.get('href'))
    # http://example.com/elsie
    # http://example.com/lacie
    # http://example.com/tillie
'''

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

def reHTML(patternStr, html, first = False):
    pattern = re.compile(patternStr, re.S)
    items = re.findall(pattern, html)
    if items == []:
        return None
    if first:
        return items[0]
    return items

def matchMovieID(html):
    pat = re.compile('movieId:(\d+)}"')
    items = re.findall(pat, html)
    return items

# url('//vfile.meituan.net/colorstone/98baed5dd0c0c0030efdeee9af74ab0a3168.eot')

def matchEotFile(html):
    patternStr = "(//vfile.meituan.net/colorstone/.*?.eot)"
    items = reHTML(patternStr, html)
    print(2124, "http:" + items[0])
    return "http:" + items[0]
    #exit()
    '''
    pos = html.find('eot', 1)
    temp = html[pos-100:pos+3]
    eotFileURL = 'http:' + temp[temp.find('//p1', 1):]
    return eotFileURL
    '''
def getSecretKey(eotText):
    eotText = eotText[eotText.find('uni', 1):]
    pat = re.compile('uni([A-Z0-9]{4})')
    items = re.findall(pat, eotText)
    secretKey = {}
    i = 0
    for item in items:
        item = item.lower()
        secretKey[item] = i
        i += 1
    return secretKey

def matchFilmBasicInfo(html):
    pat = re.compile('<h3 class="name">(.*?)</h3>.*?ename ellipsis">(.*?)</div>.*?action clearfix" data-val="{movieid:(\d+)}"', re.S)
    item = re.findall(pat, html)[0]
    filmBasicInfo = {}
    filmBasicInfo['name'] = item[0]
    filmBasicInfo['ename'] = item[1]
    filmBasicInfo['movieID'] = item[2]
    return filmBasicInfo

def matchFilmScore(html):
    pat = re.compile('movie-stats-container.*?movie-index-title">(.*?)</p>.*?index-left info-num.*?stonefont">(.*?);</span>', re.S)
    items = re.findall(pat, html)
    if items == []:
        return False
    print(items[0])

def matchFilmBoxOffice(html):
    pat = re.compile('movie-index-content box.*?stonefont">(.*?);</span>.*?unit">(.*?)</span>', re.S)
    items = re.findall(pat, html)
    if items == []:
        return False
    print(items[0])

def parseOneHtml(html):
    #get secretKey
    eotFileURL = matchEotFile(html)
    if 'colorstone' in eotFileURL:
        print('2@OK:matchEotFile')
    else:
        print('1@ER:matchEotFile.Trying again!')
        return '1@ER:matchEotFile'
    eotText = getOnePage(eotFileURL, headers = headers, cookies = cookies)
    print(eotText)
    secretKey = getSecretKey(eotText)
    print(secretKey)

    #get film information
    filmBasicInfo = matchFilmBasicInfo(html)
    print(filmBasicInfo)
    matchFilmScore(html)
    matchFilmBoxOffice(html)

def getMovieID(url, offset):
    html = getOnePage(url + str(offset), headers = headers, cookies = cookies)
    movieIDs = matchMovieID(html)
    return movieIDs

def getOneFilm(movieID):
    url = 'http://maoyan.com/films/' + str(movieID)
    while True:
        html = getOnePage(url, headers = headers, cookies = cookies)
        result = parseOneHtml(html)
        if not result == '1@ER:matchEotFile':
            break
        time.sleep(2)

def main(url, offset):
    movieIDs = getMovieID(url, offset)
    for movieID in movieIDs:
        getOneFilm(movieID)
        time.sleep(5)

headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Connection": "keep-alive",
            "Host": "maoyan.com",
            "Referer": "http://piaofang.maoyan.com/?date=2017-12-25",
            "Uid": "c6d02c7c3717cf196e6c486dcc3981f9505d9225",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
          }
cookies = {"Cookie": "uuid=1A6E888B4A4B29B16FBA1299108DBE9C3F5EFD493C408FA5857A753C3E349497; _lxsdk=16068e55c0ec8-0df3de255f6a8e-6b1b1279-1fa400-16068e55c0ec8; _csrf=b0b3b91febf6ae895730e31534fb8080c50db139052e9a4274ca61d6a0dcbe40; theme=moviepro; __mta=41808541.1513588334671.1514117029138.1514117192547.21; _lxsdk_s=989475b17b71623f58dee26031d6%7C%7C2"}

'''
url = 'http://maoyan.com/films?offset='
offset, end = 30, 30
while offset <= 30:
    print(offset, '*******************************************************************************************')
    main(url, offset)
    offset += 30
'''

getOneFilm(1170264)
