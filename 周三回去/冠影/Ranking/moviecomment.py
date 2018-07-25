#好评榜，从豆瓣、猫眼和娱票儿上分别获取分数，惊，豆瓣更新了
#猫眼太麻烦了，干脆放弃了
# -*- coding:utf-8 -*-
# coding = utf-8


import requests
import re
import json
import xlwt
from lxml import etree
import datetime
from time import sleep
import urllib
from selenium import webdriver
import time
from pymouse import PyMouse

def downloaderdouban(url):
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/56.0.2924.87 Safari/537.36',

        'Referer': 'http://www.douban.com',
    }
    res = requests.get(url, headers)
    return res

#豆瓣搜索页面更新，采用小孟建议，使用search_suggest获得链接
def getdoubanscore():
    f = open('moviecandidates.txt', 'r', encoding="utf8")
    name = f.readline().strip()
    result = []
    for line in f:
        sleep(3)
        name = line.strip()  # name是电影名
        print(name)
        if name == "":
            continue
        url = "https://movie.douban.com/j/subject_suggest?q=" + name
        res = downloaderdouban(url)
        res = json.loads(res.text)
        try:
            res = res[0]
        except Exception as e:
            print(e)
            score = 0
            result.append(0)
            break
        print(res)
        url = res["url"]
        url = url[:url.find('suggest')-1]
        #print(url)
        res = downloaderdouban(url)

        res = (res.text)
        selector = etree.HTML(res)
        try:
            score = selector.xpath("//strong[@property='v:average']/text()")
        except Exception as e:
            print(e)
            score = 0
        result.append(score[0])
        print(score)
    return result

def downloader(url):
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/56.0.2924.87 Safari/537.36',

        'Referer': 'https://piaofang.wepiao.com',
    }
    res = requests.get(url, headers)
    return res

def downloader1(url,movieid):
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/56.0.2924.87 Safari/537.36',
        'origin':'https://piaofang.wepiao.com',
        'Content-Type':'application/json',
        'Referer': 'https://piaofang.wepiao.com/movie/?id='+movieid+'&date=2017-03-31&from=/',
    }
    payload = {'id':movieid,
               'lang':'cn',
    }
    payload = json.dumps(payload)
    res = requests.post(url,data=payload,headers=headers)
    return res

def downloader2(url,name):
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/56.0.2924.87 Safari/537.36',
        'origin':'https://piaofang.wepiao.com',
        'Content-Type':'application/json',
        'Referer': 'https://piaofang.wepiao.com',
    }
    payload = {'name':name,
               'moviePaging':{'page':1,'pageSize':50},
               'cinemaPaging':{'page':1,'pageSize':50},
               'lang':'cn',
    }
    payload = json.dumps(payload)
    res = requests.post(url,data=payload,headers=headers)
    return res

def getwepiaoscore():
    f = open('moviecandidates.txt', 'r', encoding="utf8")
    name = f.readline().strip()
    result = []
    for line in f:
        sleep(3)
        name = line.strip()  # name是电影名
        print(name)
        if name == "":
            continue
        url = "https://piaofang.wepiao.com/api/cinemaMovieInfo/0/search"
        res = downloader2(url, name)
        res = res.text
        print(res)
        res = (json.loads(res))
        mid = res["movies"][0]["movieId"]
        mid = str(mid)
        url = "https://piaofang.wepiao.com/movie/?id="
        url += (mid)
        print(url)
        sleep(1)
        res = downloader(url)
        url = "https://piaofang.wepiao.com/api/v1/movie/detail"
        res = downloader1(url, mid)
        res = json.loads(res.text)
        score = (res["data"]["movie"]["score"])
        result.append(score)
    return(result)

def getmaoyanscore():
    f = open('moviecandidates.txt', 'r', encoding="utf8")
    name = f.readline().strip()
    result = []
    for line in f:
        sleep(3)
        name = line.strip()  # name是电影名
        print(name)
        if name == "":
            continue


# getdoubanscore()
#getwepiaoscore()

def cal():
    score_douban = getdoubanscore()
    score_wepiao = getwepiaoscore()
    f = open('moviecandidates.txt', 'r', encoding="utf8")
    print(len(f.readlines()))
    if len(score_douban) != len(score_wepiao):
        print("Score Error!\n")

cal()
