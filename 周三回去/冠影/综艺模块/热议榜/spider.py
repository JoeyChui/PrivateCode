
import json, xlrd, xlwt, crawlWeiZS


def crawlWeiZSHotZT(header, keywords, sDate, eDate):
    weiZSHotZT = {}
    for keyword in keywords:
        print('crawlWeiZSHotZT', keyword)
        hotZT = crawlWeiZS.getWeiZSHotZT(header, keyword, sDate, eDate)
        weiZSHotZT[keyword] = hotZT
    return weiZSHotZT

def getNameDate(file):
	tvNameDate = {}
	tvNameList, tvDateList = readFromXLS(file)
	for keyword in keywords:
		tempDateList = []
		for ii, tvName in enumerate(tvNameList):
			if keyword in tvName:
				date = int(tvDateList[ii])
				if date not in tempDateList:
					tempDateList.append(int(tvDateList[ii]))
		tvNameDate[keyword] = tempDateList
	return tvNameDate

def figurePhaseReYiGrade(weiZSVaule, date1, date2):
	vauleSum = 0
	for item in weiZSVaule:
		if date1 <= item[0] <= date2:
			vauleSum =  vauleSum + int(item[1])
	return int(vauleSum / (date2 - date1 + 1) * 20)

def tvNameHander(tvName):
    if tvName == '':
        return "mriasdgadfgadfgadfadfg"
    if tvName[0] == '第':
        return tvName
    if '（' in tvName:
        tvName = tvName[:tvName.find('（')]
    if '(' in tvName:
        tvName = tvName[:tvName.find('(')]
    if ' ' in tvName:
        tvName = tvName[:tvName.find(' ')]
    if '第' in tvName:
        tvName = tvName[:tvName.find('第')]
    if '：' in tvName:
        tvName = tvName[:tvName.find('：')]
    while tvName[-1].isdigit():
        tvName = tvName[:-1]
    return tvName
'''
def readFromXLS(file):
	xlsFile = xlrd.open_workbook(file)
	table = xlsFile.sheets()[0]
	tvNameList = table.col_values(0)
	tvDateList = table.col_values(2)
	return tvNameList, tvDateList
'''
def readFromXLS(file):
    xlsFile = xlrd.open_workbook(file)
    table = xlsFile.sheets()[0]
    tvNameList = table.col_values(0)
    return tvNameList

def writeToXLS(content, filename):
	workbook = xlwt.Workbook(encoding = 'utf-8')
	booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok = True)
	for i, rowVal in enumerate(content):
		for j, colVal in enumerate(rowVal):
			booksheet.write(i, j, colVal)
	workbook.save('%s.xls' % filename)
	return


header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36",
          "Referer": "http://data.weibo.com/index?sudaref=www.google.com"}
          #"Referer": "http://data.weibo.com/index/hotword?wid={}&wname={}".format(wid, keyword)
cookie = {"Cookie": 'SINAGLOBAL=9593676043677.764.1512397399492; SCF=Aq7YX9XtP9dpcKHI5mhPhhh0lHvVJ-oZtNdj1soOvY2j6keICzB0pwgv0jS2yZaePItCRqfMPiT2ecRsOOL4t8k.; SUHB=0h150JzumyJkzk; ALF=1544001250; SUB=_2AkMtGD09f8NxqwJRmPEWyWrqa4l0zw3EieKbRMzmJRMxHRl-yT9kqkgLtRB6BpgQPAqirEDVY709sspAfDkeK1bbeitk; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WhKMK7JPLUUvlvAyubBex1v; WEB3=16eecaac1b039ffa98ceae90acb175f9; WBStorage=c1cc464166ad44dc|undefined; _s_tentry=www.baidu.com; UOR=www.baidu.com,bang.weibo.com,www.baidu.com; Apache=2150166840655.1433.1514610546674; ULV=1514610546684:5:5:2:2150166840655.1433.1514610546674:1514451428930; PHPSESSID=5negdul8714ndu2o8209qk39i3'}


file, wtFilename = 'candidates-20171216-20171229.xls', '综艺热议榜-20171001-20171027'
sDate, eDate = "2017-12-29", "2017-12-22"

keywords = []
tvNameList = readFromXLS(file)
for ii in range(len(tvNameList)):
	tvNameList[ii] = tvNameHander(tvNameList[ii])
	if not tvNameList[ii] in keywords:
		keywords.append(tvNameList[ii])
keywords = keywords[:51]
print(keywords, len(keywords))


weiZSNameDateVaule = crawlWeiZSHotZT(header, keywords, sDate, eDate)
print(123, weiZSNameDateVaule)
exit()
tvNameDate = getNameDate(file) # XLS文件应按日期降序排列
print('ok')
tvReYiGrade = []

for tvName in tvNameDate:
	print(tvName)
	date1 = tvNameDate[tvName].pop(0)
	while True:
		if tvNameDate[tvName] == []:
			date2 = date1 #小问题
			tvPhaseReYiGrade = figurePhaseReYiGrade(weiZSNameDateVaule[tvName], date1, date2)
			tvReYiGrade.append([tvName, date1, tvPhaseGrade])
			break
		else:
			date2 = tvNameDate[tvName].pop(0)
			tvPhaseGrade = figurePhaseReYiGrade(weiZSNameDateVaule[tvName], date1, date2)
			tvReYiGrade.append([tvName, date1, tvPhaseGrade])
			date1 = date2
writeToXLS(tvReYiGrade, wtFilename)
