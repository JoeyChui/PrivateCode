#-*-coding:utf-8-*- 
#2017-9-20 JoeyChui sa517045@mail.ustc.edu.cn

import time, re, requests, json, xlwt
from requests.exceptions import RequestException

def getOnePage(url, encoding = 'UTF-8', headers = {}, cookies = {}, json = False):
    try:
        response = requests.get(url, headers = headers, cookies = cookies)
        if response.status_code == 200:
            response.encoding = encoding
            if json:
                return response.json()
            return response.text
        return None
    except RequestException:
        print("ER:getOnePage", url)
        return None

def reHTML(patternStr, html, first = False):
    pattern = re.compile(patternStr, re.S)
    items = re.findall(pattern, html)
    if items == []:
        return None
    if first:
        return items[0]
    return items


def cutdouhao(num):
    if not num:
        return ''
    result = ''
    for ele in num:
        if ele.isdigit():
            result += ele
    return result

def wtToXLS(content, filename):
    workbook = xlwt.Workbook(encoding = 'utf-8')
    booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok = True)
    for i, rowVal in enumerate(content):
        for j, colVal in enumerate(rowVal):
            booksheet.write(i, j, colVal)
    workbook.save('%s.xls' % filename)
    return

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
          "Host": "seixin.sogou.com"}
cookies = {"Cookie": 'CXID=CF8CB896101787C6447D59728D17B8F7; SUV=00C2A3A53AD223E35A45F4DC35442178; usid=7iRdDXk8rVSsjTxe; SUID=DE4388753765860A5A37BE390001B0DB; ad=lZllllllll2z2EcilllllVIJRallllllNYPRTklllxwlllll4Cxlw@@@@@@@@@@@; ABTEST=8|1514776687|v1; SNUID=93F4B9559F9AFE31CEF79294A0A140D2; JSESSIONID=aaafPYXMUQf_xcDTAmw8v; IPLOC=CN3205; sct=4; weixinIndexVisited=1; ppinf=5|1514778272|1515987872|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToyNzolRTUlQjQlOTQlRTUlOEElOUIlRTglQkUlODl8Y3J0OjEwOjE1MTQ3NzgyNzJ8cmVmbmljazoyNzolRTUlQjQlOTQlRTUlOEElOUIlRTglQkUlODl8dXNlcmlkOjQ0Om85dDJsdUNvcTRJMFZYVjBZU3JxX05sbnV1VmdAd2VpeGluLnNvaHUuY29tfA; pprdig=V_IHkPcQUGLUZqolChlTcdH-iBHulRTIMqRLvrRs1KAD03qPlgmFl28fO80G6geWTysHBUFh1yAMmdSBFLnbPNeDtf58oXqf13nkAPuszKyZAh97KdhSoa78gq134Nr8Jm20hzIGbbKdJcfQFrMokiAG1Yp71XZr6Wt5TvZjoIA; sgid=04-30689591-AVpJrqBsbj0ACsRXt5icPBp4; ppmdig=15147782720000002eaf9fb9965dd6b7b90f5a232ca50164'}

bigTable = [["candidate", "number", "url"]]

starCandidate = ['韩雪', '黄轩', '李小璐', '张雨绮', '迪丽热巴', '黄子韬', '马天宇', '陈学冬', '马可', '唐艺昕', '窦骁', '李治廷', '鹿晗', '赵丽颖', '韩庚', '陈晓', '王一博', '张天爱', '于朦胧', '张晓晨', '宋祖儿', '贾乃亮', '蒋劲夫', '吉克隽逸', '杨蓉', '张嘉倪', '关晓彤', 'angelababy', '吴亦凡', '薛之谦', '翟天临', '杨幂', '张哲瀚', '鞠婧祎', '张歆艺', '古力娜扎', '杨洋', '张艺兴', '胡歌', '甘薇', '李易峰', '刘亦菲', '郑爽', '范冰冰', '林俊杰', '陈伟霆', '田馥甄', '周杰伦', '华晨宇', '周星驰']
for candidate in starCandidate:
    url = 'http://weixin.sogou.com/weixin?type=2&query=' + candidate
    #html = getOnePage(url, headers = headers, cookies = cookies)
    html = getOnePage(url)
    patternStr = 'pagebar_container.*?class="mun">.*?([,\d]+).*?<' 
    item = reHTML(patternStr, html, first = True)
    number = cutdouhao(item)
    print(url, item, number)
    bigTable.append([candidate, number, url])
    time.sleep(10)

wtToXLS(bigTable, "meitiguanzhu")
