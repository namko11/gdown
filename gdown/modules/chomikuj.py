# -*- coding: utf-8 -*-

"""
gdown.modules.chomikuj
~~~~~~~~~~~~~~~~~~~

This module contains handlers for chomikuj.

"""

import re

from ..module import browser, acc_info_template


def accInfo(username, passwd):
    """Returns account info."""
    # TODO: detect premium acc
    acc_info = acc_info_template()
    r = browser()
    rc = r.get('http://chomikuj.pl').content
    token = re.search('name="__RequestVerificationToken" type="hidden" value="(.*?)"', rc).group(1)
    data = {'__RequestVerificationToken': token, 'ReturnUrl': '', 'Login': username, 'Password': passwd, 'rememberLogin': 'true', 'topBar_LoginBtn': 'Zaloguj'}
    rc = r.post('http://chomikuj.pl/action/Login/TopBarLogin', data).content

    transfer = float(re.search('title="Transfer" rel="nofollow"><strong>([0-9,]+) MB</strong>', rc).group(1).replace(',', '.'))
    acc_info['transfer'] = int(transfer * 1024 * 1024)  # convert MB to B

    acc_info['points'] = int(re.search('title="Punkty" rel="nofollow"><strong>([0-9]+)</strong>', rc).group(1))

    return acc_info


def getUrl(link, username, passwd):
    """Returns direct file url."""
    r = browser()
    rc = r.get('http://chomikuj.pl').content
    token = re.search('name="__RequestVerificationToken" type="hidden" value="(.*?)"', rc).group(1)
    data = {'__RequestVerificationToken': token, 'ReturnUrl': link, 'Login': username, 'Password': passwd, 'rememberLogin': 'true', 'topBar_LoginBtn': 'Zaloguj'}
    rc = r.post('http://chomikuj.pl/action/Login/TopBarLogin', data).content
    # get download url
    fileId = re.search('name="FileId" value="([0-9]+)"', rc).group(1)
    token = re.search('name="__RequestVerificationToken" type="hidden" value="(.*?)"', rc).group(1)
    data = {'fileId': fileId, '__RequestVerificationToken': token}
    rc = r.post('http://chomikuj.pl/action/License/Download', data).content
    return re.search('"redirectUrl":"(.*?)"', rc).group(1)
