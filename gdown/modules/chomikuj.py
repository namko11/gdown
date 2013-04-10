# -*- coding: utf-8 -*-

"""
gdown.modules.chomikuj
~~~~~~~~~~~~~~~~~~~

This module contains handlers for chomikuj.

"""

import re

from ..module import browser


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
