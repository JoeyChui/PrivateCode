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

candidates = ['开学第一课','中国有嘻哈','极限挑战','中国新歌声','明日之子','脱口秀大会','爸爸去哪儿','小手牵小狗','开心相对论','脑大洞开','中餐厅','我爱二次元','了不起的孩子','姐姐好饿','天使之路','快乐男声','我们来了','天使之路','大片起来嗨','大学生来了','集结吧王者']
url = 'https://movie.douban.com/j/search_subjects?type=tv&tag=综艺&sort=time&page_limit=100'
handZYHaoPingBang(url, candidates, 'ZYHaoPingBang')
