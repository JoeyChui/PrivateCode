#-*-coding:utf-8-*- 
#2017-9-15 JoeyChui sa517045@mail.ustc.edu.cn

import re, requests, xlwt, json
from requests.exceptions import RequestException
#from time import sleep

def getOnePage(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
    	print('ER:getOnePage')
    	return None

def getTVBasic(url):
	html = getOnePage(url)
	pattern = re.compile('href="//v.youku.com/v_show/id_(\w+==)\.html.*?_src="(http://.*?)".*?alt="(.*?)".*?ibg"></i><span>(.*?)</span>.*?yk-col4 mr1', re.S)
	items = re.findall(pattern, html)
	for item in items:
		tvDate = re.findall('(\d\d)-(\d\d)', item[3])
		if tvDate != []:
			tvDate = int('2017' + str(tvDate[0][0]) + str(tvDate[0][1]))
		else:
			tvDate = item[3]
		print(item[2], tvDate)
		yield [item[2], tvDate, item[0], 'http://v.youku.com/v_show/id_'+item[0]+'.html', item[1]]

def getTVID(url):
	html = getOnePage(url)
	pattern = re.compile('subtitle" title="(.*?)">.*?videoId:"(\d+).*?showid:"(\d+)', re.S)
	items = re.findall(pattern, html)
	if items != []:
		tvName, videoID, showID = items[0]
		return tvName, int(videoID), int(showID)
	else:
		return -1, -1, -1

def wipeComma(string):
	while (',' in string):
		pos = string.find(',')
		string = string[:pos] + string[pos+1:]
	return string

def getTVDisCnt(videoID, showID):
	if videoID == -1:
		return -1, -1, -1
	url = 'http://v.youku.com/action/getVideoPlayInfo?beta&vid={}&showid={}&param%5B%5D=updown&callback=tuijsonp5'.format(videoID, showID)
	html = getOnePage(url)
	upCount, downCount, displayCount = re.findall('up":"([,\d]+).*?down":"([,\d]+).*?vv":"([,\d]+)', html)[0]
	upCount = wipeComma(upCount)
	downCount = wipeComma(downCount)
	displayCount = wipeComma(displayCount)
	return int(upCount), int(downCount), int(displayCount)

def getTVDetail(tvBasic):
	for item in tvBasic:
		tvName, videoID, showID = getTVID(item[3])
		upCount, downCount, displayCount = getTVDisCnt(videoID, showID)
		yield [item[0], tvName, item[1], upCount, downCount, displayCount, videoID, item[2], showID, item[3], item[4], 'YouKu']

def writeToTXT(content, fileName):
    with open('%s.txt' % fileName, 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()
    return

def writeToXLS(content, fileName):
	workbook = xlwt.Workbook(encoding='utf-8')
	booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)
	for i, rowVal in enumerate(content):
		for j, colVal in enumerate(rowVal):
			booksheet.write(i, j, colVal)
	workbook.save('%s.xls' % fileName)
	return

def judgeDate(tvDate, startDate, endDate):
	if not str(tvDate).isdigit():
		return True
	if startDate <= tvDate <= endDate:
		return True
	return False

def crawlYouKuZY(page):
	SEEDURL = 'http://list.youku.com/category/show/c_85_s_6_d_1_p_%s' % page
	#STARTDATE, ENDDATE = 20170800, 20170910
	tvBasic = getTVBasic(SEEDURL)
	tvDetail = getTVDetail(tvBasic)
	writeToXLS(tvDetail, 'YoukuZY%s' % page)


crawlYouKuZY(10) # start from 0
