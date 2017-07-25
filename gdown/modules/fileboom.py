# -*- coding: utf-8 -*-

"""
gdown.modules.uploaded
~~~~~~~~~~~~~~~~~~~

This module contains handlers for uploaded.

"""

import re
from dateutil import parser
from datetime import datetime
from bs4 import BeautifulSoup
# from time import sleep
# from decimal import Decimal

from ..core import captcha
from ..exceptions import ModuleError
from ..module import browser, acc_info_template


def accInfo(username, passwd, proxy=False):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser(proxy)
    rc = r.get('https://fileboom.me/login.html').text
    open('gdown.log', 'w').write(rc)
    csrf_token = re.search('value="(.+?)" name="YII_CSRF_TOKEN"', rc).group(1)
    data = {'YII_CSRF_TOKEN': csrf_token,
            'LoginForm[username]': username,
            'LoginForm[password]': passwd,
            'LoginForm[rememberMe]': 0}
    if 'LoginForm[verifyCode]' in rc:
        # print('CAPTCHA')
        img_url = 'https://fileboom.me' + re.search('id="captcha_auth0" src="(/auth/captcha.html\?v=.+?)"', rc).group(1)
        img = r.get(img_url).content
        data['LoginForm[verifyCode]'] = captcha(img)  # TODO: verification (False)
    rc = r.post('https://fileboom.me/login.html', data=data).text
    open('gdown.log', 'w').write(rc)
    if 'The verification code is incorrect.' in rc:  # wrong captcha
        # TODO: report wrong captcha
        print('wrong captcha')
        return accInfo(username, passwd, proxy)
    elif 'Incorrect username or password' in rc:
        acc_info['status'] = 'deleted'
        return acc_info
    elif 'You account was used from a different countries and automatically locked for security reasons.' in rc:
        acc_info['status'] = 'blocked'
        return acc_info

    rc = r.get('https://fileboom.me/site/profile.html').text  # TODO?: redirect on login?
    open('gdown.log', 'w').write(rc)
    if '<strong>Free <br>' in rc or '    Free</span>' in rc:
        acc_info['status'] = 'free'
        return acc_info
    elif 'Premium expires: ' in rc:
        acc_info['transfer'] = re.findall('<b><a href="/user/statistic.html">([0-9\.]+ M?G?B)</a></b><br>', rc)[1]  # first is used
        acc_info['status'] = 'premium'
        if '<b>LifeTime</b>' in rc:
            acc_info['expire_date'] = datetime.max
        else:
            # d = re.search('Premium expires: <b>([0-9]{4})\.([0-9]{2})\.([0-9]{2})</b>', rc)
            expire_date = re.search('Premium expires:            <b>([0-9\.]+)</b>', rc).group(1)
            # bs = BeautifulSoup(rc, 'lxml')
            # expire_date = bs.find('strong', class_='nowrap-item').contents[0].strip()
            if expire_date == 'LifeTime':
                acc_info['expire_date'] = datetime.max
            else:
                acc_info['expire_date'] = parser.parse(expire_date)
            # acc_info['expire_date'] = datetime(int(d.group(1)), int(d.group(2)), int(d.group(3)))
        return acc_info
    else:
        open('gdown.log', 'w').write(rc)
        raise ModuleError('Unknown error, full log in gdown.log')
