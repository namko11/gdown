# -*- coding: utf-8 -*-

"""
gdown.modules.keep2share
~~~~~~~~~~~~~~~~~~~

This module contains handlers for keep2share.

"""

import re
from datetime import datetime
from bs4 import BeautifulSoup
from dateutil import parser

from ..core import captcha
from ..module import browser, acc_info_template
from ..exceptions import ModuleError


def accInfo(username, passwd, proxy=False):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser(proxy)
    rc = r.get('https://keep2share.cc/login.html').text
    open('gdown.log', 'w').write(rc)
    csrf_token = re.search('value\="(.+?)" name\="YII_CSRF_TOKEN"', rc).group(1)
    data = {'LoginForm[username]': username,
            'LoginForm[password]': passwd,
            'LoginForm[rememberMe]': 0,
            'YII_CSRF_TOKEN': csrf_token}
    if 'LoginForm_verifyCode' in rc:
        # raise ModuleError('captcha')
        print('captcha')  # DEBUG
        img_url = 'https://keep2share.cc' + re.search('id="captcha_auth0" src="(/auth/captcha.html\?v=.+?)"', rc).group(1)
        img = r.get(img_url).content
        data['LoginForm[verifyCode]'] = captcha(img)  # TODO: verification (False)
    rc = r.post('https://keep2share.cc/login.html', data=data).text
    open('gdown.log', 'w').write(rc)

    # if '<a href="/premium.html" class="free" style="color: red">free</a>' in rc:
    if 'The verification code is incorrect.' in rc:  # wrong captcha
        # TODO: report wrong captcha
        print('wrong captcha')
        return accInfo(username, passwd, proxy)
    # elif '<strong>Free <br>' in rc:
    elif '<strong>Free</strong>' in rc:
        acc_info['status'] = 'free'
        return acc_info
    elif 'You account was used from a different countries and automatically locked for security reasons.' in rc or 'Your account is blocked for sharing' in rc:
        acc_info['status'] = 'blocked'
        return acc_info
    elif 'Incorrect username or password' in rc:
        acc_info['status'] = 'deleted'
        return acc_info
    elif 'Premium expires: ' in rc:
        acc_info['status'] = 'premium'
        if '<b>LifeTime</b>' in rc:
            acc_info['expire_date'] = datetime.max
        else:
            # d = re.search('Premium expires: <b>([0-9]{4})\.([0-9]{2})\.([0-9]{2})</b>', rc)
            bs = BeautifulSoup(rc, 'lxml')
            expire_date = bs.find('strong', class_='nowrap-item').contents[0].strip()
            if expire_date == 'LifeTime':
                acc_info['expire_date'] = datetime.max
            else:
                acc_info['expire_date'] = parser.parse(expire_date)
            # acc_info['expire_date'] = datetime(int(d.group(1)), int(d.group(2)), int(d.group(3)))
            rc = r.get('https://keep2share.cc/site/profile.html').text
            open('gdown.log', 'w').write(rc)
            acc_info['transfer'] = re.findall('href="/user/statistic.html">([0-9\. MGB]+)</a>', rc)[1]
        return acc_info
    else:
        open('gdown.log', 'w').write(rc)
        raise ModuleError('Unknown error, full log in gdown.log')
