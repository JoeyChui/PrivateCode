# coding=utf-8
# 2017年8月22日 上午11:55
# author:Gordon Deng
import pymongo
import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from config import *


client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

# browser = webdriver.Chrome()    #不用浏览器模拟
driver = webdriver.PhantomJS(executable_path=r'/Users/gordon/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs')#驱动搞死人别带后缀.exe，因为已经内含
browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)  #change for webdriver.PhantomJS
wait = WebDriverWait(browser, 10)

browser.set_window_size(1400, 900)




def search():
    print('Crawing     ')
    try:
        browser.get('https://www.taobao.com')
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#q'))#EC.presence_of_all_elements_located为数组，EC.presence_of_element_located为元素
        )

        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
        input.send_keys(KEYWORD)
        submit.click()
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total')))#括号别少
        get_products()#查找成功才执行
        return total.text

    except TimeoutException:
        return search()


def next_page(page_number):
    print('changing the page ', page_number)
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input'))
        )

        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        input.clear()
        input.send_keys(page_number)#传数字别传字符串
        submit.click()
        wait.until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(page_number)))
        get_products()#翻页成功才执行

    except TimeoutException:
        next_page(page_number)


def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()#items()得到所有选择内容
    for item in items:
        product = {
            'title': item.find('.title').text(),
            'price' : item.find('.price').text(),
        #抓class="price xxxxxxxxx"的话可以只能.porice
            'deal': item.find('.deal-cnt').text()[:-3],
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text(),
            'image' : item.find('.pic .img').attr('src')
        #img为独立标签，不是什么class
        #     attr(属性名) // 获取属性的值（取得第一个匹配元素的属性值。通过这个方法可以方便地从第一个匹配元素中获取一个属性的值。如果元素没有相应属性，则返回
        #     undefined ）

        }
        print(product)
        # save_to_mongo(product)


def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('Insert MongoDb Successfully', result)
    except Exception:
        print('Insert MongoDb Unsuccessfully', result)
    # browser.close()  #不用实体浏览器抓取的话，不用检测是否关闭

def main():
    try:
        total = search()
        total = int(re.compile('(\d+)').search(total).group(1))

        for i in range(2, total + 1):
            next_page(i)
    finally:             #无论异常与否
        browser.close()  #后来发现时close()放错位置


if __name__ == '__main__':
    main()