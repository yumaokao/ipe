#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

import re
import urllib
import requests
import pandas as pd
from lxml import etree
from lxml.html import document_fromstring


COOKIE = 'JSESSIONID=9D08CD5044B57DB94723D285AF217184; currentUserLocale=zh_TW; _ga=GA1.3.124500067.1491977542'


def main():
    headers = {'Origin': 'http://arsp.most.gov.tw',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Referer': 'http://arsp.most.gov.tw/NSCWebFront/modules/talentSearch/talentSearch.do?action=initSearchList&LANG=chi',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
               'Cookie': COOKIE}

    payload = {'currentPage': '',
               'pageSize': '',
               'sortCondition': '',
               'specCode': '',
               'isSearch': '1',
               'LANG': 'chi',
               'nameChi': '',
               'sex': 'A',
               'organ_2_1': '',
               'organ_3_1': '',
               'organ_2_2': '',
               'organ_3_2': '',
               'organ_2_3': '',
               'organ_3_3': '',
               'organ_2_4': '',
               'organDesc': '',
               'kind_1': '',
               'spec_1': 'H',
               'spec_2': 'H17',
               'spec_3': '',
               'academicExpertiseFullSearch': '',
               'code_1': ''}

    url = "http://arsp.most.gov.tw/NSCWebFront/modules/talentSearch/"
    url_search = url + "talentSearch.do?action=initSearchList&LANG=chi"
    r = requests.post(url + "talentSearch.do?action=initSearchList&LANG=chi", headers=headers, data=payload)
    text = urllib.parse.unquote(r.text)
    m = re.search("共<em>(\d+)</em>筆資料│", text)
    if m is None:
        print('not found count')
        return
    pages = int(int(m.group(1)) / 100)

    data = []
    for p in range(1, pages + 2):
        payload['currentPage'] = str(p)
        r = requests.post(url_search, headers=headers, data=payload)
        text = urllib.parse.unquote(r.text)
        # print(text)
        root = document_fromstring(text)
        div = root.find('.//div[@class="c30Tblist2"]')
        table = div[0]
        for tr in table.iterfind('.//tr'):
            # print(etree.tostring(tr, encoding='unicode'))
            tds = tr.findall('.//td')
            if len(tds) != 7:
                continue
            # print(etree.tostring(tr, encoding='unicode'))

            adata = []
            # name
            name = tds[0].find('.//a')
            adata.extend(name.xpath('.//text()'))

            # rsno
            # adata.append(name.get('href'))
            qs = urllib.parse.urlparse(name.get('href')).query
            rsno = urllib.parse.parse_qs(qs)['rsNo'][0]
            adata.append(rsno)

            # dep
            adata.append(tds[1].text.strip())
            # pos
            adata.append(tds[2].text.strip())
            # tel
            adata.append(tds[3].text.strip())

            print(adata)
            data.append(adata)


        break

    for rs in data:
        # talentSearch.do?action=initRsm02&rsNo=fe7ff544a15f41e585199d39c7c4177c
        rsno = rs[2]
        r = requests.get('{}talentSearch.do?action=initRsm02&rsNo={}'.format(url, rsno), headers=headers, data=payload)
        print(r.status_code)
        # print(r.text)

    # df = pd.DataFrame(data, columns=['cname', 'ename', 'link', 'dep', 'pos', 'contact'])
    # df.to_csv('arsp.csv')


if __name__ == "__main__":
    main()
