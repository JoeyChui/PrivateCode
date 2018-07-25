# -*- coding: utf-8 -*-
from urllib import urlencode

from requests.exceptions import RequestException

import requests
import json

def get_page_index(offset, keyword):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': 3

    }
    url = 'http://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('cuo cuo cuo')
        return None

def parse_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article.url')


def main():
    html = get_page_index(0, '街拍')
    for url in parse_page_index(html):
        print(url)

if __name__ == '__main__':
    main()