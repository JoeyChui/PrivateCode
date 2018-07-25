# coding=utf-8
# 2017年9月23日 下午10:03
# author:Gordon Deng

import json, xlwt
from spider import *

def readWeiZSVaule(fileName):
	with open('%s.txt' % fileName, 'r', encoding='utf-8') as f:
		weiZSVaule = f.read()
		f.close()
	return json.loads(weiZSVaule)

def figureReYiGrade(weiZSVaule, name, date, date2):
	n = date2 - date + 1
	tvPhaseGrade = 0
	while date <= date2:
		tvPhaseGrade =  tvPhaseGrade + int(weiZSVaule[name][str(date)])
		date += 1
	return int(tvPhaseGrade / n)

def writeToXLS(content, fileName):
	workbook = xlwt.Workbook(encoding='utf-8')
	booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)
	for i, rowVal in enumerate(content):
		for j, colVal in enumerate(rowVal):
			booksheet.write(i, j, colVal)
	workbook.save('%s.xls' % fileName)
	return

def weiZSHander(tvNameDate, rdFileName, wtFileName):
	reYiGrade = []
	weiZSVaule = readWeiZSVaule(rdFileName)
	for name in tvNameDate:
		print(name)
		date1 = tvNameDate[name].pop(0)
		while True:
			if tvNameDate[name] == []:
				date2 = date1 + 1
				tvPhaseGrade = figureReYiGrade(weiZSVaule, name, date1, date2)
				reYiGrade.append([name, date1, tvPhaseGrade])
				break
			else:
				date2 = tvNameDate[name].pop(0)
			tvPhaseGrade = figureReYiGrade(weiZSVaule, name, date1, date2)
			reYiGrade.append([name, date1, tvPhaseGrade])
			date1 = date2
	writeToXLS(reYiGrade, wtFileName)
	return

tvNameDate = dict.fromkeys(list(weiZSData.keys()), [20170901, 20170908])
rdFileName = 'WeiZS-20170801-20170910'
wtFileName = '综艺热议榜-20170801-20170910'
weiZSHander(tvNameDate, rdFileName, wtFileName)
