#直接从微票网站获取一个月的排行

import requests
import json
import xlwt
from lxml import etree
import random
from time import sleep
import re

def downloader1(url,begin,end):
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/56.0.2924.87 Safari/537.36',
        'origin':'https://piaofang.wepiao.com',
        'Content-Type':'application/json',
        'Referer': 'https://piaofang.wepiao.com/?dateStart=2017-07-01&dateEnd=2017-07-31&scheduleState=month&firstTier=0&secondTier=0',
        'Cookie':'_gat=1; _ga=GA1.3.380216471.1500799481; _wp_uid_=03bcba80-8c88-4102-afb6-177e71f32241'
    }
    payload = {
               'movieFilter':{'showDateFrom':begin,'showDateTo':end,'sortType':'desc'},
               'paging':{'pageSize':10},
               'lang':'cn',
    }
    payload = json.dumps(payload)
    res = requests.post(url,data=payload,headers=headers)
    return res

def downloader2(url,begin,end):
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/56.0.2924.87 Safari/537.36',
        'origin':'https://piaofang.wepiao.com',
        'Content-Type':'application/json',
        'Referer': 'https://piaofang.wepiao.com/?dateStart=2017-07-01&dateEnd=2017-07-31&scheduleState=month&firstTier=0&secondTier=0',
        'Cookie':'_gat=1; _ga=GA1.3.380216471.1500799481; _wp_uid_=03bcba80-8c88-4102-afb6-177e71f32241'
    }
    payload = {
               'movieFilter':{'showDateFrom':begin,'showDateTo':end,'sortType':'desc'},
               'paging':{'pageSize':50},
               'lang':'cn',
    }
    payload = json.dumps(payload)
    res = requests.post(url,data=payload,headers=headers)
    return res

def getmonthrank():
    url = "https://piaofang.wepiao.com/api/v1/index"
    begin = "2017-07-01"
    end = "2017-07-31"
    res = downloader1(url,begin,end)
    #print(res.text)
    top = re.findall('"movieName":"(.+?)"',res.text)[:10]
    print(top)
    aa = open("boxrank.txt","a",encoding="utf8")
    for i in range(0,10):
        aa.write("\n")
        aa.write(top[i])
    res = downloader2(url, begin, end)
    #print(res.text)
    all = re.findall('"movieName":"(.+?)"', res.text)
    print(all)
    bb = open("moviecandidates.txt", "a", encoding="utf8")
    for i in range(0, len(all)):
        bb.write("\n")
        bb.write(all[i])

getmonthrank()