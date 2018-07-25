#猫眼电影实时爬取
import os
import requests
import json
import time 
import csv

#链接url
def get_to_link():
    try:
        r = requests.get("https://box.maoyan.com/promovie/api/box/second.json")
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("链接错误！！！")
        return ''

#json化字符串
def json_text(text):
    jd = json.loads(text)
    return jd

#返回实时日期
def date_time(jd):
    ja = jd['data']
    date = ja['queryDate']#返回日期
    alltime = ja['updateInfo'].split()[1]#返回时间
    money = ja['totalBox'] + ja['totalBoxUnit']#返回总票房
    return date,alltime,money

#返回影片票房
def movie_price(jd):
    jl = jd['data']['list']
    for i,jls in enumerate(jl,1):
        name = jls['movieName']#影片名
        try:
            days = jls['releaseInfo'][2]#上映时间
        except:
            days = '点映'
        totalmoney = jls['sumBoxInfo']#影片总票房
        mainmoney = jls['boxInfo']#综合票房
        moneyrate = jls['boxRate']#票房占比
        shownumber = jls['showInfo']#排片场次
        showrate = jls['showRate']#排片占比
        people = jls['avgShowView']#场均人次
        showpeople = jls['avgSeatView']#上座率
        
        yield i,name,days,totalmoney,mainmoney,moneyrate,shownumber,showrate,people,showpeople

#创建文件夹
def makeasocket(path):
    if not os.path.exists(path):
        os.makedirs(path)
    
#保存到csv中
def save_to_csv(path,date,alltime,moeny,movie_price):
    with open(path + '猫眼电影专业版实时数据.csv','a') as f:
        writer = csv.writer(f)
        writer.writerow(['日期',date,'','时间',alltime,'','总票房',moeny])
        writer.writerow(['排名','影片名','上映时间(/天)','影片总票房','综合票房(/万)','票房占比(%)','排片场次','排片占比(%)','场均人次','上座率(%)'])
        for movie in movie_price:
            writer.writerow([movie[0],movie[1],movie[2],movie[3],movie[4],movie[5],movie[6],movie[7],movie[8],movie[9]])



def main():
    path = 'D:/数据/猫眼电影专业版数据/'
    makeasocket(path)
    while True:  
        text = get_to_link()
        jd = json_text(text)
        date,alltime,moeny = date_time(jd)
        print('***'*46)
        print('{:>10s}:{}{:>10s}:{}{:>10s}：{}'.format('日期',date,'时间',alltime,'总票房',moeny))
        print('---'*46)
        print('{:^6s}{:^20s}{:^10s}{:^12s}{:^12s}{:^10s}{:^10s}{:^6s}{:^6s}{:^6s}'.format('排名','影片名','上映时间(/天)','影片总票房(/亿)','综合票房(/万)','票房占比(%)','排片场次','排片占比(%)','场均人次','上座率(%)'))
        print('---'*46)
        for movie in movie_price(jd):
            print('{:^6d}{:^20s}{:^20s}{:^20s}{:^12s}{:^11s}{:^13s}{:^10s}{:^10s}{:^10s}'.format(movie[0],movie[1],movie[2],movie[3],movie[4],movie[5],movie[6],movie[7],movie[8],movie[9]))
            print('---'*46)
        save_to_csv(path,date,alltime,moeny,movie_price(jd))
        time.sleep(3)

if __name__ == "__main__":
    main()