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
    opera = browser()
    # get token
    content = opera.get('http://chomikuj.pl').content
    token = re.search('name="__RequestVerificationToken" type="hidden" value="(.*?)"', content).group(1)
    # login
    content = opera.post('http://chomikuj.pl/action/Login/TopBarLogin', {'__RequestVerificationToken': token, 'ReturnUrl': link, 'Login': username, 'Password': passwd, 'rememberLogin': 'true', 'topBar_LoginBtn': 'Zaloguj'}).content
    # get download url
    fileId = re.search('name="FileId" value="([0-9]+)"', content).group(1)
    token = re.search('name="__RequestVerificationToken" type="hidden" value="(.*?)"', content).group(1)
    content = opera.post('http://chomikuj.pl/action/License/Download', {'fileId': fileId, '__RequestVerificationToken': token}).content
    return re.search('"redirectUrl":"(.*?)"', content).group(1)
