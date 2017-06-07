# -*- coding: utf-8 -*-

"""
gdown.modules.mediafire
~~~~~~~~~~~~~~~~~~~

This module contains handlers for mediafire.

"""

import re
from dateutil import parser

from ..module import browser, acc_info_template
from mediafire import MediaFireApi
from mediafire.api import MediaFireApiError


def accInfo(username, passwd, proxy=False):
    acc_info = acc_info_template()
    r = MediaFireApi()
    try:
        r.session = r.user_get_session_token(42511, username, passwd)
    except MediaFireApiError as e:
        if e.code == 107:
            acc_info['status'] = 'deleted'
            return acc_info
        elif e.code == 114:
            acc_info['status'] = 'blocked'
            return acc_info
        elif e.code == 129:
            print('ip blocked?')
            asasdas
        print(e)
        print(r.session)
    rc = r.user_get_info()
    if rc['user_info']['premium'] == 'no':
        acc_info['status'] = 'free'
        return acc_info
    rc = r.request('billing/get_invoice')
    acc_info['status'] = 'premium'
    acc_info['expire_date'] = parser.parse(rc['invoice']['recurring_startdate'])
    return acc_info
    '''
    rc = r.get('https://www.mediafire.com/templates/login_signup/login_signup.php').text
    token = re.search('name="security" value="(.+?)"', rc).group(1)
    data = {'security': token, 'login_email': username, 'login_pass': passwd, 'login_remember': 'on'}
    rc = r.post('https://www.mediafire.com/dynamic/client_login/mediafire.php', data).text
    open('log.log', 'w').write(rc)
    et = re.search('var et = ([\-0-9]+);', rc).group(1)
    print('et: %s' % et)
    '''


def getUrl(link, premium_key, username=None, passwd=None):
    """Returns direct file url."""
    fileid = re.match('http://[w\.]{,4}mediafire.com/\?(.+)', link).group(1)
    r = browser()
    values = {'premium_key': premium_key, 'files': fileid}
    content = r.post('http://www.mediafire.com/basicapi/premiumapi.php', values).text
    link = re.search('<url>(.+)</url>', content).group(1)
    return r.get(link).url
