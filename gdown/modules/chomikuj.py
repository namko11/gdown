# -*- coding: utf-8 -*-

"""
gdown.modules.chomikuj
~~~~~~~~~~~~~~~~~~~

This module contains handlers for chomikuj.

"""

import re
from dateutil import parser

from ..module import browser, acc_info_template


def accInfo(username, passwd, proxy=False):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser(proxy)
    rc = r.get('http://chomikuj.pl').text
    token = re.search('name="__RequestVerificationToken" type="hidden" value="(.*?)"', rc).group(1)
    data = {'__RequestVerificationToken': token, 'ReturnUrl': '', 'Login': username, 'Password': passwd, 'rememberLogin': 'true', 'topBar_LoginBtn': 'Zaloguj'}
    rc = r.post('http://chomikuj.pl/action/Login/TopBarLogin', data).text

    if 'Podane hasło jest niewłaściwe' in rc:
        acc_info['status'] = 'deleted'
        return acc_info

    expire_date = re.search('Abonament Twojego Chomika jest ważny do: <h3>([0-9]{4}\-[0-9]{2}\-[0-9]{2})</h3>', rc)
    if expire_date:
        acc_info['status'] = 'premium'
        acc_info['expire_date'] = parser.parse(expire_date.group(1))
    else:
        acc_info['status'] = 'free'

    transfer = float(re.search('title="Transfer" rel="nofollow"><strong>([0-9,]+) MB</strong>', rc).group(1).replace(',', '.'))
    acc_info['transfer'] = int(transfer * 1024 * 1024)  # convert MB to B

    acc_info['points'] = int(re.search('title="Punkty" rel="nofollow"><strong>([0-9]+)</strong>', rc).group(1))

    return acc_info


def getUrl(link, username, passwd):
    """Returns direct file url."""
    r = browser()
    rc = r.get('http://chomikuj.pl').text
    token = re.search('name="__RequestVerificationToken" type="hidden" value="(.*?)"', rc).group(1)
    data = {'__RequestVerificationToken': token, 'ReturnUrl': link, 'Login': username, 'Password': passwd, 'rememberLogin': 'true', 'topBar_LoginBtn': 'Zaloguj'}
    rc = r.post('http://chomikuj.pl/action/Login/TopBarLogin', data).text
    # get download url
    fileId = re.search('name="FileId" value="([0-9]+)"', rc).group(1)
    token = re.search('name="__RequestVerificationToken" type="hidden" value="(.*?)"', rc).group(1)
    data = {'fileId': fileId, '__RequestVerificationToken': token}
    rc = r.post('http://chomikuj.pl/action/License/Download', data).text
    return re.search('"redirectUrl":"(.*?)"', rc).group(1)
