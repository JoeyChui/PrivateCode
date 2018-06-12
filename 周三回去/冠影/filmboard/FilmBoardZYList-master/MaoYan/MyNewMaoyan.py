
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

def getOneHtml(url):
	counter = 1
	while True:
		response = requests.get(url)
		if response.status_code == 200:
			print('2@OK:getOneHtml')
			return response.text

		print('1@ER:getOneHtml, %d.Trying again!', counter)
		counter += 1
		if counter > 10:
			print('ER times over 10.exit!')
			exit(0)

def matchMovieID(html):
	pat = re.compile('movieId:(\d+)}"')
	items = re.findall(pat, html)
	return items

def matchEotFile(html):
	pos = html.find('eot', 1)
	temp = html[pos-100:pos+3]
	eotFileURL = 'http:' + temp[temp.find('//p1', 1):]
	return eotFileURL

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
	eotText = getOneHtml(eotFileURL)
	secretKey = getSecretKey(eotText)
	print(secretKey)

	#get film information
	filmBasicInfo = matchFilmBasicInfo(html)
	print(filmBasicInfo)
	matchFilmScore(html)
	matchFilmBoxOffice(html)

def getMovieID(url, offset):
	html = getOneHtml(url + str(offset))
	movieIDs = matchMovieID(html)
	return movieIDs

def getOneFilm(movieID):
	url = 'http://maoyan.com/films/' + str(movieID)
	while True:
		html = getOneHtml(url)
		result = parseOneHtml(html)
		if not result == '1@ER:matchEotFile':
			break
		time.sleep(2)

def main(url, offset):
	movieIDs = getMovieID(url, offset)
	for movieID in movieIDs:
		getOneFilm(movieID)
		time.sleep(5)

'''
url = 'http://maoyan.com/films?offset='
offset, end = 30, 30
while offset <= 30:
	print(offset, '*******************************************************************************************')
	main(url, offset)
	offset += 30
'''

getOneFilm(343945)
