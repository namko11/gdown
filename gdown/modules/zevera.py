# -*- coding: utf-8 -*-

"""
gdown.modules.zevera
~~~~~~~~~~~~~~~~~~~

This module contains handlers for zevera.

"""

import re
from dateutil import parser
from datetime import datetime
# from bs4 import BeautifulSoup

from ..module import browser, acc_info_template
from ..exceptions import ModuleError


def accInfo(username, passwd, proxy=False):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser(proxy)
    rc = r.get('http://www.zevera.com/account/login').text
    open('gdown.log', 'w').write(rc)

    viewstate = re.search('name="__VIEWSTATE" id="__VIEWSTATE" value="(.+?)"', rc).group(1)
    viewstategenerator = re.search('name="__VIEWSTATEGENERATOR" id="__VIEWSTATEGENERATOR" value="(.+?)"', rc).group(1)
    eventvalidation = re.search('name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="(.+?)"', rc).group(1)
    data = {'__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': viewstate,
            '__VIEWSTATEGENERATOR': viewstategenerator,
            '__EVENTVALIDATION': eventvalidation,
            'MainContent_txUsername_Raw': username,
            'ctl00$MainContent$txUsername': username,
            'ctl00$MainContent$txUsername$CVS': '',
            'MainContent_txPassword_Raw': passwd,
            'ctl00$MainContent$txPassword': passwd,
            'ctl00$MainContent$txPassword$CVS': '',
            'ctl00$MainContent$cmdLogin': 'submit',
            'DXScript': '1_171,1_94,1_114,1_121,1_164,1_105,1_91,1_156,1_162,1_147',
            'DXCss': '1_4,1_12,1_5,1_3,1_10,1_1,/Content/bootstrap.css,/Content/Site.css,../content/jquery.fullpage.css,../favicon.ico'}
    rc = r.post('http://www.zevera.com/account/login', data=data).text
    open('gdown.log', 'w').write(rc)

    if 'We could not log you into the system. Please check your username and your password.' in rc:
        acc_info['status'] = 'deleted'
    elif '<span id="lbExpirationDate">NEVER</span>' in rc:
        acc_info['status'] = 'premium'
        acc_info['expire_date'] = datetime.max
        acc_info['transfer'] = re.search('<span id="lbTrafficLeft">([0-9 MGB]+?)</span>', rc).group(1)
    elif 'Account Details' in rc:
        if 'id="ContentPlaceHolder1_txExpirationDate">Expired</span>' in rc:
            acc_info['status'] = 'free'
        else:
            expire_date = re.search('id="ContentPlaceHolder1_txExpirationDate">(.+?)</span>', rc).group(1)
            acc_info['expire_date'] = parser.parse(expire_date)
            # if 'id="ContentPlaceHolder1_txExtraTrafficLeft"><a href=\'hosterstatus.aspx\'>UNLIMITED</a>' in rc:  # unlimited transfer
    else:
        raise ModuleError('unknown error')
    return acc_info
