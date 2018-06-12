#从猫眼爬取基本的信息，如日期和类型
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

def downloader(url):
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Cookie':'_lxsdk=15cc4502029c8-0e395c2ae21066-474f0820-144000-15cc4502029c8; __utma=17099173.1954679609.1497942205.1500799015.1502529600.32; __utmz=17099173.1497942205.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; uuid=1A6E888B4A4B29B16FBA1299108DBE9CCD6D410DA635E16162C1736AD0F38669; _lx_utm=utm_source%3Dbaidu%26utm_medium%3Dorganic; __mta=142924426.1497947893134.1509101370839.1509102875082.159; _lxsdk_s=fbde297a3368d528331ed64847f3%7C%7C17',
        'Host':'maoyan.com',
        'Referer': 'http://maoyan.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest',
    }
    res = requests.get(url, headers)
    return res

def getdate():
    #old = open_workbook('2017.xls')
    old = open_workbook('20170630_date.xls')
    book_old = old.sheet_by_index(0)

    new = copy(old)
    book_new = new.get_sheet(0)
    #book.write(0,0,'year')
    #book.write(1,1,'name')
    book_new.write(0,2,'release_date')
    book_new.write(0, 3, 'duration')
    i = 0  #从哪一行开始
    err = open("error4.txt","a",encoding="utf8")
    err.write("456\n")
    err.close()
    for movie in book_old.col_values(1,1):
        err = open("error4.txt", "a", encoding="utf8")
        sleep(3)
        i = i + 1
        #print(movie)
        movie = str(movie)
        flag = 0
        if movie == "201413.0":
            movie = "201413"
        #url = "http://maoyan.com/query?kw="+movie
        url = "http://maoyan.com"
        res = downloader(url)
        page = etree.HTML(res.text)
        print(res.text)
        try:
            info = page.xpath('//div[@class="channel-detail movie-item-title"]')[0]
            title = info.xpath('a/text()')[0]
            print(title,movie)

            if title == movie: #第一次便匹配成功
                date = page.xpath('//div[@class="movie-item-pub"]/text()')[0]
                detail_url = "http://maoyan.com/"+info.xpath('a/href()')[0]
                print(detail_url)
                res1 = downloader(detail_url)
                page1 = etree.HTML(res1.text)
                info1 = page1.xpath('//li[@class="ellipsis"]/text()')[1]
                print(info1)
                duration = re.findall('(\d+)分钟',info1)

                print(date)
                print(duration)
                book_new.write(i, 2, date)
                book_new.write(i, 3, duration+"分钟")
                new.save("20170630_date.xls")
            else: #第一个匹配不成功
                #book_new.write(i,2,'incorrect')
                #deleteset = string.punctuation
                #movie.translate(str.maketrans('','',string.punctuation)) #名字中去掉空格
                #movie.replace('“',"")
                print(movie + "before: ")
                movie = re.sub("[“”：:  ·—。！？-]","",movie)
                movie = re.sub("II","2",movie)
                movie = re.sub("III", "3",movie)
                print(movie+ "after.\n")
                #movie.replace("II","2")
                #movie.replace("III", "3")
                length = len(page.xpath('//div[@class="channel-detail movie-item-title"]'))
                for j in range(0,length):
                    info = page.xpath('//div[@class="channel-detail movie-item-title"]')[j]
                    title = info.xpath('a/text()')[0]
                    #title.translate(str.maketrans('','',string.punctuation))
                    title = re.sub("[“”：:  ·—。！:？-]","",title)
                    movie = re.sub("II", "2", movie)
                    movie = re.sub("III", "3", movie)
                    print(title, movie,j)
                    if movie == title:
                        flag = 1
                        date = page.xpath('//div[@class="movie-item-pub"]/text()')[j]
                        print(date)
                        book_new.write(i, 2, date)
                        detail_url = "http://maoyan.com/" + info.xpath('a/href()')[j]
                        res1 = downloader(detail_url)
                        page1 = etree.HTML(res1.text)
                        info1 = page1.xpath('//li[@class="ellipsis"]/text()')[1]
                        print(info1)
                        duration = re.findall('(\d+)分钟', info1)

                        print(date)
                        print(duration)
                        book_new.write(i, 2, date)
                        book_new.write(i, 3, duration + "分钟")
                        new.save("20170630_date.xls")
                        new.save("20170630_date.xls")
                        break

                if flag == 0: #如果遍历一遍找不到，还是采取第一个
                    #print("no movie " + movie + "\n")
                    #book_new.write(i, 2, 'incorrect')
                    date = page.xpath('//div[@class="movie-item-pub"]/text()')[0]
                    print(date)
                    detail_url = "http://maoyan.com/" + info.xpath('a/href()')[0]
                    res1 = downloader(detail_url)
                    page1 = etree.HTML(res1.text)
                    info1 = page1.xpath('//li[@class="ellipsis"]/text()')[1]
                    print(info1)
                    duration = re.findall('(\d+)分钟', info1)

                    print(date)
                    print(duration)
                    book_new.write(i, 2, date)
                    book_new.write(i, 3, duration + "分钟")
                    new.save("20170630_date.xls")
                    book_new.write(i, 2, date)
                    new.save("20170630_date.xls")
                    str1 = title + " " + movie + " " + str(i) + "\n"
                    err.write(str1)
                    print("record.\n")

        except Exception as e:
            print(e)
            print("no such movie "+movie+"\n")
            book_new.write(i,2,'无')
            book_new.write(i, 3, '无')
            new.save("20170630_date.xls")
            str1 = movie + " " + str(i) + "\n"
            err.write(str1)

            print("recorded.\n")

    err.close()
    new.save("20170630_date.xls")

getdate()