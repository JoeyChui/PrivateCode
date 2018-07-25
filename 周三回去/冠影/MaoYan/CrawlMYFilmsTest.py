
import re, time, json, requests
from requests.exceptions import RequestException
from multiprocessing import Pool

def getOnePage(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def getMagicalNum(html):
    pattern = re.compile('p1\.meituan\.net/colorstone/.*\.eot', re.S)
    items = re.findall(pattern, html)
    if items == []:
        time.sleep(1)
        print('555')
        return False
    pos = items[0].find('eot', 1)
    urlMagical = items[0][:pos+3]
    responseMagical = requests.get('http://' + urlMagical)
    htmlMagical = responseMagical.text
    pos = htmlMagical.find('uni', 1)
    htmlMagical = htmlMagical[pos:]
    text = htmlMagical
    pat = re.compile('uni.{4}', re.S)
    items = re.findall(pat, text)
    MagicalNumber = {}
    i = 0
    for ele in items:
        ele = ele[3:]
        ele = ele.lower()
        MagicalNumber[ele] = i
        i += 1
    return MagicalNumber

def parseOnePage(html):
    pattern = re.compile('<h3 class="name">(.*?)</h3>.*?"ename ellipsis">(.*?)</div>.*?<li class="ellipsis">(.*?)</li>.*?ellipsis">(.*?)/(.*?)</li>'
                            +'.*?="ellipsis">(.*?)</li>.*?movieid:(.*?)}">.*?stonefont">&#x(.*?);.&#x(.*?);</span.*?><span class="stonefont">(.*?)</span.*?movie-index-content box.*?stonefont">(.*?)</span>', re.S)
    items = re.findall(pattern, html)
    print(items)
    temp = []
    for ele in items[0]:
        temp.append(ele)
    return temp

def dataHander(items, MagicalNumber):
    i = 0
    for item in items:
        result = tranData(item, MagicalNumber)
        if not result == False:
            items[i] = result
        i += 1

def tranData(datastr, MagicalNumber):
    if datastr in MagicalNumber:
        return MagicalNumber[datastr]
    return False


def writeToFile(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()

def main(offset):
    url1 = 'http://maoyan.com/films/' + str(offset)
    print(url1)
    while True:
        response = requests.get(url1)
        if response.status_code == 200:
            html = response.text
            break
    print(111111)
    #writeToFile(html)
    while True:
        MagicalNumber = getMagicalNum(html)
        if not MagicalNumber == False:
            break
    print(222222)
    print(MagicalNumber)
    items = parseOnePage(html)
    writeToFile(items)
    writeToFile(MagicalNumber)
    print('SEC')
    writeToFile('****************************************************************************\n')

def idParseOnePage(html):
    pattern = re.compile('movieid:(\d+)}', re.S)
    items = re.findall(pattern, html)
    print(items[0])
    return items

def writeToIDFile(content):
    with open('movieidresult.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()

#if __name__ == '__main__':
'''
    pool = Pool()
    pool.map(main, [i*10 for i in range(10)])
    pool.close()
    pool.join()
'''
main(1207856)
'''
idurl = 'http://maoyan.com/films?offset=0'
idhtml = getOnePage(idurl)
items = idParseOnePage(idhtml)
for item in items:
    writeToIDFile(item)
    main(item)
'''



