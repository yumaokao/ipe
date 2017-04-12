#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

import re
import urllib
import requests
from lxml.html import document_fromstring


COOKIE = 'ASP.NET_SessionId=jqhc2aeu5q1acef4zn104qj4; .ASPXAUTH=87B6BF1636B40A25EE6C11C7AE359FE7A6236A1CF0084B0D7BB11161F95A9C2E19B5AD565EAF499C12245C29FC2FC724BE8D7BE90F74B47A378DC700E450273F0C70776E328AB2AFD7B67507FBFD69D27167FCC160B8B3B379CCF89213D280208F118DB3ADFFA1F5EEFDAB994DA37BBBD96FD5B11FE9EFCFB6DAB59D9D221773CA293F718339DCEDB29A1B87411A6D197CA817C34591F77B0F1C735870AD583A; ajaxkey=66AF219464EA8353372192D7B4D1167359872290589D5454; __utmt=1; __utma=105455707.1441289696.1490357465.1490390292.1490392206.10; __utmb=105455707.1.10.1490392206; __utmc=105455707; __utmz=105455707.1490357465.1.1.utmcsr=messenger.com|utmccn=(referral)|utmcmd=referral|utmcct=/'


def decode_u(a):
    if a is None:
        return ''
    b = "b'" + a.replace('%u', '\\u') + "'.decode('unicode-escape')"
    # print(b)
    try:
        s = eval(b)
    except:
        s = b
    return s

def main():
    headers = {'Origin': 'http://www.ipe.org.cn',
               'X-Requested-With': 'XMLHttpRequest',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'Referer': 'http://www.ipe.org.cn/IndustryRecord/Regulatory.aspx?index=0',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
               'Cookie': COOKIE}

    payload = {'cmd': 'getRecords',
               'pageSize': '100',
               'pageIndex': '1',
               'countryId': '2',
               'provinceId': '0',
               'cityId': '-1',
               'startYear': '-1',
               'endYear': '-1',
               'professionId': '-1',
               'itemType': '1',
               'companyType': '0',
               'indusName': '',
               'fengxian': '0',
               'ishistory': '2'}

    r = requests.post("http://www.ipe.org.cn/data_ashx/GetAirData.ashx", headers=headers, data=payload)
    text = urllib.parse.unquote(r.text)
    m = re.search("recordCount:'(\d+)'", text)
    if m is None:
        print('not found recordCount')
        return
    pages = int(int(m.group(1)) / 100)

    for p in range(1009, pages + 2):
        # print(p)
        payload['pageIndex'] = str(p)

        r = requests.post("http://www.ipe.org.cn/data_ashx/GetAirData.ashx", headers=headers, data=payload)
        # print(r)
        # print(urllib.parse.unquote(r.text))
        text = urllib.parse.unquote(r.text)
        text = text.replace('\n', '').replace('\r', '')
        m = re.search("content:'(.*)'", text)
        if m is None:
            print('not found context')
            print(text)
            return

        # print(m.group(1))
        root = document_fromstring(m.group(1))
        # print(len(list(root.iter("tr"))))
        for elem in root.iter("tr"):
            # id, name, location, year, times
            print("{}, {}, {}, {}, {}".format(elem[0].text, 
                decode_u(elem[1].text),
                decode_u(elem[2].text) + decode_u(elem[2][0].text),
                decode_u(elem[3].text),
                decode_u(elem[4].text)))


if __name__ == "__main__":
    main()
