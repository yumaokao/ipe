#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

import re
import urllib
import requests
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

    payload = {'currentPage': '2',
               'pageSize': '100',
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

    r = requests.post("http://arsp.most.gov.tw/NSCWebFront/modules/talentSearch/talentSearch.do?action=initSearchList&LANG=chi", headers=headers, data=payload)
    print(r.text)
    text = urllib.parse.unquote(r.text)
    # print(text)


if __name__ == "__main__":
    main()
