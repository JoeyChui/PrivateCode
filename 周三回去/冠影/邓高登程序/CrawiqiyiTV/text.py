import requests
from multiprocessing import Pool
from requests.exceptions import RequestException
import re
import json


import time
# from Download import Suprequest

def get_one_page(url):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

count = 0

def parse_one_page(html):
    global count
    time.sleep(5)    #延时应该放在这，等网页加载完再匹配
    pattern = re.compile('<p class="site-piclist_info_title ">.*?<a.*?pos=(\d+).*?title="(.*?)".*?.href="(.*?)".*?</a>', re.S)
    items = re.findall(pattern, html)
    # print(items)
    for item in items:
        print(item[1])
        write_to_file(item[1].strip('\"'))
        # yield {
        #     'index': count + int(item[0]),
        #     'title': item[1],
        #     'href': item[2]
        #     # 'actor': item[3].strip()[3:],
        #     # 'time': item[4].strip()[5:],
        #     # 'score': item[5]+item[6]
        # }

    count+=30

def write_to_file(content):
    with open('TvRange.txt', 'a', encoding='utf-8')as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()

def main(offset):
    url = 'http://list.iqiyi.com/www/2/-------------11-' + str(offset) + '-1---.html'
    time.sleep(1)
    html = get_one_page(url)
    parse_one_page(html)
    # for item in parse_one_page(html):
    #     print(item)
    #     write_to_file(item)

if __name__ == '__main__':
    for i in range(1, 20):
        main(i)

        # pool = Pool()                                #进程池
    # pool.map(main, [i for i in range(1, 5)])
    # pool.terminate()
