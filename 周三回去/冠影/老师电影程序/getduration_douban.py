#从艺恩爬取基本的信息，如日期和时长
#从给定的名单中
#对getdate.py的改进，遍历前十个query的结果，争取找到名字一模一样的

import re
import string
import sys
import os
import urllib
from bs4 import BeautifulSoup
import requests
from lxml import etree
import traceback
from time import sleep
import random
from xlrd import open_workbook
import xlwt
from datetime import datetime,timedelta
from xlutils.copy import copy
from time import sleep
import json

def downloader(url):
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Host':'www.douban.com',
        'Referer': 'https://movie.douban.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest',
    }
    res = requests.get(url, headers)
    return res

def getdate():
    #old = open_workbook('2017.xls')
    filename = "duration_date1.xls"
    #filename = "20170630_duration.xls"
    old = open_workbook(filename)
    book_old = old.sheet_by_index(0)

    new = copy(old)
    book_new = new.get_sheet(0)
    #book.write(0,0,'year')
    #book.write(1,1,'name')
    #book_new.write(0,2,'release_date')
    #book_new.write(0, 3, 'duration')
    i = 824 #从哪一行开始
    err = open("error4.txt","a",encoding="utf8")
    err.write("456\n")
    err.close()
    for movie in book_old.col_values(1,i):
        err = open("error4.txt", "a", encoding="utf8")
        sleep(3)

        #print(movie)
        movie = str(movie)
        flag = 0
        if movie == "201413.0":
            movie = "201413"
        url = "https://movie.douban.com/j/subject_suggest?q="+movie
        #url = "http://maoyan.com"
        res = downloader(url)  #获得json
        #page = etree.HTML(res.text)
        res = json.loads(res.text)
        """
        try:
            res = res[0]
        except Exception as e:
            print(e)
            break
        """
        if len(res)==0:
            print("no such movie "+movie+"\n")
            book_new.write(i,2,'无')
            book_new.write(i, 3, '无')
            new.save(filename)
            str1 = movie + " " + str(i) + "\n"
            err.write(str1)
            print("recorded.\n")
            i = i + 1
            continue

        for j in range(0,len(res)): #检测所有的名字，希望能发现最匹配；如果没有，那么使用第一个
            eps = (res[j])
            title = eps["title"]
            print(title,movie)
            if title == movie: #第一次匹配正确
                url = eps["url"]
                url = url[:url.find('suggest') - 1]
                flag = 1
                break

        if flag == 0: #没找到匹配，对搜索名字进行处理，并且遍历
            print(movie + "before: ")
            movie = re.sub("[“”：:  ·—。！？-]", "", movie)
            movie = re.sub("II", "2", movie)
            movie = re.sub("III", "3", movie)
            print(movie + "after.\n")
            for k in range(0,len(res)): #检测所有的名字，希望能发现最匹配；如果没有，那么使用第一个
                eps = (res[k])
                title = eps["title"]
                print(title,movie)
                if title == movie: #第一次匹配正确
                    url = eps["url"]
                    url = url[:url.find('suggest') - 1]
                    flag = 1
                    break

        if flag == 0: #仍然没有找到匹配，则使用第一个
            eps = res[0]
            url = eps["url"]
            url = url[:url.find('suggest') - 1]

        res = downloader(url)
        res = (res.text)
        selector = etree.HTML(res)

        try:
            duration = selector.xpath('//span[@property="v:runtime"]/text()')[0]
            date = selector.xpath('//span[@property="v:initialReleaseDate"]/text()')[0]
        except Exception as e:
            duration = "None"
            date = "None"
        print(date)
        print(duration)
        book_new.write(i, 2, date)
        book_new.write(i, 3, duration)
        new.save(filename)
        i = i + 1



    err.close()
    new.save(filename)

getdate()
