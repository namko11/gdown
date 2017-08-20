# -*- coding: utf-8 -*-

"""
gdown.modules.mediafire
~~~~~~~~~~~~~~~~~~~

This module contains handlers for mediafire.

"""

import re
import time
from hashlib import sha1
from dateutil import parser
from requests.exceptions import ConnectionError  # TODO?: import connection errors into gdown
from simplejson.scanner import JSONDecodeError

from ..module import browser, acc_info_template
from ..exceptions import ModuleError


def accInfo(username, passwd, proxy=False):
    acc_info = acc_info_template()
    r = browser(proxy=proxy)
    application_id = 42511  # mediafireapi official client
    signature = sha1()
    signature.update(username.encode('ascii'))
    signature.update(passwd.encode('ascii'))
    signature.update(str(application_id).encode('ascii'))
    signature = signature.hexdigest()
    data = {'application_id': application_id,
            'signature': signature,
            'email': username,
            'password': passwd,
            'response_format': 'json'}
    try:
        rc = r.post('https://www.mediafire.com/api/1.5/user/get_session_token.php', data=data).json()
    except ConnectionError as e:
        print('connection error')
        time.sleep(1)
        return accInfo(username=username, passwd=passwd, proxy=proxy)
    result = rc['response']['result']  # TODO: validate this
    if result == 'Error':
        if rc['response']['message'] in ('The Credentials you entered are invalid', 'One or more parameters for this request are invalid'):
            acc_info['status'] = 'deleted'
            return acc_info
        elif rc['response']['message'] == 'Account Suspended':
            acc_info['status'] = 'blocked'
            return acc_info
        elif 'Internal server error' in rc['response']['message']:
            time.sleep(5)
            return accInfo(username, passwd, proxy=proxy)
        else:
            print(rc)
            raise ModuleError('Unknown error during login.')
    token = rc['response']['session_token']
    # ekey = rc['response']['ekey']
    # pkey = rc['response']['pkey']

    data = {'session_token': token,
            'response_format': 'json'}
    try:
        rc = r.post('http://www.mediafire.com/api/1.5/user/get_info.php', data=data).json()
    except JSONDecodeError:
        print('ip banned?')
        time.sleep(5)
        rc = r.post('http://www.mediafire.com/api/1.5/user/get_info.php', data=data).json()
    if 'user_info' not in rc['response']:  # DEBUG
        if rc['response'].get('message') == 'Internal server error (1002)':
            time.sleep(5)
            rc = r.post('http://www.mediafire.com/api/1.5/user/get_info.php', data=data).json()
        else:
            print(rc)
    # result = rc['response']['result']  # TODO?: validate this
    premium = rc['response']['user_info']['premium'] == 'yes'
    # print(rc)
    if premium:
        acc_info['status'] = 'premium'
        data = {'session_token': token,
                'response_format': 'json'}
        rc = r.post('https://www.mediafire.com/api/1.5/billing/get_invoice.php', data=data).json()
        # print(rc)
        # result = rc['response']['result']  # TODO?: validate this
        acc_info['expire_date'] = parser.parse(rc['response']['invoice']['recurring_startdate'])
        # TODO: transfer https://www.mediafire.com/developers/core_api/1.3/user/#get_limits
    else:
        acc_info['status'] = 'free'
    return acc_info


def getUrl(link, premium_key, username=None, passwd=None):
    """Returns direct file url."""
    fileid = re.match('http://[w\.]{,4}mediafire.com/\?(.+)', link).group(1)
    r = browser()
    values = {'premium_key': premium_key, 'files': fileid}
    content = r.post('http://www.mediafire.com/basicapi/premiumapi.php', values).text
    link = re.search('<url>(.+)</url>', content).group(1)
    return r.get(link).url
