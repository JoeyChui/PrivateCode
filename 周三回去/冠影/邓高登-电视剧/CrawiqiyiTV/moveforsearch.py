# coding=utf-8
# 2017年8月29日 上午8:55
# author:Gordon Deng
#With Chrome

import json
import pymongo
import re
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from pyquery import PyQuery as pq
from config import *
from time import sleep
from urllib.parse import urlencode
import requests
from requests.exceptions import RequestException


client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

browser = webdriver.Chrome()    #用浏览器模拟
# driver = webdriver.PhantomJS(executable_path=r'/Users/gordon/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs')#驱动搞死人别带后缀.exe，因为已经内含
# browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)  #change for webdriver.PhantomJS
browser.maximize_window()
wait = WebDriverWait(browser, 10)

def search(item):
    try:
        browser.get('http://index.iqiyi.com/')
        input = wait.until(
            ec.presence_of_element_located((By.CSS_SELECTOR,'body > div > div:nth-child(2) > div > div > div > div.chart_sear.clearfix > div > div > div > div > input'))

        )
        submit = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'body > div > div:nth-child(2) > div > div > div > div.chart_sear.clearfix > div > div > div > a')))

        input.send_keys(item)
        # print("输进去了")
        sleep(2)
        submit.click()
        sleep(2)
        page_url = browser.current_url
        pattern = re.compile('http://index.iqiyi.com/.*?aid=(\d+)', re.S)
        page_id = re.findall(pattern, page_url)
        # print(page_url)
        # print(page_id)
        html = get_page(page_id[0])             #记得是数组
        # print(html)
        merge_data(html)
        # parse_page(get_page(page_id[0]))
        # for xpx in range(60,960,30):
        #     get_nums(xpx)
        #     sleep(1)
        #     cut_nums(KEYWORD)

        # get_nums(60)
        # sleep(5)
        # cut_nums(KEYWORD)

    except TimeoutException:
        return search(item)


def get_nums(xpx):
    submit_30 = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'body > div > div:nth-child(2) > div > div > div:nth-child(2) > div > div > div:nth-child(2) > div > div:nth-child(1) > div.playVideoData.mt20 > div.switchoverBtn > a:nth-child(3)')))
    submit_30.click()
    sleep(2)
    canvas_position = browser.find_element_by_xpath('//*[@id="playTrendBar"]')
    # rightclick_btn = browser.find_element_by_css_selector('#playTrendBar > div:nth-child(1) > canvas')
    action = ActionChains(browser)
    action.move_to_element_with_offset(canvas_position, xpx, 296).click().perform()  #60开始br
    # sleep(6)

    # html = browser.page_source
    #
    # doc = pq(html)
    # items = doc('#playTrendBar > div:nth-child(2) > p:nth-child(2) > span:nth-child(2)').items()
    # print(html)
    #
    # for item in items:
    #     data = {
    #         'num': item.find('.span').text()
    #
    #     }
    #     print(data)

def cut_nums(name):
    imgelement = browser.find_element_by_css_selector('#playTrendBar > div:nth-child(2)')
    locations = imgelement.get_attribute()
    print(locations)

    sizes = imgelement.size
    print(sizes)

    if len(name) !=0 :
        rangle = (int(locations['x'] + sizes['width']*float((len(name)*0.35+0.3)/5.3)), int(locations['y'] + sizes['height']/2), int(locations['x'] + sizes['width']*(1.0-float((len(name)*0.35+0.3)/5.2)) + 100), int(locations['y'] + sizes['height']) + 100)

    print(rangle)
    browser.save_screenshot('test.png')
    img = Image.open('test.png')
    jpg = img.crop(rangle)
    jpg.save('test.png')
    # canvas_position_2 = browser.find_element_by_xpath('//*[@id="playTrendBar"]')
    # action = ActionChains(browser)
    # action.move_to_element_with_offset(canvas_position_2, int(locations['x'] + sizes['width']*float((len(name)*0.35+0.3)/5.3)), int(locations['y'] + sizes['height']/2)).conclick().perform()
    # action.move_to_element_with_offset(canvas_position_2, int(locations['x'] + sizes['width']*float((len(name)*0.35+0.3)/5.3)), int(locations['y'] + sizes['height']/2)).conclick().perform()


def get_page(offset):
    url = 'https://uaa.if.iqiyi.com/video_index/v2/get_index_trend?album_id=' + str(offset) +'&time_window=30'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('Error for get_page')
        return None

def merge_data(html):
    pattern_names = re.compile('"names":\["(.*?)"\],', re.S)
    pattern_ids = re.compile('"ids":\[(\d+)\],', re.S)
    pattern_data = re.compile('"data":\[(.*?)\],"name"', re.S)
    pattern_playtime = re.compile('"playtime":\[(.*?)\]\}', re.S)
    details_namess = re.findall(pattern_names, html)
    details_ids = re.findall(pattern_ids, html)
    details_data = re.findall(pattern_data, html)
    data_arr = details_data[0].split(',')
    details_playtime = re.findall(pattern_playtime, html)
    play_arrs = details_playtime[0].split(',')
    play_arr = []
    for i in range(len(play_arrs)):        #神坑2：有些电视剧频没有30个，直接指定30会过界
        play_arr.append(play_arrs[i].strip('\"'))
    print(details_namess)
    print(data_arr)
    print(play_arr)


def main():
    print("Start")
    browser.maximize_window()
    f = open('TvRange.txt')
    for KEYWORD in f.readlines():     #神坑1：文本中如果有换行符号需要取出，否者会和点击提交冲突
        KEYWORD = KEYWORD.strip('\n\"')
        search(KEYWORD)
    # for url in parse_page(get_page(206302301)):
    #     print(url)
    print("end")
    # print(len(KEYWORD))


if __name__ == '__main__':
    main()


