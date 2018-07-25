# coding=utf-8
# 2017年9月20日 下午7:33
# author:Gordon Deng

import requests, re, json,xlwt
import time
from requests.exceptions import RequestException
import json


dramalate = []
dramatitle = []
dramaplaynum = []

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
    detailhtml = get_onepage('http://list.youku.com/show/id_' + detailurl[0]+ '.html')
    # return detailhtml
    pattern2 = re.compile('</li><li>总播放数：(.*?)</li><li>评论', re.S)
    totalplaynum = re.findall(pattern2, detailhtml)
    return int(totalplaynum[0].replace(',', ''))



def get_drama_total(url):
    html = get_onepage(url)
    pattern = re.compile('<p class="tvintro"> 已完结 40集全 </p>', re.S)
    total = re.findall(pattern, html)
    return int(total[0])

#有些URL带http,有些不带，匹配的时候记得看，不看会2333333333333333333333333333

def get_drama_detail_bypage(url):
    html = get_onepage(url)
    pattern = re.compile('<div class="site-piclist_pic">.*?href="(.*?)".*?class="site-piclist_pic_link".*?target=', re.S)
    pageurl = re.findall(pattern, html)
    for i in range(len(pageurl)):
        dramalate.append(str(pageurl[i]))
    pattern2 = re.compile('<div class="site-piclist_pic">.*?title="(.*?)".*?class="site-piclist_pic_link".*?target=', re.S)
    pagetitle = re.findall(pattern2, html)
    for j in range(len(pagetitle)):
        dramatitle.append(pagetitle[j])

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
    print(title[0])
    return title[0]


def get_drama_playnum(url):
    html = get_onepage(url)
    pattern = re.compile('albumId: (\d+),', re.S)
    albumId = re.findall(pattern, html)
    if albumId == []:
        return 0
    else:
        html = get_onepage('http://cache.video.iqiyi.com/jp/pc/' + albumId[0] + '/')
        pattern2 = re.compile(':(\d+)', re.S)
        playnum = re.findall(pattern2, html)
        return int(playnum[0])

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
        booksheet.write(i, 2, 'IQiYi')
    workbook.save('%s.xls' % fileName)


def main(pages):
    for page in range(1, pages+1):
        url = 'http://list.iqiyi.com/www/2/-------------4-' + str(page) + '-1-iqiyi--.html'
        get_drama_detail_bypage(url)
    for oneurl in dramalate:
        dramaplaynum.append(get_drama_playnum(oneurl))
        print(dramaplaynum)
    if len(dramatitle) == len(dramaplaynum):
        writeto_xls(dramatitle, dramaplaynum, 'IQiYiDrama')
    else:
        print('error: title don\'t match playnum')


main(7)


