# -*- coding: utf-8 -*-

"""
gdown.modules.nordvpn
~~~~~~~~~~~~~~~~~~~

This module contains handlers for nordvpn.

"""

import re
import time
# from dateutil import parser
# from datetime import datetime, timedelta
# from bs4 import BeautifulSoup

from ..module import browser, acc_info_template
from ..exceptions import ModuleError


def _cf(s):
    # !+[]  1
    # !![]  1
    # ![]   0
    # []    0
    #
    # int(len(host), 10)
    result = ''
    # print(s)  # DEBUG
    ss = re.split('\(|\)', s)
    for s in ss:
        if s in ('+', ''):
            continue
        elif s[0] == '+':
            s = s[1:]
        s = s.replace('!+[]', '1')
        s = s.replace('!![]', '1')
        s = s.replace('![]', '0')
        s = s.replace('[]', '0')
        s = s.replace('+!![]', '10')
        # print(s)  # DEBUG
        result += str(sum([int(i) for i in s.split('+')]))
    return int(result)
    # print(s)
    # return sum([int(i) for i in s.split('+')])


def accInfo(username, passwd, proxy=False):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser(proxy)

    # cloudflare anty-ddos
    rc = r.get("https://nordvpn.com/login").text
    open('gdown.log', 'w').write(rc)
    if 'Checking your browser before accessing' in rc:
        host = re.search('Checking your browser before accessing</span> (.+?)\.</h1>', rc).group(1)
        ans = re.search('.+?={".+?":([+\(\)!\[\]]+)};', rc).group(1)
        ans = _cf(ans)
        for i in re.findall('.+?\..+?([*+-]{1})=([+\(\)!\[\]]+);', rc):
            if i[0] == '*':
                ans *= _cf(i[1])
            elif i[0] == '+':
                ans += _cf(i[1])
            elif i[0] == '-':
                ans -= _cf(i[1])
        ans = ans + len(host)
        # print(f'ans: {ans}')
        print('ans: %s' % ans)
        time.sleep(5)  # 4 is enough?
        jschl_vc = re.search('name="jschl_vc" value="(.+?)"', rc).group(1)
        jschl_pass = re.search('name="pass" value="(.+?)"', rc).group(1)
        params = {'jschl_vc': jschl_vc,
                  'pass': jschl_pass,
                  'jschl-answer': str(ans)}
        rc = r.get('https://nordvpn.com/cdn-cgi/l/chk_jschl', params=params).text
        open('gdown.log', 'w').write(rc)

    print(r.cookies)  # There should be cf_clearance cookie
    mgmnonce = re.search('name="_mgmnonce_user_login" value="(.+?)"', rc).group(1)
    data = {'log': username,
            'pwd': passwd,
            'wp-submit': 'Log In',
            'testcookie': 1,
            'redirect_to': 'https://nordvpn.com/profile/',
            '_mgmnonce_user_login': mgmnonce,
            '_wp_http_referer': '/login/'}
    rc = r.post('https://nordvpn.com/login/', data=data).text
    if 'Your account has expired.' in rc:
        acc_info['status'] = 'free'
    else:
        print(r.cookies)
        open('gdown.log', 'w').write(rc)
        raise ModuleError('Unknown response.')
    return acc_info
