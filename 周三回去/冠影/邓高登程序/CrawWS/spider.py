# coding=utf-8
# 2017年10月12日 下午7:11
# author:Gordon Deng


import requests, re, json,xlwt
import time
from requests.exceptions import RequestException
import json


def get_onepage(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('Error:Get_onepage')
        return None

def get_newsnum(url):
    html = get_onepage(url)
    time.sleep(10)
    pattern = re.compile('<div class="mun">找到约(.*?)条结果<!--resultbarnum', re.S)
    newsnum = re.findall(pattern, html)
    if newsnum == []:
        return 0
    else:
        return int(newsnum[0].replace(',', ''))


def writeto_xls(title, playnum, fileName):
    workbook = xlwt.Workbook(encoding='utf-8')
    booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)
    for i in range(len(title)):
        booksheet.write(i, 0, title[i])
        booksheet.write(i, 1, playnum[i])
        booksheet.write(i, 2, 'Youku')
    workbook.save('%s.xls' % fileName)


def main():
    stars = ['鹿晗', '迪丽热巴', '薛之谦', '周莹', '陈学冬', '毛晓彤', '陈晓', '古力娜扎', '张艺兴', '王俊凯', '陈翔', '胡歌', '杨幂', '李易峰', '易烊千玺', '郑爽', '杨洋', '潘粤明', 'angelababy', '徐冬冬', '吴磊', '周杰伦', '刘亦菲', '刘涛', '范冰冰', '邓超', '王源', '李钟硕', '唐纳德·特朗普', '黄子韬', '陈奕迅', '周冬雨', '王珂', '沈腾', '李晨', '江疏影', '白敬亭', '李沁', '张一山', '靳东', '陈伟霆', '宋祖儿', '张翰', '李刚', '马丽', '木村拓哉', '国庆', '张碧晨', '王鸥', '艾伦', '关晓彤', '吴亦凡', '赵丽颖', '阚清子', '孙俪', '任重', '景甜', '刘德华', '新垣结衣', '陈小春', '周星驰', '吴京', '汪苏泷', '郭德纲', '唐嫣', '成龙', '欧阳靖', '杨紫', '张雪迎', '梁缘', '缝纫机乐队', '郭沁', '毛不易', '冯提莫', 'tfboys', '吴世勋', '少女时代', '张子枫', '华晨宇', '王菲', '张国荣', '无印良品', '俞灏明', '鞠婧祎', '乔欣', '周柏豪', '谢霆锋', '宋茜', '林俊杰', '尹正', '张学友', '汪峰', '邓伦', '孙怡', '平安', '林允儿', '张杰', '高晓松', '潘玮柏', '乔任梁']
    newsnum = []
    for star in stars:
        url = 'http://weixin.sogou.com/weixin?p=01030402&query=' + star + '&type=2&ie=utf8'
        print(url)
        num = get_newsnum(url)
        print(num)
        newsnum.append(num)
    writeto_xls(stars, newsnum, 'StarTrend')


main()

