
import re, json, requests
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

def idParseOnePage(html):
    pattern = re.compile('movieid:(\d+)}', re.S)
    items = re.findall(pattern, html)
    return items

def writeToIDFile(content):
    with open('movieidresult.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()

idurl = 'http://maoyan.com/films?offset=0'
idhtml = getOnePage(idurl)
for item in idParseOnePage(idhtml):
    writeToIDFile(item)

