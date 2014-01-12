# -*- coding: utf-8 -*-

"""
gdown.modules.weeb
~~~~~~~~~~~~~~~~~~~

This module contains handlers for weeb.

"""

import re

from ..module import browser, acc_info_template


def accInfo(username, passwd, proxy=False):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser(proxy)
    values = {'username': username, 'userpassword': passwd}
    rc = r.post('http://weeb.tv/account/login', values).content

    r.cookies['___utmvc'] = 'navigator=object,navigator.vendor=Google Inc.,opera=ReferenceError: opera is not defined,ActiveXObject=ReferenceError: ActiveXObject is not defined,navigator.appName=Netscape,plugin=dll,webkitURL=function,navigator.plugins.length==0=false,digest=29487,29625,29669,29721'
    print r.cookies
    #print r.get('http://weeb.tv/_Incapsula_Resource?SWKMTFSR=1&e=0.5699805873446167').content
    r.headers['Referer'] = 'http://weeb.tv/account/login/do'
    #print r.get('http://weeb.tv/_Incapsula_Resource?SWHANEDL=2033807792603236480,17378173075619522697,9780620802265862016,42735').content

    rc = r.get('http://weeb.tv/account/login/do').content
    #print rc
