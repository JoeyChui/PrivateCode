#生成榜单；首先从百度风云榜、微指数获得候选人；然后结合其他数据
#首先获取候选人近20条微博的热度；问题是 不是所有人都开了微博；有些人微博数过少，粉丝不停转发和评论同一条微博。（这条暂时不考虑了）
#获取候选人近一个月的百度指数
#获取候选人近一个月的微指数
#获取候选人微博话题
#所有数据保存在以日期命名的文件夹中;把一些文件拿过来，生成一些文件
#热度榜单

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

#从百度风云榜中抓人名

def candi():
    candidates = []
    headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/56.0.2924.87 Safari/537.36',
               'Referer': 'http://www.baidu.com/',
               }

    url = "http://top.baidu.com/buzz?b=618&c=9&fr=topbuzz_b17_c9"
    html = requests.get(url, headers)
    html.encoding = "gb2312"
    selector = etree.HTML(html.content)
    #print(html.content)
    starName1 = selector.xpath("//a[@class='list-title']/text()")
    #print(starName1)
    #candidates.append(starName)

    url = "http://top.baidu.com/buzz?b=18&c=9&fr=topbuzz_b618_c9"
    html = requests.get(url, headers)
    html.encoding = "gb2312"
    selector = etree.HTML(html.content)
    #print(html.content)
    starName = selector.xpath("//a[@class='list-title']/text()")
    starName2 = re.findall("list-title.+?>(.+)<",html.text)
    #print(starName)
    #candidates.append(starName)

    url = "http://top.baidu.com/buzz?b=17&c=9&fr=topbuzz_b18_c9"
    html = requests.get(url, headers)
    html.encoding = "gb2312"
    selector = etree.HTML(html.content)
    # print(html.content)
    starName = selector.xpath("//a[@class='list-title']/text()")
    starName3 = re.findall("list-title.+?>(.+)<", html.text)
    #print(starName)
    #candidates.append(starName)
    for name in starName1:
        if name not in candidates:
            candidates.append(name)

    for name in starName2:
        if name not in candidates:
            candidates.append(name)

    for name in starName3:
        if name not in candidates:
            candidates.append(name)
    print(candidates)
    aa = open("candi.txt","w",encoding="utf8")
    aa.write(candidates)
    aa.close()
    return candidates

def wbdownloader(url):
    cookie3 = {
        "Cookie": "_T_WM=7c5930258162fd8f073e9ecdd9190bb2; SUB=_2A250FV7VDeThGedG6FEX8C3Iyz6IHXVX9mKdrDV6PUJbkdBeLRntkW0WtcW-QY7RzMTWOCUAR11kW_sVEg..; SUHB=08JqqL49kwmUf3; SCF=AjJjBv-pUsOGtkW8JFo3haRdM9LVd-bosbMCu3nnzLc5gXJnEfzA0DemA9wmM7ja1xxtKJuHg76prQn-Cvj1maQ.; SSOLoginState=1494298245"}

    cookie2 = {
        "Cookie": "ALF=1499772633; SSOLoginState=1497180634; SCF=ApK1L_vhvYj6M87AX98Tz0BUGHkfFbzAa-6jG4QnKcUcEDYL2SRxXnXaCy8_LeiY0Di1YplQpVr00x8RgkmZW4I.; SUB=_2A250OVmKDeThGeNL4lsR9CbEzT-IHXVXwmfCrDV6PUNbktBeLWLXkW2AF-tC66ngua9TK_JXKdcBBSx2Mg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWCqVAQg2c2rMwAPfrsqYcc5JpX5KMhUgL.Fo-f1K.7ShnRSoe2dJLoIEBLxK-L1h-LB-zLxK-L12BLBKqLxKqLB-BLBKeLxK-LBK-LB.Bt; SUHB=0M2VuFAIWCRSg0; _T_WM=2d132a775ec8516db42e0357e80e4ed0"}

    cookie1 = {
        "Cookie": "ALF=1499744586; SCF=AvOZbZlloyrtrpmOsxChTRjnwm1oC1ew5W7EbJ_JNf9Kv9F9JQ8VpAh7QywIMC0nOIdEdt7pO-h7TGgl7wNU5E8.; SUB=_2A250OMwcDeThGeNJ6FsY8yvOwjuIHXVXwtRUrDV6PUJbktBeLWPfkW2heI6Uw_eBkNNS6qhmCzB1gZJL7g..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhT742wYZB6Z1WeU48AjcD35JpX5o2p5NHD95QfS0e41Kefeo.NWs4Dqcjdi--RiK.pi-20i--ciK.4i-zXi--fi-2XiKLh; SUHB=0cS3YWVS2qyAlP; SSOLoginState=1497152588; _T_WM=642b31423dfb19dca6900a57fc3e96fa"}
    t = random.uniform(0, 3)
    if t > 2:
        cookie = cookie2
    elif t > 1:
        cookie = cookie1
    else:
        cookie = cookie1

    headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/56.0.2924.87 Safari/537.36',
               'Referer': 'https://weibo.cn/',
               }
    html = requests.get(url, headers, cookies= cookie)
    return html



def weiboinf(candidates):  #需要考虑的点实在太多了，暂时不考虑
    weibopr = []
    bb = open("nouserid.txt","a",encoding="utf8")
    for name in candidates:
        aa = open("userid.txt", "r", encoding="utf8")
        aa.readline()
        sumf = 0
        suma = 0
        sumc = 0
        print(name)
        for ln in aa:
            flag = 0 #有没有找到
            [nameid,id] = ln.split(" ",maxsplit=1)
            id = id.strip()
            #print(ln)
            if name == nameid:
                flag = 1
                print(nameid,id)
                url = "https://weibo.cn/u/"+str(id)+"?filter=1&page=1"
                html = wbdownloader(url)
                html.encoding="utf8"
                html = html.text
                #print(html)
                #forward = re.findall("W_ficon ficon_forward S_ficon.+?<em>(\d+)",html)
                forward1 = re.findall("转发.(\d+)\W",html)
                agree1 = re.findall("赞.(\d+)\W",html)
                comment1 = re.findall("评论.(\d+)\W",html)
                #print(url)
                sleep(5)
                url = "https://weibo.cn/u/" + str(id) + "?filter=1&page=2"
                #print(url)
                html = wbdownloader(url)
                html.encoding = "utf8"
                html = html.text
                #print(html)
                forward2 = re.findall("转发.(\d+)\W", html)
                agree2 = re.findall("赞.(\d+)\W", html)
                comment2 = re.findall("评论.(\d+)\W", html)
                for i in range(0,len(forward1)):
                    sumf += int(forward1[i])
                    suma += int(agree1[i])
                    sumc += int(comment1[i])
                for i in range(0, len(forward2)):
                    sumf += int(forward2[i])
                    suma += int(agree2[i])
                    sumc += int(comment2[i])
                """
                print(forward1)
                print(agree1)
                print(comment1)
                print(forward2)
                print(agree2)
                print(comment2)
              """
                sumf = sumf/200000
                suma = suma/1000000
                sumc = sumc /200000
                #print(sumf)
                #print(suma)
                #print(sumc)
                sum = sumf + suma + sumc
                print(sum)
                sleep(5)
                weibopr.append(sum)
                break
        if flag == 0: #没有发现
            bb.write(name+"\n")

    return(weibopr)






if __name__ == '__main__':

    candidates = candi()
    #candidates = ['杨紫','黄子韬']
    #weibopr = weiboinf(candidates)
    #print(weibopr)
