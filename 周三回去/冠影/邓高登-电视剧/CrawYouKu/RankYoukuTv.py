# coding=utf-8
# 2017年9月12日 下午3:33
# author:Gordon Deng

import requests, re, json,xlwt
import time
from requests.exceptions import RequestException
import json


dramalate = []

def get_onepage(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('Error:Get_onepage')
        return None

def get_drama_totalplaynum(url):
    html = get_onepage(url)
    pattern = re.compile('<a class="desc-link.*?href=".*?//list.youku.com/show/id_(\w+).html".*?target="_blank">.*?</a>', re.S)
    detailurl = re.findall(pattern, html)
    if detailurl ==[]:
        return ' '
    detailhtml = get_onepage('http://list.youku.com/show/id_' + detailurl[0]+ '.html')
    # return detailhtml
    pattern2 = re.compile('</li><li>总播放数：(.*?)</li><li>评论', re.S)
    totalplaynum = re.findall(pattern2, detailhtml)
    if totalplaynum == []:
        return ' '
    return int(totalplaynum[0].replace(',', ''))



def get_drama_total(url):
    html = get_onepage(url)
    pattern = re.compile('<p class="tvintro"> 已完结 40集全 </p>', re.S)
    total = re.findall(pattern, html)
    return int(total[0])

#有些URL带http,有些不带，匹配的时候记得看，不看会2333333333333333333333333333

def get_drama_url_bypage(url):
    html = get_onepage(url)
    pattern = re.compile('<li class="yk-col4 mr1"><div class="yk-pack pack-film"><div class="p-thumb"><a href=".*?//(.*?)" title=".*?" target="_blank"></a><i class="bg"></i>', re.S)
    pageurl = re.findall(pattern, html)
    for i in range(len(pageurl)):
        dramalate.append('http://' + str(pageurl[i]))


def get_drama_allurl(url):
    allurl = []
    html = get_onepage(url)
    pattern = re.compile('div class="item.*?name="tvlist".*?item-id="item_(\w+==)" title="第', re.S)
    item_ids =re.findall(pattern, html)
    if isFirst(url):
        allurl.append(url)
        for i in range(int(get_drama_total(url))-1):
            allurl.append('http://v.youku.com/v_show/id_' + str(item_ids[i]) + '.html')

    else:
        for i in range(int(get_drama_total(url))):
            allurl.append('http://v.youku.com/v_show/id_' + str(item_ids[i]) + '.html')
    return allurl

def get_drama_allurl2(url):
    allurl = []
    html = get_onepage(url)
    pattern = re.compile('div class="item.*?name="tvlist".*?item-id="item_(\w+==)" title="第', re.S)
    item_ids =re.findall(pattern, html)
    print(len(item_ids))

def isFirst(url):
    html = get_onepage(url)
    pattern = re.compile('<span id="subtitle" title="第(\d+)集">.*?</span>', re.S)
    CurrentPlay = re.findall(pattern, html)
    if CurrentPlay[0] == get_drama_total(url):
        return 0
    else:
        return 1


def get_drama_ID(url):
    html = get_onepage(url)
    time.sleep(1)
    pattern = re.compile('subtitle" title=".*?videoId:"(\d+).*?showid:"(\d+)', re.S)
    items = re.findall(pattern, html)
    if items != []:
        videoID, showID = items[0]
        return int(videoID), int(showID)


def get_drama_title(url):
    html = get_onepage(url)
    time.sleep(1)
    pattern = re.compile('<a href="//tv.youku.com/" target="_blank">.*?</a><span>(.*?)</span>', re.S)
    title = re.findall(pattern, html)
    if title != []:
        print(title[0])
        return title[0]
    else:
        return 'No Title'


def get_drama_playnum(videoID, showID):
    url = 'http://v.youku.com/action/getVideoPlayInfo?beta&vid={}&showid={}&param%5B%5D=updown&callback=tuijsonp5'.format(
        videoID, showID)
    html = get_onepage(url)
    time.sleep(1)
    playnum = re.findall('up":".*?down":".*?vv":"([,\d]+)"', html)[0]
    return int(playnum.replace(',', ''))


def merge_playnum(urllist):
    totalplaynum = 0
    for i in range(get_drama_total(urllist[0])):
        videoID, showID = get_drama_ID(urllist[i])
        totalplaynum += get_drama_playnum(videoID, showID)
        print(get_drama_playnum(videoID, showID))
    print(totalplaynum)
    return totalplaynum


def writeto_xls(title, playnum, fileName):
    workbook = xlwt.Workbook(encoding='utf-8')
    booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)
    for i in range(len(title)):
        booksheet.write(i, 0, title[i])
        booksheet.write(i, 1, playnum[i])
        booksheet.write(i, 2, 'Youku')
    workbook.save('%s.xls' % fileName)


def main(pages):
    title = []
    playnum = []
    for page in range(1, pages+1):
        url = 'http://list.youku.com/category/show/c_97_s_6_d_1_p_' + str(page) + '.html'
        get_drama_url_bypage(url)
    for oneurl in dramalate:
        title.append(get_drama_title(oneurl))
        playnum.append(get_drama_totalplaynum(oneurl))
    writeto_xls(title, playnum, 'YoukuDrama')


main(4)