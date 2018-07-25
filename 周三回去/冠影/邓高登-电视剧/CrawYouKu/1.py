#-*-coding:utf-8-*-
#2017-9-20 JoeyChui sa517045@mail.ustc.edu.cn

import re, requests, json, xlwt
from requests.exceptions import RequestException

def getOnePage(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('ER:getOnePage')
        return None

def getTVDataDict(url):
	tvDataDict = {}
	html = getOnePage(url)
	tvDataList = json.loads(html)['subjects']
	for item in tvDataList:
		tvDataDict[item['title']] = [item['rate'], item['url']]
	return tvDataDict

def getTVNameScoreURL(candidate, tvDataDict):
	for sName in tvDataDict:
		if candidate in sName:
			return [sName, float(tvDataDict[sName][0]), tvDataDict[sName][1]]
	return [candidate, -1, -1]

def writeToXLS(content, fileName):
    workbook = xlwt.Workbook(encoding='utf-8')
    booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)
    for i, rowVal in enumerate(content):
        for j, colVal in enumerate(rowVal):
            booksheet.write(i, j, colVal)
    workbook.save('%s.xls' % fileName)
    return

def handZYHaoPingBang(url, candidates, fileName):
	tvNameScoreURL = []
	tvDataDict = getTVDataDict(url)
	for candidate in candidates:
		print(candidate)
		tvNameScoreURL.append(getTVNameScoreURL(candidate, tvDataDict))
	writeToXLS(tvNameScoreURL, fileName)
	return

candidates = []
for line in open("DramaRank.txt"):
	candidates.append(re.sub('[\n]','',line))
print(candidates)
url = 'https://movie.douban.com/j/search_subjects?type=tv&tag=国产剧&sort=time&page_limit=100'
handZYHaoPingBang(url, candidates, 'DramaHaoPingBang')
