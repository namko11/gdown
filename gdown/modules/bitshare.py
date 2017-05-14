# -*- coding: utf-8 -*-

"""
gdown.modules.bitshare
~~~~~~~~~~~~~~~~~~~

This module contains handlers for bitshare.

"""

import re
import os
from hashlib import md5
from dateutil import parser

from ..module import browser, acc_info_template
from ..exceptions import ModuleError, IpBlocked


def accInfo(username, passwd, proxy=False):
    """Returns account info."""
    acc_info = acc_info_template()
    r = browser(proxy)
     # api version (do not return expire date)
    content = r.post('http://bitshare.com/api/openapi/login.php', {'user': username, 'password': md5(passwd).hexdigest()}).text  # get hashkey (login)
    if content == 'ERROR:Username is not matching to the provided password!':
        acc_info['status'] = 'deleted'
        return acc_info
    elif content == 'ERROR:Due to an IP-Block because of security reasons you are not allowed to send more than 10 login requests per 10 minutes!':
        raise IpBlocked
    elif 'ERROR' in content:
        open('gdown.log', 'w').write(content)
        raise ModuleError('Unknown error, full log in gdown.log')
    content = r.post('http://bitshare.com/api/openapi/accountdetails.php', {'hashkey': content[8:]}).text
    content = re.search('SUCCESS:([0-9]+)#[0-9]+#[0-9]+#[0-9]+#.+', content).group(1)  # 0=noPremium | 1=premium
    if content == '1':
        acc_info['status'] = 'premium'
        acc_info['expire_date'] = expireDate(username, passwd)     # check expire date
    elif content == '0':
        acc_info['status'] = 'free'
    return acc_info


def expireDate(username, passwd):  # manual (without api)
    r = browser()
    r.get('http://bitshare.com/?language=EN')   # change language (regex)
    values = {'user': username, 'password': passwd, 'rememberlogin': '1', 'submit': 'Login'}
    content = r.post('http://bitshare.com/login.html', values).text
    if '(<b>Premium</b>)' in content:
        content = r.get('http://bitshare.com/myaccount.html').text
        content = re.search('Valid until: ([0-9]+\-[0-9]+\-[0-9]+)', content).group(1)
        return parser.parse(content)
    #elif '(<b><a href="http://bitshare.com/myupgrade.html">Free</a></b>)' in content:  # no need to check this
    #   return 0
    #elif 'Wrong Username or Password!' in content:
    #   return -2
    else:
        open('gdown.log', 'w').write(content)
        raise ModuleError('Unknown error, full log in gdown.log')


def getUrl(link, username, passwd):
    """Returns direct file url.
    IP validator is NOT present."""
    r = browser()
    values = {'user': username, 'password': passwd, 'rememberlogin': '1', 'submit': 'Login'}
    r.post('http://bitshare.com/login.html', values)
    return r.get(link).url


def upload(username, passwd, filename):
    """Returns uploaded file url."""
    file_size = int(os.path.getsize(filename))  # get file size
    r = browser()
    hashkey = r.post('http://bitshare.com/api/openapi/login.php', {'user': username, 'password': md5(passwd).hexdigest()}).text[8:]  # get hashkey (login)
    host = r.post('http://bitshare.com/api/openapi/upload.php', {'action': 'getFileserver'}).text[8:]  # get host
    content = ''
    while 'SUCCESS' not in content:
        content = r.post(host, {'hashkey': hashkey, 'filesize': file_size}, files={'file': open(filename, 'rb')}).text  # upload
    return re.search('SUCCESS:(.+?)#\[URL', content).group(1)
